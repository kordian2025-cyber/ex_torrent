# ex_torrenty.py
# DATE: 2025-10-14
# VERSION: 3.3
# AUTHOR: KordianJ (5c0rp10n)
# CO-AUTHOR: powerzasty
# THANKS: ex-torrenty.pl
# LICENSE: GPLv3+


import json
import tempfile
import sys
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from novaprinter import prettyPrinter


class ex_torrenty(object):
    url = "https://ex-torrenty.org/"
    name = "EX-Torrenty"
    supported_categories = {"all": "all"}

    API_BASE = "https://ex-torrenty.org/api/qt/torrents"
    PER_PAGE = 50

    # ⚠️ Provide your own session data (after logging in through browser)
    COOKIES = {
        "uid": "xxxxxx",
        "pass": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "hashv": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "PHPSESSID": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/141.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://ex-torrenty.org/",
    }

    # ==========================================
    # Helper methods
    # ==========================================
    def _cookie_str(self):
        """Combine cookies into a single header"""
        return "; ".join([f"{k}={v}" for k, v in self.COOKIES.items()])

    def _fetch_json(self, url):
        """Fetch JSON from API using urllib"""
        headers = self.HEADERS.copy()
        headers["Cookie"] = self._cookie_str()
        req = Request(url, headers=headers)
        with urlopen(req) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)

    def _human_size(self, size_bytes):
        """Convert bytes to human-readable format"""
        try:
            size_bytes = int(size_bytes)
        except:
            return str(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    # ==========================================
    # Main search method
    # ==========================================
    def search(self, what, cat="all"):
        """Search torrents via API and print results"""
        page = 1
        per_page = self.PER_PAGE
        sort = "seeders_desc"

        while True:
            # Fix: multi-word search query is not encoded
            search_url = f"{self.API_BASE}?q={what}&page={page}&per_page={per_page}&sort={sort}"

            try:
                js = self._fetch_json(search_url)
            except Exception as e:
                prettyPrinter({
                    "link": "",
                    "name": f"[ERROR] {e}",
                    "size": "-1",
                    "seeds": "0",
                    "leech": "0",
                    "engine_url": self.url,
                    "desc_link": ""
                })
                break

            # Handle API errors
            if "error" in js:
                code = js.get("code", "???")
                msg = js.get("error", "Unknown error")
                prettyPrinter({
                    "link": "",
                    "name": f"[ERROR {code}] {msg}",
                    "size": "-1",
                    "seeds": "0",
                    "leech": "0",
                    "engine_url": self.url,
                    "desc_link": ""
                })
                break

            results = js.get("results", [])
            if not results:
                prettyPrinter({
                    "link": "",
                    "name": "No results found",
                    "size": "-1",
                    "seeds": "0",
                    "leech": "0",
                    "engine_url": self.url,
                    "desc_link": ""
                })
                break

            for r in results:
                name = r.get("name", "unknown")
                size = self._human_size(r.get("size", 0))
                seeds = str(r.get("seeds", "0"))
                leech = str(r.get("leech", "0"))
                desc_link = urljoin(self.url, r.get("desc_link", ""))
                download_url = urljoin(self.url, r.get("link", ""))

                prettyPrinter({
                    "link": download_url,
                    "name": name,
                    "size": size,
                    "seeds": seeds,
                    "leech": leech,
                    "engine_url": self.url,
                    "desc_link": desc_link
                })

            total = js.get("total", len(results))
            per_page_ret = js.get("per_page", per_page)
            current_page = js.get("page", page)

            if total and current_page * per_page_ret < total:
                page += 1
            else:
                break

    # ==========================================
    # Download .torrent (with cookies)
    # ==========================================
    def download_torrent(self, info):
        """Download .torrent from API with authorization (cookies)"""
        url = info["link"] if isinstance(info, dict) else info
        if not url or url.startswith("magnet:"):
            return

        headers = self.HEADERS.copy()
        headers["Cookie"] = self._cookie_str()
        req = Request(url, headers=headers)

        try:
            with urlopen(req) as resp:
                status = resp.status
                if status == 429:
                    print("[ex-torrenty] Daily download limit reached (50).", file=sys.stderr)
                    return
                elif status == 403:
                    print("[ex-torrenty] Authorization error — check your cookies.", file=sys.stderr)
                    return
                elif status == 404:
                    print("[ex-torrenty] Torrent does not exist or access denied (404).", file=sys.stderr)
                    return
                elif status != 200:
                    print(f"[ex-torrenty] HTTP {status} — failed to download torrent.", file=sys.stderr)
                    return

                data = resp.read()

            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".torrent")
            tmp_file.write(data)
            tmp_file.close()
            print(f"{tmp_file.name} {url}")

        except Exception as e:
            print(f"[ex-torrenty] Torrent download error: {e}", file=sys.stderr)
# To testing !
#       except Exception as e:
#           pass

# ==========================================
# Local test
# ==========================================
if __name__ == "__main__":
    engine = ex_torrenty()

    # 🔍 Test search
    query = "ubuntu"
    print(f"Searching torrents for: {query}")
    engine.search(query)

    # Download the first search result and save the link
    first_link = None
    try:
        search_url = f"{engine.API_BASE}?q={query}&page=1&per_page=1&sort=seeders_desc"
        js = engine._fetch_json(search_url)
        if js.get("results"):
            first_result = js["results"][0]
            first_link = urljoin(engine.url, first_result.get("link", ""))
            print(f"First torrent: {first_result.get('name')}")
        else:
            print("❌ No results for the given query.")
    except Exception as e:
        print(f"[ex-torrenty] Error fetching first result: {e}", file=sys.stderr)

    # 💾 Test downloading torrent from search result
    if first_link:
        print("\nDownloading first torrent from search results:")
        engine.download_torrent(first_link)
    else:
        print("❌ Failed to obtain first torrent link.")
