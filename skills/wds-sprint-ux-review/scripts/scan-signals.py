#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
scan-signals.py — Deterministic UX fidelity signal scanner for wds-sprint-ux-review.

Checks signals 1 (hardcoded hex drift), 2 (missing @reference in scoped styles),
and the file-detection half of signal 3 (new pages in pages/).

Scans only the files that changed in the diff range — not the entire codebase.
Emits JSON to stdout.

Exit codes: 0 = scan complete, 2 = error (git unavailable or fatal).
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HEX_PATTERN = re.compile(r'#[0-9a-fA-F]{3,6}\b')
CSS_VAR_PATTERN = re.compile(r'var\(--color[-\w]*\)')
STYLE_BLOCK_PATTERN = re.compile(r'<style[^>]*>(.*?)</style>', re.DOTALL)
APPLY_PATTERN = re.compile(r'@apply\b')
REFERENCE_PATTERN = re.compile(r'@reference\b')

COMMENT_LINE = re.compile(r'^\s*(//|/\*|\*|<!--)')
SCANNABLE_SUFFIXES = {'.astro', '.ts', '.js', '.css'}


def run_git(args: list[str], cwd: str) -> str:
    result = subprocess.run(
        ['git'] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or f"git exited {result.returncode}")
    return result.stdout


def changed_files(project_root: str, diff_range: str, scan_paths: str) -> list[str]:
    out = run_git(['diff', '--name-only', diff_range, '--', scan_paths], project_root)
    return [f for f in (line.strip() for line in out.splitlines()) if f]


def new_files(project_root: str, diff_range: str, scan_paths: str) -> list[str]:
    out = run_git(['diff', '--name-only', '--diff-filter=A', diff_range, '--', scan_paths], project_root)
    return [f for f in (line.strip() for line in out.splitlines()) if f]


def scan_hex_drift(project_root: str, files: list[str]) -> list[dict]:
    findings = []
    root = Path(project_root)
    for rel in files:
        path = root / rel
        if not path.exists() or path.suffix not in SCANNABLE_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        for i, line in enumerate(content.splitlines(), 1):
            if COMMENT_LINE.match(line):
                continue
            m = HEX_PATTERN.search(line) or CSS_VAR_PATTERN.search(line)
            if m:
                findings.append({'file': rel, 'line': i, 'match': m.group(0)})
    return findings


def scan_missing_reference(project_root: str, files: list[str]) -> list[dict]:
    """Flag .astro files that use @apply inside a <style> block without @reference."""
    findings = []
    root = Path(project_root)
    for rel in files:
        if not rel.endswith('.astro'):
            continue
        path = root / rel
        if not path.exists():
            continue
        try:
            content = path.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        for style_match in STYLE_BLOCK_PATTERN.finditer(content):
            block = style_match.group(1)
            if APPLY_PATTERN.search(block) and not REFERENCE_PATTERN.search(block):
                findings.append({
                    'file': rel,
                    'context': '@apply used without @reference in <style> block',
                })
                break  # one finding per file is enough
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Deterministic UX fidelity signal scanner for wds-sprint-ux-review.',
    )
    parser.add_argument('project_root', help='Absolute path to the project root')
    parser.add_argument('--diff-range', default='HEAD~3..HEAD',
                        help='Git diff range (default: HEAD~3..HEAD)')
    parser.add_argument('--scan-paths', default='src/',
                        help='Path within project root to scan (default: src/)')
    parser.add_argument('-o', '--output', help='Write JSON to this file instead of stdout')
    parser.add_argument('--verbose', action='store_true', help='Progress to stderr')
    args = parser.parse_args()

    project_root = str(Path(args.project_root).resolve())
    scan_paths = args.scan_paths

    if args.verbose:
        print(f"project_root: {project_root}", file=sys.stderr)
        print(f"diff_range:   {args.diff_range}", file=sys.stderr)
        print(f"scan_paths:   {scan_paths}", file=sys.stderr)

    try:
        all_changed = changed_files(project_root, args.diff_range, scan_paths)
        all_new = new_files(project_root, args.diff_range, scan_paths)
    except RuntimeError as exc:
        print(json.dumps({'error': str(exc), 'no_changes': False}), flush=True)
        sys.exit(2)

    if not all_changed:
        result = {
            'scan_range': args.diff_range,
            'no_changes': True,
            'changed_files': [],
            'hex_drift': [],
            'missing_reference': [],
            'new_pages': [],
        }
    else:
        new_pages = [f for f in all_new if '/pages/' in f or f.startswith('pages/')]
        result = {
            'scan_range': args.diff_range,
            'no_changes': False,
            'changed_files': all_changed,
            'hex_drift': scan_hex_drift(project_root, all_changed),
            'missing_reference': scan_missing_reference(project_root, all_changed),
            'new_pages': new_pages,
        }

    payload = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding='utf-8')
    else:
        print(payload, flush=True)


if __name__ == '__main__':
    main()
