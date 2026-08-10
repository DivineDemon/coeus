#!/usr/bin/env python3
"""
leadfinder.py — a self-contained Hunter.io replacement.

One file. No external services. Does everything Hunter's core does:
  1. FIND    — scrapes a company's own site for real name/email pairs
  2. PATTERN — infers the company's email naming convention from what it found
  3. GENERATE— builds candidate emails for new names using that pattern
  4. VERIFY  — confirms deliverability via DNS MX + a raw SMTP handshake
               (no email is ever sent)
  5. FLAG    — detects catch-all domains and disposable/throwaway domains

Dependencies (all mature, all free):
    pip install requests beautifulsoup4 dnspython --break-system-packages

Usage:
    python3 leadfinder.py --domain acme.com --names "Jane Smith" "John Doe"
    python3 leadfinder.py --domain acme.com --names "Jane Smith" --json
    python3 leadfinder.py --domain acme.com --names-file names.txt --json

Designed to run standalone in a Hermes `--no-agent` cron job:
    hermes cron create "every 1d" --script leadfinder.py --deliver local
"""

import argparse
import json
import random
import re
import smtplib
import socket
import string
import sys
import time
from collections import Counter
from urllib.parse import urljoin

import dns.resolver
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

USER_AGENT = "Mozilla/5.0 (compatible; leadfinder/1.0; +https://example.com/bot)"
TIMEOUT = 10
COMMON_TEAM_PATHS = [
    "", "about", "about-us", "team", "our-team", "leadership",
    "people", "company", "contact", "meet-the-team", "staff",
]

# A short, high-signal disposable-domain list. Extend this from a maintained
# feed (e.g. github.com/disposable-email-domains/disposable-email-domains)
# if you need broader coverage — it's a static text file, no API required.
DISPOSABLE_DOMAINS = {
    "mailinator.com", "10minutemail.com", "guerrillamail.com",
    "tempmail.com", "yopmail.com", "trashmail.com", "fakeinbox.com",
}

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# ---------------------------------------------------------------------------
# 1. FIND — scrape the company's own site for real name/email pairs
# ---------------------------------------------------------------------------

def fetch(url: str) -> str | None:
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
        if r.status_code == 200:
            return r.text
    except requests.RequestException:
        pass
    return None


def discover_pages(domain: str) -> list[str]:
    base = f"https://{domain}"
    pages = []
    for path in COMMON_TEAM_PATHS:
        url = urljoin(base + "/", path)
        html = fetch(url)
        if html:
            pages.append((url, html))
    return pages


def extract_pairs(pages: list[tuple[str, str]], domain: str) -> list[tuple[str, str]]:
    """Return [(full_name, email), ...] found on the pages, restricted to
    addresses on the target domain (ignore gmail/outlook contact addresses)."""
    pairs = []
    for url, html in pages:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        emails = {e for e in EMAIL_RE.findall(text) if e.lower().endswith("@" + domain.lower())}
        # naive but effective: look at mailto links first, they usually sit
        # right next to a name in markup
        for a in soup.find_all("a", href=True):
            if a["href"].lower().startswith("mailto:"):
                email = a["href"].split(":", 1)[1].split("?")[0].strip()
                if email.lower().endswith("@" + domain.lower()):
                    name = a.get_text(strip=True) or (a.parent.get_text(" ", strip=True) if a.parent else "")
                    name = _clean_name(name)
                    if name:
                        pairs.append((name, email))
                    emails.discard(email)
        # fallback: any leftover emails with no obvious name nearby still count
        # toward pattern-inference even without a name attached
        for email in emails:
            pairs.append(("", email))
    return pairs


def _clean_name(raw: str) -> str:
    raw = re.sub(r"[^A-Za-z\s\-']", "", raw).strip()
    parts = raw.split()
    return " ".join(parts[:2]) if len(parts) >= 2 else ""

# ---------------------------------------------------------------------------
# 2. PATTERN — infer the naming convention from found pairs
# ---------------------------------------------------------------------------

PATTERN_FNS = {
    "first.last":  lambda f, l: f"{f}.{l}",
    "first_last":  lambda f, l: f"{f}_{l}",
    "firstlast":   lambda f, l: f"{f}{l}",
    "flast":       lambda f, l: f"{f[0]}{l}",
    "first.l":     lambda f, l: f"{f}.{l[0]}",
    "first":       lambda f, l: f"{f}",
    "last":        lambda f, l: f"{l}",
    "lfirst":      lambda f, l: f"{l[0]}{f}",
}


