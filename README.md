[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Drippinblood333/news-24-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Drippinblood333/news-24-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# The World in One Day — Tuesday 24 November 2026

A single 1024×1024 English front page that fits the whole day's world news
into one image: **26 stories from 6 regions**, all from Tuesday 24 November
2026.

- **Lead story:** four tankers hit mines in the Strait of Hormuz, marked
  CLAIM with a tanker-and-mines illustration and a red CLAIM stamp — the
  claims are unverified.
- **The Day in Numbers:** 8 key figures, from 4 tankers hit by mines to
  ~500,000 reported Russian war dead.
- **Six story cards:** Gaza, Zaporizhzhia, Riyadh, Moscow region, NATO in
  space, and Hanoi — each with a REPORTED / CLAIM badge and its sources.
- **Also on Tuesday 24 November:** 19 one-line briefs, stories 8–26.
- **DATE CHECK:** every story on the page happened, or was first reported,
  on 24 November 2026; earlier news (COP31's close, Megaspeed's
  blacklisting, Liverpool 4-0 Man Utd, South Korea's minister quitting)
  was left out.

## Run it

```sh
python3 generate_entry.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`generate_entry.py` draws `entry.png` with Python + PIL, using only the
system DejaVu and Liberation fonts. `main.ts` copies `entry.png` into the
directory given by `MAKEFUN_OUTPUT_DIR` (default `/output`).

## Verification

- Run `python3 generate_entry.py` twice: the two `entry.png` files have
  identical sha256 hashes (deterministic build — fixed strings, fixed
  layout, no randomness, no clock, no network).
- Output is 1024×1024 PNG, smaller than 1 MiB.
- `MAKEFUN_OUTPUT_DIR=out node main.ts` copies `entry.png` to `out/` with
  an identical hash.
- Visual check of the full image: no overlapping, clipped, or overflowing
  text. The generator raises an error instead of emitting an image if any
  text block exceeds its reserved space.

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
