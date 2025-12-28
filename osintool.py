#!/usr/bin/env python3
import argparse
import subprocess
import tempfile
from pathlib import Path
import json
import sys
import datetime

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

def collect_emails(repo_url, since=None, exclude_noreply=False, domain_only=False):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # clone
        run(["git", "clone", "--quiet", repo_url, tmp.as_posix()])

        # git log
        cmd = ["git", "log", "--pretty=format:%ae"]
        if since:
            cmd.insert(2, f"--since={since}")

        log = run(cmd, cwd=tmp)

        emails = set()
        for line in log.splitlines():
            line = line.strip().lower()
            if "@" not in line:
                continue
            if exclude_noreply and "noreply.github.com" in line:
                continue
            if domain_only:
                line = line.split("@", 1)[1]
            emails.add(line)

        return sorted(emails)

def main():
    parser = argparse.ArgumentParser(
        description="Collect author emails from a Git repository using git log."
    )
    parser.add_argument("repo", help="Git repository clone URL")
    parser.add_argument("-o", "--output", help="Output file (txt or json)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--exclude-noreply", action="store_true",
                        help="Exclude *@users.noreply.github.com")
    parser.add_argument("--domain-only", action="store_true",
                        help="Collect domain part only")
    parser.add_argument("--since", help="Only commits since YYYY-MM-DD")

    args = parser.parse_args()

    if args.since:
        try:
            datetime.datetime.strptime(args.since, "%Y-%m-%d")
        except ValueError:
            print("[ERROR] --since must be YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    try:
        emails = collect_emails(
            args.repo,
            since=args.since,
            exclude_noreply=args.exclude_noreply,
            domain_only=args.domain_only
        )
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

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

