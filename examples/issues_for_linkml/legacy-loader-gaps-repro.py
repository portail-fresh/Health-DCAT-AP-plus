"""Minimal, network-free reproductions for LinkML 1.12.1 (legacy SchemaLoader).

Case 1  gen-yaml's merged output is not re-importable (imports kept + elements copied).
Case 2  nested bare relative import of a REMOTE schema: resolved against the root's folder.
Case 3  nested './relative' import of a REMOTE schema: path-separator / '//' corruption.

Everything is served from a local http.server, so no w3id / GitHub is involved.
Run with a venv that has linkml==1.12.1:  python -W ignore -I legacy-loader-gaps-repro.py [posix]
Not reported upstream yet (see ROADMAP.md, "Future improvements" 2); kept here for when it is.
Passing 'posix' emulates Linux path semantics for linkml.utils.mergeutils only.
"""
import functools
import http.server
import shutil
import sys
import tempfile
import textwrap
import threading
from pathlib import Path

import linkml
import yaml
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.yamlgen import YAMLGenerator

if "posix" in sys.argv[1:]:
    import posixpath
    import types
    from pathlib import PurePosixPath

    import linkml.utils.mergeutils as _mu

    _mu.Path = PurePosixPath
    _mu.os = types.SimpleNamespace(path=posixpath)

import importlib.metadata as md  # noqa: E402

print(f"linkml {md.version('linkml')}, platform {sys.platform}, posix-emulation={'posix' in sys.argv[1:]}")

work = Path(tempfile.mkdtemp(prefix="upstream_repro_", dir=Path(__file__).parent))


def w(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text), encoding="utf-8", newline="\n")
    return path


HEADER = """\
    id: https://example.org/{name}
    name: {name}
    prefixes:
      linkml: https://w3id.org/linkml/
      ex: https://example.org/
    default_prefix: ex
    default_range: string
"""


def schema(name: str, imports: list[str], body: str = "") -> str:
    imps = "".join(f"  - {i}\n" for i in imports)
    return textwrap.dedent(HEADER).format(name=name) + f"imports:\n{imps}" + textwrap.dedent(body)


def attempt(label, fn):
    try:
        out = fn()
        print(f"  {label}: OK")
        return out
    except BaseException as e:  # noqa: BLE001
        print(f"  {label}: FAIL  {type(e).__name__}: {str(e).splitlines()[0][:170]}")


# ------------------------------------------------------------------ case 1
print("\nCase 1: merged gen-yaml output, re-imported")
c1 = work / "case1"
w(c1 / "base.yaml", schema("base", ["linkml:types"], """\
    classes:
      Thing:
        attributes:
          label: {}
"""))
w(c1 / "mid.yaml", schema("mid", ["linkml:types", "base"], """\
    classes:
      Sub:
        is_a: Thing
"""))
merged = YAMLGenerator(str(c1 / "mid.yaml")).serialize()
(c1 / "mid_merged.yaml").write_text(merged, encoding="utf-8", newline="\n")
m = yaml.safe_load(merged)
print(f"  merged output keeps imports={m['imports']} AND defines classes={sorted(m['classes'])}")
w(c1 / "top.yaml", schema("top", ["linkml:types", "mid_merged"], """\
    classes:
      Leaf:
        is_a: Sub
"""))
attempt("import the ORIGINAL mid.yaml   ", lambda: PythonGenerator(str(c1 / "mid.yaml")).serialize())
w(c1 / "top_orig.yaml", schema("top_orig", ["linkml:types", "mid"], "classes:\n  Leaf:\n    is_a: Sub\n"))
attempt("import the original (top_orig) ", lambda: PythonGenerator(str(c1 / "top_orig.yaml")).serialize())
attempt("import the MERGED mid_merged   ", lambda: PythonGenerator(str(c1 / "top.yaml")).serialize())

# ------------------------------------------------------------------ cases 2 + 3
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(work))
handler.log_message = lambda *a, **k: None  # type: ignore[attr-defined]
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{port}"

for case, sib_import in (("2 (bare sibling import)", "sib"), ("3 (dot-relative sibling import)", "./sib")):
    d = work / ("case2" if case.startswith("2") else "case3")
    # remote/mid.yaml imports its sibling remote/sib.yaml ; root lives elsewhere and imports remote/mid by URL
    w(d / "remote" / "sib.yaml", schema("sib", ["linkml:types"], "classes:\n  Sib:\n    attributes:\n      x: {}\n"))
    w(d / "remote" / "mid.yaml", schema("mid", ["linkml:types", sib_import], "classes:\n  Mid:\n    is_a: Sib\n"))
    w(d / "root" / "root.yaml", schema("root", ["linkml:types", f"{base}/{d.name}/remote/mid"], "classes:\n  Root:\n    is_a: Mid\n"))
    print(f"\nCase {case}: root (local) -> mid (http) -> sibling")
    attempt("SchemaView                      ", lambda: __import__("linkml_runtime").utils.schemaview.SchemaView(str(d / "root" / "root.yaml")).all_classes())
    attempt("PythonGenerator (legacy loader) ", lambda: PythonGenerator(str(d / "root" / "root.yaml")).serialize())

srv.shutdown()
shutil.rmtree(work, ignore_errors=True)
