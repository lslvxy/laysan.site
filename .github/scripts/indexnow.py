import argparse
import csv
import io
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


HOST = "laysan.site"
SITEMAP_URL = f"https://{HOST}/sitemap.xml"
INDEXNOW_URL = "https://www.bing.com/indexnow"
KEY_FILE = Path(__file__).resolve().parents[2] / "static" / "672250591380a3705fb15bdf6d43d3f7.txt"
BATCH_SIZE = 10_000


def get(url):
    return subprocess.check_output(
        ["curl", "--fail", "--silent", "--show-error", "--max-time", "30", url]
    )


def sitemap_urls(xml):
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    root = ET.fromstring(xml)
    if root.tag != namespace + "urlset":
        raise ValueError("Expected a sitemap URL set")

    urls = set()
    for entry in root.findall(f"{namespace}url/{namespace}loc"):
        url = (entry.text or "").strip()
        parts = urlsplit(url)
        if parts.scheme == "https" and parts.netloc == HOST and not parts.fragment:
            urls.add(url)
    if not urls:
        raise ValueError(f"No HTTPS URLs for {HOST} in the sitemap")
    return urls


def changed_urls(base):
    if not re.fullmatch(r"[0-9a-fA-F]{40}", base) or base == "0" * 40:
        raise ValueError("Provide the previous commit's full SHA with --base")
    changed = set(subprocess.check_output(
        ["git", "diff", "--no-renames", "--name-only", "--diff-filter=ACMT", "-z",
         base, "HEAD", "--", "content/"],
        text=True,
    ).rstrip("\0").split("\0")) - {""}
    if not changed:
        return set()

    published = subprocess.check_output(
        ["hugo", "list", "published", "--environment", "production"], text=True
    )
    return {
        row["permalink"]
        for row in csv.DictReader(io.StringIO(published))
        if row["path"] in changed
    }


def submit(urls):
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    key_location = f"https://{HOST}/{KEY_FILE.name}"
    if KEY_FILE.stem != key or get(key_location).decode("utf-8").strip() != key:
        raise ValueError("The public IndexNow key file does not match the local key")

    for start in range(0, len(urls), BATCH_SIZE):
        batch = urls[start:start + BATCH_SIZE]
        payload = json.dumps(
            {"host": HOST, "key": key, "keyLocation": key_location, "urlList": batch}
        ).encode("utf-8")
        code = subprocess.check_output(
            ["curl", "--silent", "--show-error", "--max-time", "30",
             "--output", "/dev/null", "--write-out", "%{http_code}",
             "--header", "Content-Type: application/json; charset=utf-8",
             "--data-binary", "@-", INDEXNOW_URL],
            input=payload,
        ).decode("ascii")
        if code not in {"200", "202"}:
            raise ValueError(f"Bing IndexNow returned HTTP {code}")
        status = "accepted, key verification pending" if code == "202" else "submitted"
        print(f"IndexNow: {len(batch)} URLs {status} (HTTP {code}).")


def main():
    parser = argparse.ArgumentParser(description="Notify Bing about published URLs.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--base", help="Previous commit SHA for incremental submission")
    mode.add_argument("--all", action="store_true", help="Submit all URLs in the live sitemap")
    parser.add_argument("--dry-run", action="store_true", help="List URLs without submitting")
    args = parser.parse_args()

    try:
        candidates = changed_urls(args.base) if not args.all else None
        urls = sitemap_urls(get(SITEMAP_URL)) if candidates is None or candidates else set()
        if candidates is not None:
            urls &= candidates

        if not urls:
            print("No changed URLs in the live sitemap.")
        elif args.dry_run:
            print("\n".join(sorted(urls)))
        else:
            submit(sorted(urls))
    except (OSError, ValueError, ET.ParseError, subprocess.CalledProcessError) as exc:
        print(f"IndexNow failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
