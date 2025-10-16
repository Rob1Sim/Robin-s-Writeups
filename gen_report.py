#!/usr/bin/env python3
"""
gen_report.py 

- Prompts for metadata
- Creates YEAR/MM-MonthName/ROOM_SLUG/
- Creates screenshots/ and exploits/
- Copies ./template.md -> REPORT.md and pre-fills metadata
"""

from __future__ import annotations
import os
import sys
import argparse
import datetime
import unicodedata
import re
import platform

def slugify(value: str) -> str:
    if not value:
        return "untitled"
    value = unicodedata.normalize('NFKD', value)
    value = ''.join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[-\s]+", "-", value.strip()).strip("-").lower()
    return value or "untitled"

def detect_host_os() -> str:
    try:
        p = platform.platform()
        if p and p != "Linux-unknown":
            return p
    except Exception:
        pass
    try:
        if os.path.isfile("/etc/os-release"):
            content = open("/etc/os-release", "r", encoding="utf-8").read()
            m = re.search(r'PRETTY_NAME=(["\']?)(.+?)\1', content)
            if m:
                return m.group(2)
            m_name = re.search(r'^NAME=(["\']?)(.+?)\1', content, re.M)
            m_ver = re.search(r'^VERSION=(["\']?)(.+?)\1', content, re.M)
            if m_name:
                return f"{m_name.group(2)} {m_ver.group(2) if m_ver else ''}".strip()
    except Exception:
        pass
    try:
        return " ".join(platform.uname())
    except Exception:
        return "Unknown OS"

def replace_metadata_in_text(text: str, meta: dict[str, str]) -> str:
    pattern = re.compile(r'^\*\s+\*\*(.+?)\*\*\s*:\s*(.*)$', re.M)
    def repl(m):
        key = m.group(1).strip()
        return f"* **{key}**: {meta.get(key, m.group(2))}"
    return pattern.sub(repl, text)

def ensure_host_os_line(text: str, host_os: str) -> str:
    if re.search(r'(?m)^\*\s+Host OS:', text):
        return re.sub(r'(?m)^\*\s+Host OS:.*$', f"* Host OS: {host_os}", text)
    m = re.search(r'(?m)^(##\s+2\)\s*Environment\s*&\s*Tools.*)$', text)
    if m:
        i = m.end()
        return text[:i] + f"\n* Host OS: {host_os}\n" + text[i:]
    return text + f"\n\n* Host OS: {host_os}\n"

def insert_metadata_section_if_missing(text: str, meta: dict[str, str]) -> str:
    if re.search(r'(?m)^\*\s+\*\*.+\*\*\s*:', text):
        return text
    block = "## Metadata\n\n" + "\n".join(f"* **{k}**: {v}" for k, v in meta.items()) + "\n"
    m = re.search(r'(?m)^(# .+$)', text)
    if m:
        i = m.end()
        return text[:i] + "\n\n" + block + text[i:]
    return block + "\n" + text

def main():
    parser = argparse.ArgumentParser(description="Create a CTF writeup folder and prefill REPORT.md from template.")
    parser.add_argument("--template", "-t", default=os.environ.get("TEMPLATE_PATH", "./template.md"),
                        help="Path to template.md (default: ./template.md)")
    parser.add_argument("--base", "-b", default=os.environ.get("BASE_DIR", "."),
                        help="Base directory for YEAR/MONTH/... (default: current dir)")
    args = parser.parse_args()

    try:
        room = input("Room / Challenge name: ").strip()
        platform_name = input("Platform (THM/HTB/etc.): ").strip()
        iphost = input("IP / Host (optional): ").strip()
        author = input("Author / Handle [R0B1]: ").strip() or "R0b1"
        difficulty = input("Difficulty (Easy/Medium/Hard): ").strip()
        goal = input("Goal (B2R / CTF / Practice): ").strip()
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        sys.exit(1)

    now = datetime.datetime.now()
    year = now.strftime("%Y")
    month_num = now.strftime("%m")
    month_name = now.strftime("%B")
    month_dir = f"{month_num}-{month_name}"
    room_slug = slugify(room or "untitled")

    dest_dir = os.path.join(args.base, year, month_dir, room_slug)
    screenshots_dir = os.path.join(dest_dir, "screenshots")
    exploits_dir = os.path.join(dest_dir, "exploits")
    report_path = os.path.join(dest_dir, "REPORT.md")

    os.makedirs(screenshots_dir, exist_ok=True)
    os.makedirs(exploits_dir, exist_ok=True)

    template_path = args.template
    if not os.path.isfile(template_path):
        print(f"ERROR: Template not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    with open(template_path, "r", encoding="utf-8") as f:
        text = f.read()

    iso_date = now.strftime("%Y-%m-%d")
    meta = {
        "Machine Name": room or "",
        "Platform": platform_name or "",
        "IP / Host": iphost or "",
        "Date": iso_date,
        "Author": author,
        "Difficulty Level": difficulty or "",
        "Goal": goal or "",
    }

    text = replace_metadata_in_text(text, meta)
    text = insert_metadata_section_if_missing(text, meta)
    text = ensure_host_os_line(text, detect_host_os())

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(text)

    # --- Clean, minimal output ---
    print(f"[OK] REPORT ready -> {report_path}")
    print(f"[DIR] screenshots -> {screenshots_dir}")
    print(f"[DIR] exploits    -> {exploits_dir}")

if __name__ == "__main__":
    main()