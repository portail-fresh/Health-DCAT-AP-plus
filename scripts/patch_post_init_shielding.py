#!/usr/bin/env python
"""
Post-process the generated Python dataclasses (health_dcat_ap_plus.py) to
fix a real, reproducible construction crash: a subclass that narrows a
slot's range or multivalued-ness via slot_usage still unconditionally
calls super().__post_init__(**kwargs) at the end of its own __post_init__,
and the parent's own __post_init__ re-processes that same slot under its
own, now-stale assumption -- crashing (e.g. TypeError: ...Frequency()
argument after ** must be a mapping, not URIorCURIE) or, in other cases,
silently corrupting an already-correct value.

Confirmed as a real, current problem, not hypothetical: HealthDataset.frequency
crashes construction outright; HealthDistribution.format crashes the same
way. Both reproduced directly (see docs/architecture-verification.md
section 6 and 7) -- this isn't limited to HealthDataset, and there's no
reason to expect it's limited to the fields already found by hand either.

This script fixes it at the *generated source* level, not via a runtime
monkeypatch: it finds every class that needs shielding (derived from the
schema itself, not a hand-maintained list -- see compute_shield_map below)
and rewrites that one `super().__post_init__(**kwargs)` line into a block
that saves the affected fields' already-correct values, blanks them so the
parent's own re-processing is a no-op, calls the parent, then restores the
real values. This is deliberately NOT a global, import-time patch: it only
ever touches each affected class's own generated method body, so
constructing a plain, un-profiled dcat-ap-plus class elsewhere in the same
process is completely unaffected.

Run as part of `just gen-python` (see justfile) -- not a separate,
forgettable step. Fails loudly (raises, non-zero exit) if it can't find
the exact pattern it expects to patch for a class the schema says needs
it, rather than silently leaving the crash in place while looking like it
succeeded.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from linkml_runtime import SchemaView

SUPER_POST_INIT_CALL = "super().__post_init__(**kwargs)"


def _is_compatible_narrowing(child_range: str, parent_range: str, sv: SchemaView) -> bool:
    """True if child_range is parent_range or a real subclass of it -- the
    one case where the parent's own re-processing is harmless (polymorphic
    isinstance checks in the generated coercion code just pass the
    already-correct, more-specific instance through unchanged). Confirmed
    empirically earlier: HealthKind (is_a Kind) narrowing contact_point
    needs no shielding at all, precisely because of this."""
    if child_range == parent_range:
        return True
    try:
        return parent_range in sv.class_ancestors(child_range)
    except ValueError:
        return False


def compute_shield_map(sv: SchemaView) -> dict[str, list[str]]:
    """{class_name: [slot names that need shielding before this class's own
    super().__post_init__() call]}.

    Derived from the schema, not hand-maintained: for every class with its
    own is_a parent and its own local slot_usage, compare each overridden
    slot's induced range/multivalued/inlined(_as_list) against the parent's
    induced value for the same slot. A mismatch that isn't a safe subclass
    narrowing means the parent's own generated coercion code would either
    crash or silently re-wrap an already-correct value -- shield it.
    Over-inclusion is harmless (shielding a field the parent's own code
    wouldn't actually have touched, or wouldn't have broken, is a no-op:
    save-blank-restore around a call that does nothing to that field
    either way) so this deliberately doesn't try to be more precise than
    that -- see the module docstring. Scans every class in the merged
    schema (imports=True), not just the Health<X> ones: the same pattern
    shows up purely inside dcat-ap-plus's own class hierarchy too (Concept,
    ConceptScheme, PeriodOfTime -- checked directly), unrelated to
    anything this repo's port does.

    inlined/inlined_as_list mismatches are checked unconditionally,
    independent of the range-compatibility check below -- confirmed as a
    real, distinct gap, not hypothetical: HealthDataset.source narrows
    inlined_as_list true -> false while keeping a range that's a genuine
    subclass (HealthDataset is_a Dataset), so the range-compatibility
    check alone judged it safe -- but the parent's own generated
    __post_init__ still tries to key-construct a full nested object from
    what's now a bare string, crashing exactly like a range mismatch
    would. Representation (keyed dict vs. bare value) is an orthogonal
    risk factor from range compatibility, not implied by it.
    """
    shield_map: dict[str, list[str]] = {}
    for cls_name in sv.all_classes(imports=True):
        cls = sv.get_class(cls_name)
        if not cls.is_a or not cls.slot_usage:
            continue
        parent = cls.is_a
        shielded: list[str] = []
        for slot_name in cls.slot_usage:
            try:
                child_slot = sv.induced_slot(slot_name, cls_name)
                parent_slot = sv.induced_slot(slot_name, parent)
            except ValueError:
                continue
            range_changed = child_slot.range != parent_slot.range
            mv_changed = bool(child_slot.multivalued) != bool(parent_slot.multivalued)
            inlined_changed = bool(child_slot.inlined) != bool(parent_slot.inlined) or bool(
                child_slot.inlined_as_list
            ) != bool(parent_slot.inlined_as_list)
            if not range_changed and not mv_changed and not inlined_changed:
                continue
            compatible = (not range_changed) or _is_compatible_narrowing(child_slot.range, parent_slot.range, sv)
            if not compatible or mv_changed or inlined_changed:
                shielded.append(slot_name)
        if shielded:
            shield_map[cls_name] = shielded
    return shield_map


def _class_block_bounds(lines: list[str], class_name: str) -> tuple[int, int]:
    """Return (start, end) line indices [start, end) of `class {class_name}(...):`'s
    body, i.e. up to (not including) the next top-level `class ` line."""
    start = None
    for i, line in enumerate(lines):
        if line.startswith(f"class {class_name}("):
            start = i
            break
    if start is None:
        raise RuntimeError(
            f"patch_post_init_shielding: expected to find 'class {class_name}(' in the "
            "generated file but didn't -- the schema says this class needs __post_init__ "
            "shielding (see compute_shield_map), so either the class was renamed/removed "
            "or gen-python's output format changed. Not silently skipping -- fix this "
            "script or the shield map before trusting the generated file."
        )
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("class "):
            end = i
            break
    return start, end


def patch_file(path: Path, shield_map: dict[str, list[str]]) -> int:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    patched = 0
    for cls_name, fields in shield_map.items():
        start, end = _class_block_bounds(lines, cls_name)
        target_idx = None
        indent = None
        for i in range(start, end):
            stripped = lines[i].strip()
            if stripped == SUPER_POST_INIT_CALL:
                target_idx = i
                indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
                break
        if target_idx is None:
            raise RuntimeError(
                f"patch_post_init_shielding: class {cls_name!r} needs shielding for "
                f"{fields!r} (per the schema) but no bare '{SUPER_POST_INIT_CALL}' line "
                "was found in its generated __post_init__. Either this class no longer "
                "generates its own __post_init__ override, or gen-python's output format "
                "changed. Not silently skipping -- investigate before trusting the "
                "generated file."
            )
        field_tuple = ", ".join(f'"{f}"' for f in fields)
        if len(fields) == 1:
            field_tuple += ","
        replacement = (
            f"{indent}__post_init_shield = {{n: getattr(self, n) for n in ({field_tuple})}}\n"
            f"{indent}for __n in __post_init_shield:\n"
            f"{indent}    setattr(self, __n, None)\n"
            f"{indent}{SUPER_POST_INIT_CALL}\n"
            f"{indent}for __n, __v in __post_init_shield.items():\n"
            f"{indent}    setattr(self, __n, __v)\n"
        )
        lines[target_idx] = replacement
        patched += 1
    path.write_text("".join(lines), encoding="utf-8")
    return patched


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("generated_python_file", help="Path to the gen-project/gen-pydantic-generated dataclass file")
    parser.add_argument(
        "--schema",
        default="src/health_dcat_ap_plus/schema/health_dcat_ap_plus.yaml",
        help="Path to the merged LinkML schema the file was generated from",
    )
    args = parser.parse_args()

    sv = SchemaView(args.schema)
    shield_map = compute_shield_map(sv)
    n_fields = sum(len(v) for v in shield_map.values())
    print(f"patch_post_init_shielding: {len(shield_map)} class(es), {n_fields} field(s) need shielding:")
    for cls_name, fields in shield_map.items():
        print(f"  {cls_name}: {', '.join(fields)}")

    path = Path(args.generated_python_file)
    patched = patch_file(path, shield_map)
    print(f"Patched {patched} class(es) in {path}")


if __name__ == "__main__":
    sys.exit(main())
