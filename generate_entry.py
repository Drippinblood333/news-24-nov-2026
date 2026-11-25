#!/usr/bin/env python3
"""Build entry.png: a one-page 1024x1024 English front page of world news
from Tuesday 24 November 2026. Deterministic: fixed strings, fixed layout,
no randomness, no clock, no network. Any text that does not fit its box
raises an error instead of producing a clipped image."""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 233)
NAVY = (18, 34, 60)
GOLD = (198, 158, 44)
RED = (178, 34, 34)
TEAL = (13, 105, 105)
INK = (32, 32, 32)
BODY_INK = (62, 60, 56)
MUTED = (96, 93, 88)
PANEL = (238, 233, 219)
CARD_EDGE = (202, 197, 188)
NUM_DESC = (198, 203, 212)
PURPLE = (96, 60, 140)
GREEN = (34, 120, 60)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap. Raises if a single word is wider than max_w."""
    lines = []
    for raw in s.split("\n"):
        words = raw.split(" ")
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if text_w(draw, trial, f) <= max_w:
                cur = trial
            else:
                if not cur:
                    raise ValueError("word too wide for box: %r" % word)
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, f, fill, leading):
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=f, fill=fill)
    return y + len(lines) * leading


def fit_or_raise(draw, s, f, max_w, what):
    w = text_w(draw, s, f)
    if w > max_w:
        raise ValueError("%s too wide: %.1f > %.1f (%r)" % (what, w, max_w, s))
    return w


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip -------------------------------------------------------
    d.rectangle([0, 0, W, 30], fill=NAVY)
    bar_f = font(SANS_BOLD, 13)
    left = "THE WORLD IN ONE DAY"
    right = "26 STORIES - 6 REGIONS - ALL FROM THIS ONE DAY"
    fit_or_raise(d, left, bar_f, 400, "top bar left")
    fit_or_raise(d, right, bar_f, 600, "top bar right")
    d.text((24, 8), left, font=bar_f, fill=(255, 255, 255))
    d.text((1000, 8), right, font=bar_f, fill=GOLD, anchor="ra")

    # ---- headline --------------------------------------------------------
    head_f = font(SERIF_BOLD, 57)
    head = "Tuesday 24 November 2026"
    fit_or_raise(d, head, head_f, 976, "headline")
    d.text((24, 42), head, font=head_f, fill=NAVY)

    sub_f = font(SERIF_ITALIC, 20)
    sub = "Four tankers hit mines in Hormuz - Gaza security chief killed - Hanoi blast kills 6"
    fit_or_raise(d, sub, sub_f, 976, "subtitle")
    d.text((24, 110), sub, font=sub_f, fill=RED)

    # ---- region chips ----------------------------------------------------
    chip_f = font(SANS_BOLD, 13)
    chips = [
        ("EUROPE 9", NAVY),
        ("ASIA 6", TEAL),
        ("MIDDLE EAST 5", PURPLE),
        ("AMERICAS 3", RED),
        ("WORLD 2", NAVY),
        ("AFRICA 1", GREEN),
    ]
    chip_w = []
    total = 0
    for label, _ in chips:
        w = text_w(d, label, chip_f) + 22
        chip_w.append(w)
        total += w
    total += 8 * (len(chips) - 1)
    if total > 976:
        raise ValueError("chips too wide: %.1f" % total)
    cx = 24
    cy = 138
    for (label, colour), w in zip(chips, chip_w):
        d.rounded_rectangle([cx, cy, cx + w, cy + 24], radius=12, fill=colour)
        d.text((cx + w / 2, cy + 5), label, font=chip_f, fill=(255, 255, 255),
               anchor="ma")
        cx += w + 8
    d.rectangle([24, 170, 1000, 173], fill=GOLD)

    # ---- lead story ------------------------------------------------------
    lx0, ly0, lx1, ly1 = 24, 178, 628, 400
    d.rectangle([lx0, ly0, lx1, ly1], fill=PANEL, outline=NAVY, width=2)
    d.rectangle([lx0, ly0, lx1, ly0 + 28], fill=RED)
    strip_f = font(SANS_BOLD, 13)
    strip = "1 - STRAIT OF HORMUZ - MIDDLE EAST - ENERGY"
    fit_or_raise(d, strip, strip_f, 500, "lead strip")
    d.text((36, ly0 + 7), strip, font=strip_f, fill=(255, 255, 255))
    badge_f = font(SANS_BOLD, 12)
    bw = text_w(d, "CLAIM", badge_f) + 20
    bx1 = lx1 - 12
    bx0 = bx1 - bw
    d.rounded_rectangle([bx0, ly0 + 5, bx1, ly0 + 23], radius=4, fill=GOLD)
    d.text(((bx0 + bx1) / 2, ly0 + 7), "CLAIM", font=badge_f, fill=NAVY,
           anchor="ma")

    lead_title_f = font(SANS_BOLD, 31)
    title_lines = wrap(d, "Four tankers hit mines in the Strait of Hormuz",
                       lead_title_f, lx1 - 40 - 16)
    if len(title_lines) > 2:
        raise ValueError("lead title needs %d lines" % len(title_lines))
    draw_lines(d, title_lines, 40, ly0 + 38, lead_title_f, NAVY, 37)

    lead_body_f = font(SANS, 15)
    body = ("Iran's IRGC says four tankers struck mines east of the strait, "
            "exploding and catching fire. The claims are unverified, and a US "
            "escort did not stop the attack. The strait is the lifeline of "
            "world oil and gas.")
    body_lines = wrap(d, body, lead_body_f, 430)
    if len(body_lines) > 4:
        raise ValueError("lead body needs %d lines" % len(body_lines))
    draw_lines(d, body_lines, 40, ly0 + 118, lead_body_f, BODY_INK, 19)

    src_f = font(SERIF_ITALIC, 13)
    d.text((40, ly1 - 24), "IRNA - Xinhua - Al Jazeera", font=src_f, fill=MUTED)

    draw_tanker_stamp(d, img)

    # ---- numbers panel ---------------------------------------------------
    px0, py0, px1, py1 = 644, 178, 1000, 400
    d.rectangle([px0, py0, px1, py1], fill=NAVY)
    num_title_f = font(SANS_BOLD, 17)
    d.text((660, 190), "THE DAY IN NUMBERS", font=num_title_f, fill=GOLD)
    rows = [
        ("4", "tankers hit by mines"),
        ("~700", "drones Russia says it downed"),
        ("6", "killed in the Hanoi blast"),
        ("7,000", "landmine casualties, 5-year high"),
        ("$375,000", "top bounty for AI exam cheating"),
        ("~500,000", "reported Russian war dead"),
        ("$3.8bn", "US military aid to Israel"),
        ("2", "arrested in Windsor intrusion"),
    ]
    num_f = font(SANS_BOLD, 17)
    desc_f = font(SANS, 14)
    ry = 220
    for big, small in rows:
        fit_or_raise(d, big, num_f, 130, "number value")
        bw2 = text_w(d, big, num_f)
        fit_or_raise(d, small, desc_f, 992 - (660 + bw2 + 8), "number label")
        d.text((660, ry), big, font=num_f, fill=(255, 255, 255))
        d.text((660 + bw2 + 8, ry + 2), small, font=desc_f, fill=NUM_DESC)
        ry += 22

    # ---- story cards -----------------------------------------------------
    cards = [
        (2, "GAZA CITY", "MIDDLE EAST - WAR", "REPORTED",
         "Israeli strike kills Hamas security chief",
         "Killed Hamas internal security chief Naeem Abu Nahal and six others, "
         "two of them police, as the ceasefire holds.",
         "Reuters - SCMP"),
        (3, "ZAPORIZHZHIA", "EUROPE - WAR", "REPORTED",
         "Russian strike kills 2, wounds 44",
         "An overnight strike hit an apartment block; four children were "
         "among the wounded.",
         "AP - Naharnet"),
        (4, "RIYADH", "MIDDLE EAST - SECURITY", "REPORTED",
         "Riyadh tower hit twice in a week",
         "Saudi Arabia condemned a 'terrorist attack' on the PIF Tower, the "
         "sovereign wealth fund's headquarters.",
         "SCMP - Al Jazeera"),
        (5, "MOSCOW REGION", "EUROPE - WAR", "CLAIM",
         "Russia says it downed ~700 drones",
         "Moscow says it shot down nearly 700 Ukrainian drones overnight, "
         "including over the Moscow region and Crimea.",
         "Naharnet"),
        (6, "SPACE / NATO", "WORLD - DEFENCE", "REPORTED",
         "NATO warns on threats in space",
         "Rutte: NATO will stand up to threats in space, after reports Russia "
         "is preparing to launch a nuclear-armed satellite.",
         "The Global Eye"),
        (7, "HANOI", "ASIA - DISASTER", "REPORTED",
         "Hanoi eatery blast kills 6",
         "A hotpot restaurant blast, suspected to be a gas leak, killed six "
         "and injured more than a dozen.",
         "AP - Naharnet"),
    ]
    cols = [(24, 344), (356, 676), (688, 1000)]
    rows_y = [(406, 578), (586, 758)]
    for i, card in enumerate(cards):
        x0, x1 = cols[i % 3]
        y0, y1 = rows_y[i // 3]
        draw_card(d, x0, y0, x1, y1, *card)

    # ---- also section ----------------------------------------------------
    also_f = font(SANS_BOLD, 16)
    also_title = "ALSO ON TUESDAY 24 NOVEMBER"
    fit_or_raise(d, also_title, also_f, 976, "also title")
    d.text((24, 766), also_title, font=also_f, fill=NAVY)
    d.rectangle([24, 788, 1000, 790], fill=GOLD)
    items = [
        (8, "NORTH KOREA", "threatens to close Swiss office in youth-camp row"),
        (9, "SOUTH KOREA", "jets scramble as Russian jets enter defence zone"),
        (10, "DR CONGO", "fighting traps Ituri Ebola rescue teams"),
        (11, "LANDMINES", "Myanmar, Syria top toll; casualties hit 5-year high"),
        (12, "GERMANY", "first to get access to Ukraine's Delta system"),
        (13, "IRAQ", "PM orders oil ministry to take over Kurdish oilfields"),
        (14, "CHINA", "cobalt firms rush shipments before Congo export ban"),
        (15, "SEOUL", "offers bounty to catch AI cheats in entrance exam"),
        (16, "LONDON", "two arrested over break-in at Prince William's home"),
        (17, "MADRID", "Spain votes Sunday as Sanchez seeks re-election"),
        (18, "WASHINGTON", "envoy doubts Trump will end $3.8bn Israel aid"),
        (19, "SHAANXI", "gas-well fire kills 2, one missing"),
        (20, "WASHINGTON", "Trump awards Giuliani the Medal of Freedom"),
        (21, "SANTA CLARA", "Huang says he is in therapy as Nvidia rally fades"),
        (22, "KYIV", "Ukraine, Libya spar over legality of Benghazi strike"),
        (23, "TEHRAN", "Hormuz stays shut until Iran's demands are met"),
        (24, "BERLIN", "Germans refuse to choose between the US and China"),
        (25, "VATICAN", "late pope's diary says he saw the devil"),
        (26, "BRUSSELS", "seven states back curbs on Russian visas (letter 23 Nov)"),
    ]
    item_b = font(SANS_BOLD, 12)
    item_r = font(SANS, 12)
    left_items = items[:10]
    right_items = items[10:]
    for col_x, col_items in ((24, left_items), (512, right_items)):
        for j, (n, place, text) in enumerate(col_items):
            iy = 794 + j * 16
            head = "%d. %s" % (n, place)
            hw = text_w(d, head, item_b)
            tail = " - " + text
            if hw + text_w(d, tail, item_r) > 488:
                raise ValueError("also item too wide: %d. %s" % (n, place))
            d.text((col_x, iy), head, font=item_b, fill=INK)
            d.text((col_x + hw, iy), tail, font=item_r, fill=INK)

    # ---- date check ------------------------------------------------------
    d.rectangle([24, 962, 1000, 994], outline=RED, width=2)
    dc_b = font(SANS_BOLD, 12)
    dc_r = font(SANS, 12)
    dc_head = "DATE CHECK: "
    dc_rest = ("every story on this page happened, or was first reported, on "
               "Tuesday 24 November 2026. Left out as earlier news: COP31's "
               "close, Megaspeed's blacklisting, Liverpool 4-0 Man Utd and "
               "South Korea's minister quitting.")
    dc_lines = wrap(d, dc_rest, dc_r, 952 - text_w(d, dc_head, dc_b))
    if len(dc_lines) > 2:
        raise ValueError("date check needs %d lines" % len(dc_lines))
    first = dc_head + dc_lines[0]
    d.text((32, 965), dc_head, font=dc_b, fill=RED)
    d.text((32 + text_w(d, dc_head, dc_b), 965), dc_lines[0], font=dc_r,
           fill=INK)
    if len(dc_lines) > 1:
        d.text((32, 980), dc_lines[1], font=dc_r, fill=INK)

    # ---- bottom strip ----------------------------------------------------
    d.rectangle([0, 1000, W, 1024], fill=NAVY)
    bot_f = font(SANS_BOLD, 16)
    bot = "TUESDAY 24 NOVEMBER 2026 - THE WORLD IN ONE IMAGE"
    fit_or_raise(d, bot, bot_f, 1000, "bottom strip")
    d.text((512, 1004), bot, font=bot_f, fill=(255, 255, 255), anchor="ma")

    img.save(OUT_PATH, format="PNG")
    print("wrote %s" % OUT_PATH)


def draw_card(d, x0, y0, x1, y1, num, place, tag, badge, title, body, source):
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=CARD_EDGE,
                width=1)
    d.rectangle([x0, y0, x1, y0 + 4], fill=NAVY)
    head_f = font(SANS_BOLD, 15)
    head = "%d - %s" % (num, place)
    fit_or_raise(d, head, head_f, (x1 - x0) - 90, "card header")
    d.text((x0 + 12, y0 + 10), head, font=head_f, fill=NAVY)
    badge_f = font(SANS_BOLD, 11)
    bg = TEAL if badge == "REPORTED" else GOLD
    fg = (255, 255, 255) if badge == "REPORTED" else NAVY
    bw = text_w(d, badge, badge_f) + 14
    bx1 = x1 - 12
    bx0 = bx1 - bw
    d.rounded_rectangle([bx0, y0 + 11, bx1, y0 + 29], radius=4, fill=bg)
    d.text(((bx0 + bx1) / 2, y0 + 13), badge, font=badge_f, fill=fg, anchor="ma")

    tag_f = font(SANS_BOLD, 12)
    fit_or_raise(d, tag, tag_f, (x1 - x0) - 24, "card tag")
    d.text((x0 + 12, y0 + 32), tag, font=tag_f, fill=RED)

    inner_w = (x1 - x0) - 24
    title_f = font(SANS_BOLD, 18)
    t_lines = wrap(d, title, title_f, inner_w)
    if len(t_lines) > 2:
        raise ValueError("card %d title needs %d lines" % (num, len(t_lines)))
    by = draw_lines(d, t_lines, x0 + 12, y0 + 50, title_f, NAVY, 21) + 4

    body_f = font(SANS, 13)
    b_lines = wrap(d, body, body_f, inner_w)
    if len(b_lines) > 3:
        raise ValueError("card %d body needs %d lines" % (num, len(b_lines)))
    end = draw_lines(d, b_lines, x0 + 12, by, body_f, BODY_INK, 16)
    if end > y1 - 26:
        raise ValueError("card %d body overflows" % num)

    src_f = font(SERIF_ITALIC, 12)
    fit_or_raise(d, source, src_f, inner_w, "card source")
    d.text((x0 + 12, y1 - 22), source, font=src_f, fill=MUTED)


def draw_tanker_stamp(d, img):
    """Small tanker + mines illustration with a rotated red CLAIM stamp,
    drawn into the lead story box (right side, below the title)."""
    ix0, iy0, ix1, iy1 = 478, 296, 614, 388
    # sea
    d.line([ix0, 372, ix1, 372], fill=TEAL, width=2)
    # hull
    d.polygon([(ix0 + 4, 372), (ix1 - 4, 372), (ix1 - 16, 344),
               (ix0 + 16, 344)], fill=NAVY)
    # deck fittings: bridge tower, funnel, mast
    d.rectangle([ix0 + 96, 322, ix0 + 118, 344], fill=NAVY)
    d.rectangle([ix0 + 122, 330, ix0 + 132, 344], fill=RED)
    d.line([ix0 + 30, 344, ix0 + 30, 326], fill=NAVY, width=3)
    d.line([ix0 + 30, 326, ix0 + 44, 332], fill=NAVY, width=2)
    # portholes
    for px in (ix0 + 26, ix0 + 48, ix0 + 70):
        d.ellipse([px, 354, px + 6, 360], fill=GOLD)
    # mines: spiked black circles below the hull line
    for mx, my in ((ix0 + 22, 380), (ix0 + 104, 382)):
        for ang in range(0, 360, 45):
            import math
            rad = math.radians(ang)
            d.line([mx + 7 * math.cos(rad), my + 7 * math.sin(rad),
                    mx + 11 * math.cos(rad), my + 11 * math.sin(rad)],
                   fill=(0, 0, 0), width=2)
        d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(0, 0, 0))
    # rotated CLAIM stamp: small enough to sit over the hull without
    # hiding the bridge tower, the funnel, or the mines below
    stamp = Image.new("RGBA", (96, 30), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    stamp_f = font(SANS_BOLD, 15)
    sd.rounded_rectangle([1, 1, 94, 28], radius=4, outline=RED, width=3)
    sd.text((48, 7), "CLAIM", font=stamp_f, fill=RED, anchor="ma")
    stamp = stamp.rotate(15, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (ix0 + 6, iy0 + 8), stamp)


if __name__ == "__main__":
    main()
