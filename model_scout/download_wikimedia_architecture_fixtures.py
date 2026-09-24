"""Download five Wikimedia Commons architecture fixtures with license metadata."""
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).parent / "artifacts" / "public_architecture_fixtures"
API = "https://commons.wikimedia.org/w/api.php?"

def get(params):
    with urlopen(Request(API + urlencode(params), headers={"User-Agent":"MINDLE-Media-AI-Scout/1.0 contact: project-owner"}), timeout=30) as response:
        return json.load(response)

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    search = get({"action":"query","generator":"search","gsrsearch":"architecture filetype:bitmap","gsrnamespace":6,"gsrlimit":12,"prop":"imageinfo","iiprop":"url|extmetadata","format":"json"})
    fixtures = []
    for page in (search.get("query", {}).get("pages", {}) or {}).values():
        info = page.get("imageinfo", [{}])[0]; meta = info.get("extmetadata", {})
        license_name = meta.get("LicenseShortName", {}).get("value", "")
        if not any(token in license_name.lower() for token in ("cc", "public domain", "pd")):
            continue
        path = ROOT / f"{len(fixtures)+1:02d}_{page['pageid']}.jpg"
        try:
            with urlopen(Request(info["url"], headers={"User-Agent":"MINDLE-Media-AI-Scout/1.0"}), timeout=60) as source: path.write_bytes(source.read())
        except Exception:
            continue
        fixtures.append({"file": path.name, "title": page["title"], "source_url": info["descriptionurl"], "license": license_name, "attribution": meta.get("Artist", {}).get("value", "")})
        if len(fixtures) == 5: break
    if len(fixtures) != 5: raise RuntimeError(f"only downloaded {len(fixtures)} licensed fixtures")
    (ROOT / "manifest.json").write_text(json.dumps({"source":"Wikimedia Commons API", "fixtures":fixtures}, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(fixtures, indent=2))

if __name__ == "__main__": main()
