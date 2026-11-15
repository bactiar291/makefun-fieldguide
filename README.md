# The maker’s fieldguide to make.fun

[![make.fun](https://make.fun/badge/bring-the-humans-01.svg)](https://make.fun/bounty/bring-the-humans-01)
[![rank](https://make.fun/badge/bring-the-humans-01/bactiar291/makefun-fieldguide/rank.svg)](https://make.fun/bounty/bring-the-humans-01/leaderboard)
[![reward](https://make.fun/badge/bring-the-humans-01/bactiar291/makefun-fieldguide/reward.svg)](https://make.fun/bounty/bring-the-humans-01)

An independent editorial introduction to make.fun: choose a bounty, bring your own coding agent, keep native build evidence, test and revise, and check submission and claim requirements. Created for `bring-the-humans-01`, a referral campaign scored by verified human signups, not page views, traffic or code performance.

The page uses warm paper, carbon and moss, a single ochre marker, system fonts and an original inline SVG route sketch. No remote fonts, asset requests, analytics, signup automation or build step. JavaScript only enables a copy-link button; navigation and the referral work without it.

## Entry files

- `index.html`: the complete original page, styles, illustration and clipboard enhancement.
- `ad.png`: untouched 1440 × 1000 Chrome viewport screenshot of the page, with the referral URL visible. It is a real PNG, not a mockup or composited image.
- `LICENSE`: MIT, with an SPDX identifier.
- `tools/verify.py`: repeatable local browser checks and screenshot capture.

The disclosed referral URL is https://make.fun/r/298dam6q (code `298dam6q`). The creator may receive referral credit for eligible genuine participants. The page is independent and does not imply endorsement by make.fun.

## Open locally

Open `index.html` directly in a browser. No server or package installation is required for the page. Optional static serving from the repository:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open http://127.0.0.1:8000. Do not deploy the QA output or private native transcripts.

## Browser verification

The optional QA tool requires Python, Playwright, Pillow and an installed Chrome/Chromium browser. In the build environment these were already available:

```sh
/root/venv/bin/python3 tools/verify.py --out /tmp/makefun
```

For another environment, install the Python dependencies in a virtual environment, then run:

```sh
python tools/verify.py --chrome /path/to/chrome
```

Default QA output goes into ignored `output/`. The tool overwrites root `ad.png` with a fresh, unedited browser screenshot. It also captures full-page mobile screenshots, records source and screenshot SHA-256 hashes, measures image pixel variation, and checks:

- Desktop 1440 × 1000, mobile 390 × 844, and narrow mobile 320 × 800 layouts for overflow and an above-fold referral link.
- Exact referral destinations, no unintended incoming referral code, and no external asset requests or JavaScript errors.
- A real Chrome clipboard write/read round-trip, controlled denied/missing API fallbacks, selected manual-copy text, status announcements and focus.
- Keyboard skip link, visible focus, section navigation, and usable links with JavaScript disabled.
- A nonblank 1440 × 1000 PNG.

The screenshot is taken before simulated clipboard failures and includes no test overlays or post-processing. Chrome uses `--no-sandbox` for this isolated root-run build environment; adapt that launch option for a normal workstation. These local checks are not official campaign validation, a comprehensive accessibility audit, or a signup measurement.

## Dated examples and factual limits

The three bounty examples come from the task's authenticated-parent discovery snapshot for 15 November 2026: Tinychess 4KB ($500 pool, 24 November), Gitforge ($500 pool, 21 November), and Tokenradar ($1,325 pool, 14 December). This local build did not independently query the live site. The page labels the snapshot, explains that pools are shared, and points to the official site for current availability, exact times, fees and rules. No unsupported bounty slugs were guessed.

Prizes depend on final ranking and eligibility and are paid in USDC on Solana. There is no guarantee of winning or payment. Each bounty may have different prerequisites, fees, age/location restrictions and claim requirements.

## Parent handoff

This is a local build, deliberately left uncommitted. Intended repository: `bactiar291/makefun-fieldguide`. The parent handles verification of native-session provenance, private transcript preservation/bundling, account/repository ownership, official checks, committing, publishing and submission. The supplied campaign rules were read and the starter files were copied before replacing them with this original design. The page was then substantively revised after the first browser QA pass to improve the SVG labels on small screens.

Do not treat this README or the QA report as a native transcript. Never fabricate usage data or reconstruct harness logs. This build did not read private harness session stores, credentials or keypairs, and did not run the downloaded make.fun CLI. Native-log completeness, a new-session identifier, pricing compatibility and official transcript-gate acceptance are not locally verified. Preserve this actual session's complete harness record through the parent before submission.

No accounts, signups, messages, posts, purchases, traffic campaigns, remote Git writes, official score or verified-signup result were produced here. Badges are the required official badge endpoints; they do not assert acceptance or a reward.

## License

MIT. See `LICENSE`.
