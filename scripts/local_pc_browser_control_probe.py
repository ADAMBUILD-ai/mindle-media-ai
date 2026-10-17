"""PC Work probe using official Chrome directly, independent of window URL discovery.

Development helper only. Requires an existing Playwright Python environment.
Does not start/stop the product server, change its package, or run model inference.
"""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--base-url', required=True)
    ap.add_argument('--evidence-root', type=Path, required=True)
    args = ap.parse_args()
    parsed = urlparse(args.base_url)
    if parsed.scheme != 'http' or parsed.hostname not in {'127.0.0.1', 'localhost'} or parsed.path not in {'', '/'} or parsed.username or parsed.password or parsed.query or parsed.fragment:
        ap.error('Use only the observed local product root URL')
    base = args.base_url.rstrip('/')
    args.evidence_root.mkdir(parents=True, exist_ok=False)
    result = {'status': 'FAIL', 'base_url': base, 'owner_pc_pass': False,
              'full_product_pass': False, 'scope': 'BROWSER_CONTROL_AND_EXISTING_PREVIEW_ONLY'}
    browser = None
    try:
        with urlopen(base + '/api/runtime-identity', timeout=5) as response:
            identity = json.load(response)
        result['runtime_identity'] = identity
        if identity.get('runtime_mode') != 'LOCAL_OFFLINE_PACKAGE':
            raise RuntimeError('Wrong product runtime mode')
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            # Playwright creates an isolated profile and manages its own control channel.
            browser = pw.chromium.launch(channel='chrome', headless=False)
            result['browser_version'] = browser.version
            page = browser.new_page(viewport={'width': 1536, 'height': 1024})
            try:
                result['page_errors'] = []
                page.on('pageerror', lambda error: result['page_errors'].append(str(error)))
                page.goto(base, wait_until='domcontentloaded', timeout=30000)
                page.wait_for_function('() => window.mindleRestoreReady === true', timeout=120000)
                result['actual_url'] = page.url
                result['title'] = page.title()
                result['control'] = 'PASS_DIRECT_OFFICIAL_CHROME_CONNECTION'
                sample = '''v => ({MediaError_code:v.error?.code??null,readyState:v.readyState,
                    videoWidth:v.videoWidth,currentSrc:v.currentSrc,currentTime:v.currentTime,paused:v.paused})'''
                video = page.locator('[data-preview="video"] video')
                if video.count() != 1:
                    raise RuntimeError('No restored video preview; import/save a video then repeat in a new evidence folder')
                result['media_before'] = video.evaluate(sample)
                if not result['media_before']['paused']:
                    video.evaluate('v => v.pause()')
                page.locator('[data-video-play]').click()
                page.wait_for_timeout(1600)
                result['media_after'] = video.evaluate(sample)
                after = result['media_after']
                if after['MediaError_code'] is not None or after['readyState'] < 2 or after['videoWidth'] <= 0 or after['currentTime'] <= result['media_before']['currentTime']:
                    raise RuntimeError('Preview did not advance; inspect recorded media diagnostics')
                video.evaluate('v => v.pause()')
                result['status'] = 'PASS_DIRECT_BROWSER_CONTROL_AND_EXISTING_PREVIEW_PLAYBACK'
            finally:
                try:
                    page.screenshot(path=str(args.evidence_root / 'BROWSER_CONTROL.png'), full_page=True)
                finally:
                    browser.close()
    except Exception as error:
        result['error'] = repr(error)
    finally:
        (args.evidence_root / 'BROWSER_CONTROL_RECEIPT.json').write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
