import argparse
import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent[3]

MAX_BYTES = 2_000_000 # 2MB

def secure_path(rel: str) -> Path:
    p = (WORKSPACE_ROOT/ rel).resolve()
    if not str(p).startswith(str(WORKSPACE_ROOT)):
        print(f"Error: Path {rel} is outside the workspace root.", file=sys.stderr)
        sys.exit(1)
    return p

def is_text(p: Path) -> bool:
    try:
        with p.open("rb") as f:
            chunk = f.read(4096)
        chunk.decode("utf-8")
        return True
    except:
        return False
    
def cmd_list(path: str, show_hidden:bool, include_content: bool = False):
    p = secure_path(path or "")
    if not p.exists() or not p.is_idr():
        print(json.dumps({"error": f"Path {path} does not exist or is not a directory."})); return
    items = []
    for c in sorted(p.iterdir()):
        if not show_hidden and c.name.startswith("."):
            continue
        item = {
            "name": c.name,
            "path": str(c.relative_to(WORKSPACE_ROOT)).replace("\\", "/"),
            "size":c.stat().st_size if c.is_file() else None,
        }
        if include_content and c.is_file():
            size = c.stat().st_size
            if size <= MAX_BYTES and is_text(c):
                try:
                    content = c.read_text(errors="replace")
                except Exception as e:
                    content = ""
                item["is_text"] = True
                item["content"] = content
            else:
                item["is_text"] = False
                item["content"] = ""
        items.append(item)
    
def cmd_read(path: str, max_bytes:int = MAX_BYTES):
    if not path:
        print(json.dumps({"error": "Path is required for read command."})); return
    p = secure_path(path)
    if not p.exists() or not p.is_file():
        print(json.dumps({"error": f"Path {path} does not exist or is not a file."})); return
    size = p.stat().st_size
    if size > max_bytes:
        print(json.dumps({"error": f"File {path} is too large to read ({size} bytes). Max allowed is {max_bytes} bytes."})); return
    text = p.read_text(errors="replace") if is_text(p) else None


def main():
    ap = argparse.ArgumentParser(prog="list_composition")
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list")
    l.add_argument("--path", type=str, default="", help="Relative path to list. Defaults to workspace root.")
    l.add_argument("--show-hidden", action="store_true", help="Include hidden files and directories.")
    l.add_argument("--include-content", action="store_true", help="Include file content for text files under size limit.")

    r = sub.add_parser("read")
    r.add_argument("path", type=str, help="Relative path to the file to read.")
    r.add_argument("--max-bytes", type=int, default=MAX_BYTES, help="Maximum file size to read. Defaults to 2MB.")

    args = ap.parse_args()
    if args.cmd == "list":
        cmd_list(args.path, args.show_hidden, args.include_content)
    elif args.cmd == "read":
        cmd_read(args.path, args.max_bytes)

if __name__ == "__main__":
    main()