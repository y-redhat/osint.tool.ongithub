#!/usr/bin/env python3
import argparse
import subprocess
import tempfile
from pathlib import Path
import json
import sys

def run(cmd, cwd=None):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout

def collect_emails(repo_url: str):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # clone
        run(["git", "clone", "--quiet", repo_url, tmp.as_posix()])

        # git log (author email only)
        log = run(
            ["git", "log", "--pretty=format:%ae"],
            cwd=tmp
        )

        emails = sorted({
            line.strip().lower()
            for line in log.splitlines()
            if "@" in line
        })

        return emails

def main():
    parser = argparse.ArgumentParser(
        description="Collect author emails from a Git repository (git log)."
    )
    parser.add_argument("repo", help="GitHub repository URL")
    parser.add_argument(
        "-o", "--output",
        help="Output file (txt or json)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    try:
        emails = collect_emails(args.repo)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    # output handling
    if args.output:
        path = Path(args.output)

        if args.json or path.suffix == ".json":
            path.write_text(
                json.dumps(emails, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
        else:
            path.write_text("\n".join(emails), encoding="utf-8")
    else:
        for e in emails:
            print(e)

if __name__ == "__main__":
    main()
