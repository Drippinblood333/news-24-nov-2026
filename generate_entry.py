#!/usr/bin/env python3
"""Draw a one-image front page of the world news of Tuesday 24 November 2026.

Written for make.fun news-image-20261124 (entry).
Deterministic: fixed strings, fixed layout, no randomness, no clock, no net.
Every text block is fit-checked while drawing: an overflow raises, so the
shipped image can never carry clipped or spilling text.
Run: python3 generate_entry.py   (writes entry.png beside this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 24
CW = W - 2 * MARGIN  # content width = 976

PAPER = (247, 243, 233)
NAVY = (18, 34, 60)
NAVY2 = (30, 54, 90)
RED = (176, 32, 32)
GOLD = (198, 158, 44)
TEAL = (13, 105, 105)
INK = (26, 26, 26)
GREY = (96, 96, 96)
LINE = (203, 195, 176)
WHITE = (255, 255, 255)
PALE = (238, 233, 219)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def F(kind, size):
    name = {
        "serif_b": (FD, "DejaVuSerif-Bold.ttf"),
        "sans_b": (FD, "DejaVuSans-Bold.ttf"),
        "sans": (FD, "DejaVuSans.ttf"),
        "sans_o": (FL, "LiberationSans-Italic.ttf"),
        "serif_i": (FL, "LiberationSerif-Italic.ttf"),
    }[kind]
    return ImageFont.truetype(os.path.join(*name), size)


class Page:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    # -- fit-checked text helpers -------------------------------------
    def wrap(self, text, fnt, max_w):
        lines, cur = [], ""
        for word in text.split():
            trial = (cur + " " + word).strip()
            if self.d.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
                if self.d.textlength(cur, font=fnt) > max_w:
                    raise ValueError("single word too wide: %r" % cur)
        if cur:
            lines.append(cur)
        return lines

    def block(self, x, y, text, fnt, fill, max_w, leading, max_lines):
        lines = self.wrap(text, fnt, max_w)
        if len(lines) > max_lines:
            raise ValueError("block overflow (%d>%d lines): %r"
                             % (len(lines), max_lines, text[:40]))
        for ln in lines:
            self.d.text((x, y), ln, font=fnt, fill=fill)
            y += leading
        return y

    def line(self, x, y, text, fnt, fill, max_w):
        if self.d.textlength(text, font=fnt) > max_w:
            raise ValueError("line too wide: %r" % text[:40])
        self.d.text((x, y), text, font=fnt, fill=fill)

    def badge(self, x, y, text, fill):
        fnt = F("sans_b", 12)
        w = self.d.textlength(text, font=fnt) + 14
        self.d.rounded_rectangle([x, y, x + w, y + 19], radius=3, fill=fill)
        self.d.text((x + 7, y + 3), text, font=fnt, fill=WHITE)
        return w


# ----------------------------------------------------------------------
# Content: every story happened or was first reported on Tue 24 Nov 2026.
# ----------------------------------------------------------------------
NUMBERS = [
    ("4", "tankers hit by mines"),
    ("~700", "drones Russia says it downed"),
    ("6", "killed in the Hanoi blast"),
    ("7,000", "landmine casualties, 5-year high"),
    ("$375,000", "top bounty for AI exam cheating"),
    ("~500,000", "reported Russian war dead"),
    ("$3.8bn", "US military aid to Israel"),
    ("2", "arrested in Windsor intrusion"),
]

CARDS_A = [
    dict(n=2, place="GAZA CITY", tag="MIDDLE EAST - WAR", badge="REPORTED",
         badge_fill=TEAL, head="Israeli strike kills Hamas security chief",
         body="Killed Hamas internal security chief Naeem Abu Nahal and "
              "six others, two of them police, as the ceasefire holds.",
         src="Reuters - SCMP"),
    dict(n=3, place="ZAPORIZHZHIA", tag="EUROPE - WAR", badge="REPORTED",
         badge_fill=TEAL, head="Russian strike kills 2, wounds 44",
         body="An overnight strike hit an apartment block; four children "
              "were among the wounded.",
         src="AP - Naharnet"),
    dict(n=4, place="RIYADH", tag="MIDDLE EAST - SECURITY", badge="REPORTED",
         badge_fill=TEAL, head="Riyadh tower hit twice in a week",
         body="Saudi Arabia condemned a 'terrorist attack' on the PIF "
              "Tower, the sovereign wealth fund's headquarters.",
         src="SCMP - Al Jazeera"),
]

CARDS_B = [
    dict(n=5, place="MOSCOW REGION", tag="EUROPE - WAR", badge="CLAIM",
         badge_fill=GOLD, head="Russia says it downed ~700 drones",
         body="Moscow says it shot down nearly 700 Ukrainian drones "
              "overnight, including over the Moscow region and Crimea.",
         src="Naharnet"),
    dict(n=6, place="SPACE / NATO", tag="WORLD - DEFENCE", badge="REPORTED",
         badge_fill=TEAL, head="NATO warns on threats in space",
         body="Rutte: NATO will stand up to threats in space, after "
              "reports Russia is preparing to launch a nuclear-armed "
              "satellite.",
         src="The Global Eye"),
    dict(n=7, place="HANOI", tag="ASIA - DISASTER", badge="REPORTED",
         badge_fill=TEAL, head="Hanoi eatery blast kills 6",
         body="A hotpot restaurant blast, suspected to be a gas leak, "
              "killed six and injured more than a dozen.",
         src="AP - Naharnet"),
]

ALSO = [
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

REGIONS = [("EUROPE", 9, NAVY2), ("ASIA", 6, TEAL),
           ("MIDDLE EAST", 5, (110, 60, 140)), ("AMERICAS", 3, RED),
           ("WORLD", 2, NAVY), ("AFRICA", 1, (146, 96, 20))]


def draw_header(p):
    d = p.d
    d.rectangle([0, 0, W, 30], fill=NAVY)
    p.line(MARGIN, 7, "THE WORLD IN ONE DAY", F("sans_b", 15), WHITE, 400)
    strap = "26 STORIES  -  6 REGIONS  -  ALL FROM THIS ONE DAY"
    fnt = F("sans_b", 15)
    p.line(W - MARGIN - d.textlength(strap, font=fnt), 7, strap, fnt,
           (240, 205, 110), 500)
    p.line(MARGIN, 40, "Tuesday 24 November 2026", F("serif_b", 57), NAVY, CW)
    p.block(MARGIN, 106,
            "Four tankers hit mines in Hormuz  -  Gaza security chief "
            "killed  -  Hanoi blast kills 6",
            F("serif_i", 20), RED, CW, 24, 1)
    # region chips
    x, y = MARGIN, 138
    for name, count, colour in REGIONS:
        label = "%s %d" % (name, count)
        fnt = F("sans_b", 13)
        w = d.textlength(label, font=fnt) + 18
        d.rounded_rectangle([x, y, x + w, y + 22], radius=4, fill=colour)
        d.text((x + 9, y + 4), label, font=fnt, fill=WHITE)
        x += w + 8
    d.rectangle([MARGIN, 166, W - MARGIN, 169], fill=GOLD)


def draw_lead(p):
    d = p.d
    x0, y0, x1, y1 = MARGIN, 178, 628, 400
    d.rectangle([x0, y0, x1, y1], fill=PALE, outline=NAVY, width=2)
    d.rectangle([x0, y0, x1, y0 + 30], fill=RED)
    p.line(x0 + 14, y0 + 6, "1  -  STRAIT OF HORMUZ  -  MIDDLE EAST - ENERGY",
           F("sans_b", 16), WHITE, x1 - x0 - 28)
    p.badge(x1 - 92, y0 + 42, "CLAIM", GOLD)
    p.block(x0 + 14, y0 + 40, "Four tankers hit mines in the Strait of Hormuz",
            F("sans_b", 30), NAVY, 480, 33, 2)
    y_end = p.block(x0 + 14, y0 + 110,
                    "Iran's IRGC says four tankers struck mines east of "
                    "the strait, exploding and catching fire. The claims "
                    "are unverified, and a US escort did not stop the "
                    "attack. The strait is the lifeline of world oil "
                    "and gas.",
                    F("sans", 14), INK, 400, 18, 5)
    if y_end > y1 - 30:
        raise ValueError("lead body runs into the source line")
    p.line(x0 + 14, y1 - 24, "IRNA - Xinhua - Al Jazeera", F("sans_o", 13),
           GREY, 300)
    # Illustration: tanker silhouette, spiked mines, CLAIM stamp.
    ix, iy = 462, 262
    pic = Image.new("RGBA", (150, 108), (0, 0, 0, 0))
    dd = ImageDraw.Draw(pic)
    # sea
    dd.line([0, 82, 150, 82], fill=NAVY2, width=3)
    dd.line([0, 90, 150, 90], fill=NAVY2, width=2)
    # tanker hull + superstructure
    dd.polygon([(6, 82), (134, 82), (142, 66), (6, 66)], fill=NAVY)
    dd.rectangle([96, 40, 128, 66], fill=NAVY2)
    dd.rectangle([104, 28, 112, 40], fill=RED)
    dd.line([14, 74, 138, 74], fill=(240, 205, 110), width=2)
    # spiked mines
    for cx, cy, r in ((28, 52, 9), (62, 44, 7)):
        for ang in range(0, 360, 45):
            import math
            x2 = cx + int((r + 5) * math.cos(math.radians(ang)))
            y2 = cy + int((r + 5) * math.sin(math.radians(ang)))
            dd.line([cx, cy, x2, y2], fill=INK, width=2)
        dd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
    stamp = Image.new("RGBA", (104, 30), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([2, 2, 102, 28], radius=4, outline=RED, width=3)
    sd.text((52, 15), "CLAIM", font=F("sans_b", 14), fill=RED, anchor="mm")
    pic.alpha_composite(stamp.rotate(12, expand=True), (30, 70))
    p.img.paste(pic, (ix, iy), pic)


def draw_numbers(p):
    d = p.d
    x0, y0, x1, y1 = 644, 178, W - MARGIN, 400
    d.rectangle([x0, y0, x1, y1], fill=NAVY)
    p.line(x0 + 14, y0 + 10, "THE DAY IN NUMBERS", F("sans_b", 16),
           (240, 205, 110), x1 - x0 - 28)
    y = y0 + 42
    for big, label in NUMBERS:
        fnt = F("sans_b", 17)
        if d.textlength(big, font=fnt) > 104:
            fnt = F("sans_b", 14)
        p.line(x0 + 14, y, big, fnt, WHITE, 110)
        bw = d.textlength(big, font=fnt)
        p.block(x0 + 14 + max(bw, 96) + 10, y + 1, label, F("sans", 12.5),
                (226, 230, 238), x1 - x0 - 34 - max(bw, 96), 16, 1)
        y += 22


def draw_card(p, c, x0, y0, x1, y1):
    d = p.d
    d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=LINE, width=1)
    d.rectangle([x0, y0, x1, y0 + 4], fill=NAVY2)
    p.line(x0 + 12, y0 + 12, "%d  %s" % (c["n"], c["place"]),
           F("sans_b", 15), NAVY, x1 - x0 - 110)
    bw = p.badge(x1 - 12 - (len(c["badge"]) * 7 + 16), y0 + 10, c["badge"],
                 c["badge_fill"])
    p.line(x0 + 12, y0 + 34, c["tag"], F("sans_b", 11.5), RED, x1 - x0 - 24)
    y = p.block(x0 + 12, y0 + 50, c["head"], F("sans_b", 18), INK,
                x1 - x0 - 24, 21, 2)
    y_end = p.block(x0 + 12, y + 2, c["body"], F("sans", 13), (52, 52, 52),
                    x1 - x0 - 24, 16.5, 3)
    if y_end > y1 - 24:
        raise ValueError("card body runs into the source line: %r"
                         % c["place"])
    p.line(x0 + 12, y1 - 17, c["src"], F("sans_o", 11.5), GREY,
           x1 - x0 - 24)


def draw_cards(p):
    cols = [(MARGIN, 344), (356, 676), (688, W - MARGIN)]
    for row, cards in ((0, CARDS_A), (1, CARDS_B)):
        y0 = 406 + row * 180
        for (x0, x1), c in zip(cols, cards):
            draw_card(p, c, x0, y0, x1, y0 + 172)


def draw_also(p):
    d = p.d
    y0 = 766
    p.line(MARGIN, y0, "ALSO ON TUESDAY 24 NOVEMBER", F("sans_b", 16), NAVY,
           500)
    d.rectangle([MARGIN, y0 + 22, W - MARGIN, y0 + 24], fill=LINE)
    col_x = [MARGIN, 512]
    col_w = 476
    for i, (n, place, text) in enumerate(ALSO):
        col = 0 if i < 10 else 1
        row = i if i < 10 else i - 10
        x = col_x[col]
        y = y0 + 28 + row * 16.8
        p.line(x, y, "%d." % n, F("sans_b", 12.5), RED, 30)
        fnt = F("sans_b", 12)
        p.line(x + 26, y, place, fnt, NAVY, 150)
        pw = d.textlength(place, font=fnt)
        rest = " - " + text
        if d.textlength(rest, font=F("sans", 12)) > col_w - 26 - pw - 4:
            raise ValueError("also line too wide: %r" % text[:40])
        d.text((x + 26 + pw, y), rest, font=F("sans", 12), fill=INK)


def draw_footer(p):
    d = p.d
    y0 = 962
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + 32], outline=RED, width=2)
    p.block(MARGIN + 10, y0 + 4,
            "DATE CHECK: every story on this page happened, or was first "
            "reported, on Tuesday 24 November 2026. Left out as earlier "
            "news: COP31's close, Megaspeed's blacklisting, Liverpool "
            "4-0 Man Utd and South Korea's minister quitting.",
            F("sans", 12), INK, CW - 20, 13.5, 2)
    d.rectangle([0, 1000, W, H], fill=NAVY)
    txt = "TUESDAY 24 NOVEMBER 2026  -  THE WORLD IN ONE IMAGE"
    fnt = F("sans_b", 16)
    p.line((W - d.textlength(txt, font=fnt)) / 2, 1004, txt, fnt, WHITE, CW)


def main():
    p = Page()
    draw_header(p)
    draw_lead(p)
    draw_numbers(p)
    draw_cards(p)
    draw_also(p)
    draw_footer(p)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    p.img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