def infer_pattern(pairs: list[tuple[str, str]]) -> tuple[str, float]:
    votes = Counter()
    usable = [(n, e) for n, e in pairs if n]
    for name, email in usable:
        local = email.split("@")[0].lower()
        parts = name.lower().split()
        if len(parts) < 2:
            continue
        f, l = parts[0], parts[-1]
        for pname, fn in PATTERN_FNS.items():
            if fn(f, l) == local:
                votes[pname] += 1
                break
    if not votes:
        return "first.last", 0.0  # industry-wide default, low confidence
    best, count = votes.most_common(1)[0]
    confidence = count / max(len(usable), 1)
    return best, round(confidence, 2)

# ---------------------------------------------------------------------------
# 3. GENERATE — build a candidate address for a new name
# ---------------------------------------------------------------------------

def generate_candidate(name: str, domain: str, pattern: str) -> str | None:
    parts = re.sub(r"[^A-Za-z\s\-']", "", name).lower().split()
    if len(parts) < 2:
        return None
    f, l = parts[0], parts[-1]
    fn = PATTERN_FNS.get(pattern, PATTERN_FNS["first.last"])
    return f"{fn(f, l)}@{domain}"

# ---------------------------------------------------------------------------
# 4. VERIFY — DNS MX lookup + raw SMTP handshake (no email sent)
# ---------------------------------------------------------------------------

def get_mx(domain: str) -> str | None:
    try:
        answers = dns.resolver.resolve(domain, "MX")
        return str(sorted(answers, key=lambda r: r.preference)[0].exchange).rstrip(".")
    except Exception:
        return None


def smtp_probe(email: str, mx_host: str, helo_domain: str = "example.com") -> str:
    """Returns one of: 'valid', 'invalid', 'unknown' (greylisted/blocked)."""
    try:
        with smtplib.SMTP(timeout=TIMEOUT) as server:
            server.connect(mx_host, 25)
            server.helo(helo_domain)
            server.mail(f"verify@{helo_domain}")
            code, _ = server.rcpt(email)
            return "valid" if code == 250 else "invalid"
    except (socket.timeout, smtplib.SMTPException, OSError):
        return "unknown"


def is_catch_all(domain: str, mx_host: str) -> bool:
    junk = "".join(random.choices(string.ascii_lowercase, k=20))
    return smtp_probe(f"{junk}@{domain}", mx_host) == "valid"

# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def find_leads(domain: str, names: list[str]) -> dict:
    if domain.lower() in DISPOSABLE_DOMAINS:
        return {"error": f"{domain} is a disposable/throwaway domain, skipping."}

    pages = discover_pages(domain)
    pairs = extract_pairs(pages, domain)
    pattern, pattern_confidence = infer_pattern(pairs)

    mx_host = get_mx(domain)
    if not mx_host:
        return {"error": f"{domain} has no MX record — cannot receive email."}

    catch_all = is_catch_all(domain, mx_host)

    results = []
    for name in names:
        candidate = generate_candidate(name, domain, pattern)
        if not candidate:
            results.append({"name": name, "error": "need first and last name"})
            continue
        time.sleep(1)  # be polite to the mail server, avoid rate-limit blocks
        status = "unknown" if catch_all else smtp_probe(candidate, mx_host)
        results.append({
            "name": name,
            "email": candidate,
            "pattern_used": pattern,
            "pattern_confidence": pattern_confidence,
            "smtp_status": status,
            "catch_all_domain": catch_all,
        })

    return {
        "domain": domain,
        "mx_host": mx_host,
        "catch_all_domain": catch_all,
        "known_pairs_found": len([p for p in pairs if p[0]]),
        "inferred_pattern": pattern,
        "pattern_confidence": pattern_confidence,
        "results": results,
    }

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Self-contained Hunter.io replacement")
    ap.add_argument("--domain", required=True, help="company domain, e.g. acme.com")
    ap.add_argument("--names", nargs="*", default=[], help="full names to find emails for")
    ap.add_argument("--names-file", help="path to a file with one full name per line")
    ap.add_argument("--json", action="store_true", help="output raw JSON")
    args = ap.parse_args()

    names = list(args.names)
    if args.names_file:
        with open(args.names_file) as f:
            names += [line.strip() for line in f if line.strip()]

    if not names:
        print("No names given — running domain analysis only (pattern + catch-all check).")

    output = find_leads(args.domain, names)

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        if "error" in output:
            print(f"Error: {output['error']}")
            sys.exit(1)
        print(f"\nDomain: {output['domain']}")
        print(f"MX host: {output['mx_host']}")
        print(f"Catch-all domain: {output['catch_all_domain']}")
        print(f"Inferred pattern: {output['inferred_pattern']} (confidence: {output['pattern_confidence']})")
        print(f"Known pairs found on site: {output['known_pairs_found']}\n")
        for r in output["results"]:
            if "error" in r:
                print(f"  {r['name']}: {r['error']}")
            else:
                print(f"  {r['name']}: {r['email']}  [{r['smtp_status']}]")


if __name__ == "__main__":
    main()