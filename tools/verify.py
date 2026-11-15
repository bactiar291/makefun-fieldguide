import json
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

import argparse

parser = argparse.ArgumentParser(description='Check the local fieldguide in Chrome and capture its unedited screenshot.')
parser.add_argument('--out', type=Path, help='Directory for QA JSON and mobile screenshots (default: repository output/)')
parser.add_argument('--chrome', default='/usr/bin/google-chrome', help='Chrome or Chromium executable')
args = parser.parse_args()
ROOT = Path(__file__).resolve().parents[1]
OUT = args.out or ROOT / 'output'
OUT.mkdir(parents=True, exist_ok=True)
REF = 'https://make.fun/r/298dam6q'
results = {'created_at': datetime.now(timezone.utc).isoformat(), 'checks': [], 'views': []}
def check(name, passed, detail=None):
    results['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=args.chrome, headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
    context = browser.new_context(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
    page = context.new_page()
    errors, external = [], []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('request', lambda r: external.append(r.url) if r.url.startswith(('http:', 'https:')) else None)
    page.goto(ROOT.joinpath('index.html').as_uri(), wait_until='load')
    check('referral code present', '298dam6q' in page.content())
    check('no incoming referral', 'tvfbjxfd' not in page.content())
    check('one descriptive h1', page.locator('h1').count() == 1)
    check('all referral anchors exact', all(h == REF for h in page.locator('a[href*="/r/"]').evaluate_all('(els) => els.map(e => e.href)')))
    check('primary CTA destination', page.get_by_role('link', name='Open make.fun & sign up').get_attribute('href') == REF)
    context.grant_permissions(['clipboard-read', 'clipboard-write'])
    page.locator('#copy-link').click()
    check('real Chrome clipboard roundtrip', page.evaluate('navigator.clipboard.readText()') == REF)
    page.reload()
    page.mouse.move(0, 0)
    page.evaluate('document.fonts.ready')
    for width, height, filename in [(1440, 1000, 'ad.png'), (390, 844, 'humans-mobile.png'), (320, 800, 'humans-small-mobile.png')]:
        page.set_viewport_size({'width': width, 'height': height})
        page.evaluate('window.scrollTo(0,0)')
        metrics = page.evaluate('''() => {
          const link = document.querySelector('#referral-link').getBoundingClientRect();
          const over = [...document.querySelectorAll('body *')].filter(e => {const r=e.getBoundingClientRect(); return r.width && (r.right > innerWidth+1 || r.left < -1) && !e.classList.contains('skip');}).map(e=>e.tagName+'.'+e.className);
          return {width:innerWidth, scrollWidth:document.documentElement.scrollWidth, link:{top:link.top,bottom:link.bottom,left:link.left,right:link.right}, overflowElements:over, bodyFont:getComputedStyle(document.body).fontSize};
        }''')
        results['views'].append(metrics)
        check(f'{width}px no horizontal overflow', metrics['scrollWidth'] == width and not metrics['overflowElements'], metrics)
        check(f'{width}px referral above fold', 0 <= metrics['link']['top'] and metrics['link']['bottom'] <= height)
        destination = ROOT / filename if filename == 'ad.png' else OUT / filename
        page.screenshot(path=str(destination), full_page=filename != 'ad.png', animations='disabled')
    page.set_viewport_size({'width': 390, 'height': 844})
    page.evaluate("Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{writeText:async (text)=>{window.__copiedText=text}}})")
    page.locator('#copy-link').click()
    check('copy success writes exact link', page.evaluate('window.__copiedText') == REF)
    check('copy success status', 'Link copied' in page.locator('#copy-status').inner_text())
    page.evaluate("Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{writeText:async ()=>{throw new Error('denied')}}})")
    page.locator('#copy-link').click()
    check('permission denied fallback visible', page.locator('#copy-fallback').is_visible())
    check('fallback selected exact link', page.locator('#link-text').evaluate('(e)=>e.value.substring(e.selectionStart,e.selectionEnd)') == REF)
    check('fallback has keyboard focus', page.locator('#link-text').evaluate('(e)=>document.activeElement===e'))
    check('fallback mobile no overflow', page.evaluate('document.documentElement.scrollWidth === innerWidth'))
    page.evaluate("Object.defineProperty(navigator, 'clipboard', {configurable:true, value:undefined})")
    page.locator('#copy-link').click()
    check('missing clipboard fallback visible', page.locator('#copy-fallback').is_visible())
    page.reload()
    page.keyboard.press('Tab')
    check('keyboard skip link first', page.locator('.skip').evaluate('(e)=>e===document.activeElement'))
    check('keyboard focus outline visible', page.locator('.skip').evaluate('(e)=>getComputedStyle(e).outlineStyle') == 'solid')
    page.keyboard.press('Enter')
    check('skip navigates to main', page.url.endswith('#main'))
    page.get_by_role('link', name='How to begin').click()
    check('workflow navigation', page.url.endswith('#workflow'))
    check('no runtime JS errors', not errors, errors)
    check('no external asset requests', not external, external)
    nojs = browser.new_context(java_script_enabled=False, viewport={'width':390,'height':844})
    plain = nojs.new_page()
    plain.goto(ROOT.joinpath('index.html').as_uri())
    check('no JS referral usable', plain.locator('#referral-link').is_visible() and plain.locator('#referral-link').get_attribute('href') == REF)
    check('no JS avoids inert copy button', not plain.locator('#copy-link').is_visible())
    browser.close()

im = Image.open(ROOT / 'ad.png').convert('RGB')
pixels = im.getdata()
background = (246,242,233)
nonpaper = sum(1 for rgb in pixels if rgb != background)
results['screenshot'] = {'path':str(ROOT/'ad.png'),'dimensions':list(im.size),'format':Image.open(ROOT/'ad.png').format,'sha256':sha256((ROOT/'ad.png').read_bytes()).hexdigest(),'bytes':(ROOT/'ad.png').stat().st_size,'nonbackground_pixels':nonpaper,'channel_stddev':ImageStat.Stat(im).stddev}
check('PNG is real 1440x1000 nonblank render', im.size == (1440,1000) and nonpaper > 20000 and min(ImageStat.Stat(im).stddev) > 10)
results['source_sha256'] = sha256((ROOT/'index.html').read_bytes()).hexdigest()
results['passed'] = all(c['passed'] for c in results['checks'])
(OUT/'humans-qa-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
raise SystemExit(0 if results['passed'] else 1)
