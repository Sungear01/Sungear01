"""
Pixel-art asset generator for the Sungear01 GitHub profile README.

Every image is drawn from ASCII grids (no external fonts, no raster files),
so it stays razor-sharp at any zoom and loads instantly.
Animations are pure CSS inside each SVG -> they work when GitHub renders <img>.
All motion is disabled for users with "prefers-reduced-motion".

Usage:  python tools/pixel_gen.py      (run from repo root; writes into ./assets)
Edit the DATA section (skills, items, dialog text) and re-run.
"""
import math
import os
import random

random.seed(7)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(os.path.join(ROOT, "px"), exist_ok=True)

# ---------------------------------------------------------------- palette ---
C = {
    "out": "#0d0a1c", "ink": "#1a1530", "n1": "#140f2b", "n2": "#1f1840",
    "n3": "#2b2156", "n4": "#3b2b6e", "mint": "#6fc3b2", "mintL": "#a8ecdc",
    "mintD": "#3f8f84", "blue": "#8aa4e6", "blueD": "#5b74c4", "lav": "#b5a3e0",
    "lavD": "#7d6fc0", "pink": "#ff8fb1", "pinkL": "#ffc2d4", "pinkD": "#d9638a",
    "gold": "#ffd166", "goldD": "#e0a43a", "white": "#f2ecff", "gray": "#a3acbd",
    "red": "#ff6b6b", "orange": "#ff9f43", "brown": "#9c6b4e", "skin": "#ffd9c2",
}

# ------------------------------------------------------------- 5x7 font ----
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": ["....."] * 7,
    ".": [".....", ".....", ".....", ".....", ".....", ".....", "..#.."],
    ",": [".....", ".....", ".....", ".....", ".....", "..#..", ".#..."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    "-": [".....", ".....", ".....", ".###.", ".....", ".....", "....."],
    ":": [".....", "..#..", ".....", ".....", ".....", "..#..", "....."],
    "/": ["....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "'": ["..#..", "..#..", ".....", ".....", ".....", ".....", "....."],
    "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    ">": ["#....", ".#...", "..#..", "...#.", "..#..", ".#...", "#...."],
    "=": [".....", ".....", "#####", ".....", "#####", ".....", "....."],
    "%": ["##..#", "##..#", "...#.", "..#..", ".#...", "#..##", "#..##"],
    "*": [".....", ".#.#.", "#####", "#####", ".###.", "..#..", "....."],  # heart
}


def _run(x, y, w, h):
    return f"M{x} {y}h{w}v{h}h{-w}z"


def text_d(s, x, y, sc):
    d, cx = [], x
    for ch in s.upper():
        for r, row in enumerate(FONT.get(ch, FONT["?"])):
            c = 0
            while c < 5:
                if row[c] == "#":
                    st = c
                    while c < 5 and row[c] == "#":
                        c += 1
                    d.append(_run(cx + st * sc, y + r * sc, (c - st) * sc, sc))
                else:
                    c += 1
        cx += 6 * sc
    return "".join(d)


def tw(s, sc):
    return len(s) * 6 * sc - sc


def text(s, x, y, sc, fill, shadow=None, cls=""):
    out = f'<path fill="{shadow}" d="{text_d(s, x + sc, y + sc, sc)}"/>' if shadow else ""
    out += f'<path fill="{fill}" d="{text_d(s, x, y, sc)}"/>'
    return f'<g class="{cls}">{out}</g>' if cls else out


def sprite(grid, pal, x, y, sc):
    w = max(len(r) for r in grid)
    runs = {}
    for r, row in enumerate(grid):
        row = row.ljust(w, ".")
        c = 0
        while c < w:
            ch, st = row[c], c
            while c < w and row[c] == ch:
                c += 1
            if ch in pal:
                runs.setdefault(ch, []).append(_run(x + st * sc, y + r * sc, (c - st) * sc, sc))
    return "".join(f'<path fill="{pal[k]}" d="{"".join(v)}"/>' for k, v in runs.items())


def size(grid, sc):
    return max(len(r) for r in grid) * sc, len(grid) * sc


def pbox(x, y, w, h, fill, border, inner=None, b=4):
    """JRPG-style window with stepped (pixel-rounded) corners."""
    s = f'<rect x="{x+b}" y="{y+b}" width="{w-2*b}" height="{h-2*b}" fill="{fill}"/>'
    for rx, ry, rw, rh in [(x+b, y, w-2*b, b), (x+b, y+h-b, w-2*b, b), (x, y+b, b, h-2*b),
                           (x+w-b, y+b, b, h-2*b), (x+b, y+b, b, b), (x+w-2*b, y+b, b, b),
                           (x+b, y+h-2*b, b, b), (x+w-2*b, y+h-2*b, b, b)]:
        s += f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" fill="{border}"/>'
    if inner:
        i = 3 * b
        for rx, ry, rw, rh in [(x+i, y+i-2, w-2*i, 2), (x+i, y+h-i, w-2*i, 2),
                               (x+i-2, y+i, 2, h-2*i), (x+w-i, y+i, 2, h-2*i)]:
            s += f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" fill="{inner}"/>'
    return s


BASE_CSS = (
    "@keyframes hop{0%,49%{transform:translateY(0)}50%,100%{transform:translateY(-6px)}}"
    "@keyframes blink{50%{opacity:0}}"
    "@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}"
    ".hop{animation:hop 1.2s linear infinite}"
    ".blink{animation:blink 1s steps(1) infinite}"
)


def svg(name, w, h, body, css="", title=""):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'shape-rendering="crispEdges" role="img" aria-label="{title}"><title>{title}</title>'
           f"<style>{BASE_CSS}{css}"
           "@media (prefers-reduced-motion:reduce){*{animation:none!important}.cover{display:none}}"
           f"</style>{body}</svg>")
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"wrote assets/{name}  ({len(doc)//1024} KB)")


# ================================================================ SPRITES ===
O = C["out"]
HERO = [  # original chibi coder: hoodie + headphones + big anime eyes
    "......kkkk......",
    "....kkhhhhkk....",
    "...khhHHhhhhk...",
    "..khHHhhhhhhhk..",
    ".khhhhhhhhhhhhk.",
    "pkhhhhhhhhhhhhkp",
    "pkhsshhsshhsshkp",
    "pksssssssssssskp",
    "pksweessssweeskp",
    "pkskeesssskeeskp",
    "pksbsssrrsssbskp",
    "..kssssssssssk..",
    "...kksssssskk...",
    "..kvvvkkkkvvvk..",
    ".kvvvvvmmvvvvvk.",
    ".kvvvvvmmvvvvvk.",
    ".kvvvvvvvvvvvvk.",
    "..kkkkkkkkkkkk..",
]
HERO_PAL = {"k": O, "h": "#4a3f7a", "H": C["lavD"], "s": C["skin"], "b": C["pink"],
            "w": C["white"], "e": "#4fd1b8", "r": "#c45a7a", "p": C["pink"], "v": C["lav"],
            "m": C["mint"]}

ICONS = {
    "heart": ([".kk...kk.", "krrk.krrk", "krwrkrrrk", "krrrrrrrk", ".krrrrrk.",
               "..krrrk..", "...krk...", "....k...."], {"k": O, "r": C["pink"], "w": C["white"]}),
    "star": (["....y....", "....y....", "...yyy...", "yyyyWyyyy", "...yyy...",
              "....y....", "....y...."], {"y": C["gold"], "W": C["white"]}),
    "sakura": (["..p.p..", ".pPpPp.", "pPpypPp", ".pyYyp.", "pPpypPp", ".pPpPp.", "..p.p.."],
               {"p": C["pink"], "P": C["pinkL"], "y": C["gold"], "Y": C["white"]}),
    "sword": (["........ww", ".......wWw", "......wWw.", ".....wWw..", "....wWw...",
               ".g.wWw....", "..gWw.....", ".bbg......", "bb..g.....", "b........."],
              {"w": C["white"], "W": C["blue"], "g": C["gold"], "b": C["brown"]}),
    "potion": (["...kk...", "...bb...", "..kwwk..", "..kwwk..", ".kmmmmk.", "kmWmmmmk",
                "kmWmmmmk", "kmmmmmmk", ".kmmmmk.", "..kkkk.."],
               {"k": O, "b": C["brown"], "w": C["white"], "m": C["lav"], "W": C["white"]}),
    "chest": ([".kkkkkkkk.", "kbbbbbbbbk", "kbbbbbbbbk", "kggggggggk", "kbbbggbbbk",
               "kbbbgybbbk", "kbbbbbbbbk", "kkkkkkkkkk"],
              {"k": O, "b": C["brown"], "g": C["gold"], "y": C["white"]}),
    "gamepad": (["..kkkkkkkk..", ".kvvvvvvvvk.", "kvvwvvvvpvvk", "kvwwwvvpvpvk",
                 "kvvwvvvvpvvk", "kvvvkkkkvvvk", ".kkk....kkk."],
                {"k": O, "v": C["blue"], "w": C["white"], "p": C["pink"]}),
    "slime": ([".....kk.....", "....kmmk....", "...kmmmmk...", "..kmWmmmmk..",
               ".kmWmmmmmmk.", "kmmmkmmkmmmk", "kmmmkmmkmmmk", "kmmmmmmmmmmk", ".kkkkkkkkkk."],
              {"k": O, "m": C["mint"], "W": C["mintL"]}),
    "cat": ([".k......k.", "kwk....kwk", "kwwkkkkwwk", "kwwwwwwwwk", "kwkwwwwkwk",
             "kbwwkkwwbk", "kwwwwwwwwk", ".kkkkkkkk."],
            {"k": O, "w": C["white"], "b": C["pink"]}),
    "crystal": (["..kkkk..", ".kWccck.", "kWcccCck", "kcccCcck", ".kccCck.", "..kcck..", "...kk..."],
                {"k": O, "W": C["white"], "c": C["mint"], "C": C["mintD"]}),
    "scroll": ([".kkkkkkkk.", "kYyyyyyyYk", ".kyyyyyyk.", ".kykkkyyk.", ".kyyyyyyk.",
                ".kykkkkyk.", ".kyyyyyyk.", ".kykkyyyk.", "kYyyyyyyYk", ".kkkkkkkk."],
               {"k": O, "y": C["gold"], "Y": C["goldD"]}),
}

# Inventory items (original pixel "loot" that represents each tool — not logos)
ITEM_ART = {
    "flame": ([ "....r.....", "....rr....", "...rrr.r..", "..rrorrr..", ".rrooorrr.",
                ".rroyyorr.", "rrooyyoorr", "rroyyyyorr", ".rroyyorr.", "..rrrrrr.."],
              {"r": C["red"], "o": C["orange"], "y": C["gold"]}),
    "tome": ([".kkkkkkkk.", "kuuuuuuuwk", "kuUUUUuuwk", "kuUuuUuuwk", "kuUUUUuuwk",
              "kuuuuuuuwk", "kuuuuuuuwk", "kuuuuuuuwk", "kwwwwwwwwk", ".kkkkkkkk."],
             {"k": O, "u": C["lavD"], "U": C["pinkL"], "w": C["white"]}),
    "atom": (["..c....c..", "...c..c...", "cccccccccc", "...cCCc...", "..ccCCcc..",
              "...cCCc...", "cccccccccc", "...c..c...", "..c....c.."],
             {"c": "#61dafb", "C": C["white"]}),
    "hexgem": (["...kkkk...", "..kGGggk..", ".kGGggggk.", "kGgggggggk", "kgggggggdk",
                "kggggggddk", ".kggggddk.", "..kgdddk..", "...kkkk..."],
               {"k": O, "G": C["mintL"], "g": "#5fbf6a", "d": "#3b8a45"}),
    "db": (["..kkkkkk..", ".kBBBBBBk.", "kbBBBBBBbk", "kbbbbbbbbk", "kkbbbbbbkk", "kbkkkkkkbk",
            "kbbbbbbbbk", "kkbbbbbbkk", "kbkkkkkkbk", ".kbbbbbbk.", "..kkkkkk.."],
           {"k": O, "b": C["blueD"], "B": C["blue"]}),
    "shield": (["kkkkkkkkkk", "kSSssssssk", "kSsswwsssk", "kssswwsssk", "ksswwwwssk",
                "ksssswwssk", ".ksswwssk.", ".kssssssk.", "..kssssk..", "...kkkk..."],
               {"k": O, "w": C["white"]}),
    "scroll": ICONS["scroll"],
    "crate": (["kkkkkkkkkk", "kBBBBBBBBk", "kBkbbbbkBk", "kbbkbbkbbk", "kbbbkkbbbk",
               "kbbbkkbbbk", "kbbkbbkbbk", "kbkbbbbkbk", "kbbbbbbbbk", "kkkkkkkkkk"],
              {"k": O, "b": "#2f7fd0", "B": "#6fb3f2"}),
    "palette": (["..kkkkkk..", ".knnnnnnk.", "knrnnynnnk", "knnnnnncnk", "knvnnkknnk",
                 "knnnnkknnk", "knpnnnnnnk", ".knnnnnnk.", "..kkkkkk.."],
                {"k": O, "n": "#e8c9a0", "r": C["red"], "y": C["gold"], "c": C["mint"],
                 "v": C["lav"], "p": C["pink"]}),
    "wand": ([".......y..", "......yWy.", "..p....y..", "......b...", ".....b....",
              "....b.....", "...b...p..", "..b.......", ".b........"],
             {"y": C["gold"], "W": C["white"], "b": "#31a8ff", "p": C["pinkL"]}),
    "key": ([".kkk......", "kgGgk.....", "kg.gk.....", "kgggkkkkkk", ".kkkgggggk",
             "....kgkgk.", "....kk.k.."], {"k": O, "g": C["gold"], "G": C["white"]}),
}


def shield_pal(main, light):
    return {**ITEM_ART["shield"][1], "s": main, "S": light}


# =================================================================== DATA ===
NAME = "WITTAWAT"
DIALOG = [
    "HI THERE! I'M WITTAWAT - WEB DEVELOPER",
    "& UI/UX DESIGNER FROM BANGKOK, THAILAND.",
    "I DESIGN IN FIGMA FIRST, THEN BUILD IT",
    "WITH LARAVEL + REACT. PIXEL-PERFECT! *",
]
# (label, value 0-100, bar colour)  -> edit to match your honest self-assessment
SKILLS = [("LARAVEL", 85, C["pink"]), ("PHP", 85, C["lav"]), ("REACT", 70, C["blue"]),
          ("UI/UX", 80, C["mint"]), ("FIGMA", 85, C["pink"]), ("MYSQL", 70, C["blue"]),
          ("DOCKER", 40, C["gold"])]
ITEMS = [  # (label, art key, palette override, rarity border colour)
    ("LARAVEL", "flame", None, C["red"]), ("PHP", "tome", None, C["lav"]),
    ("REACT", "atom", None, C["blue"]), ("NODE.JS", "hexgem", None, C["mint"]),
    ("MYSQL", "db", None, C["blue"]), ("HTML", "shield", shield_pal("#e34f26", "#ff9a73"), C["orange"]),
    ("CSS", "shield", shield_pal("#1572b6", "#6fb3f2"), C["blue"]), ("JS", "scroll", None, C["gold"]),
    ("DOCKER", "crate", None, C["blue"]), ("FIGMA", "palette", None, C["pink"]),
    ("PHOTOSHOP", "wand", None, C["blue"]), ("GIT", "key", None, C["orange"]),
]


# ================================================================= HEADER ===
def header():
    W, H = 1000, 280
    b, css = [], []
    bands = [C["n1"], "#181233", C["n2"], "#251c4b", C["n3"], "#33266a"]
    for i, col in enumerate(bands):
        b.append(f'<rect x="0" y="{i*40}" width="{W}" height="{H}" fill="{col}"/>')
    # twinkling stars
    for i in range(46):
        x, y = random.randrange(0, W, 4), random.randrange(4, 190, 4)
        s = random.choice([2, 2, 4])
        col = random.choice([C["white"], C["mintL"], C["pinkL"], C["gold"]])
        dur, dl = random.uniform(1.4, 3.2), random.uniform(-3, 0)
        b.append(f'<rect class="tw" style="animation:tw {dur:.1f}s steps(3) {dl:.1f}s infinite" '
                 f'x="{x}" y="{y}" width="{s}" height="{s}" fill="{col}"/>')
    # pixel moon with craters
    mx, my, r, cs = 900, 54, 7, 5
    for gy in range(-r, r + 1):
        for gx in range(-r, r + 1):
            if gx * gx + gy * gy <= r * r:
                col = C["pinkL"] if (gx + 2) ** 2 + (gy + 2) ** 2 > 22 else C["white"]
                if (gx - 2, gy - 1) in [(0, 0), (1, 0), (0, 1)] or (gx + 3, gy - 3) == (0, 0):
                    col = C["lav"]
                b.append(f'<rect x="{mx+gx*cs}" y="{my+gy*cs}" width="{cs}" height="{cs}" fill="{col}"/>')
    # shooting star
    css.append("@keyframes shoot{0%{transform:translate(0,0);opacity:0}4%{opacity:1}"
               "14%{transform:translate(-260px,130px);opacity:0}100%{opacity:0}}"
               ".shoot{animation:shoot 7s linear 1s infinite;opacity:0}")
    trail = "".join(f'<rect x="{620+i*6}" y="{20-i*3}" width="4" height="4" fill="{C["white"]}" '
                    f'opacity="{1-i*0.15:.2f}"/>' for i in range(6))
    b.append(f'<g class="shoot">{trail}</g>')
    # far hills + ground
    for x in range(0, W, 8):
        hy = int(205 + 16 * math.sin(x / 85) + 9 * math.sin(x / 31)) // 4 * 4
        b.append(f'<rect x="{x}" y="{hy}" width="8" height="{H-hy}" fill="#2a2058"/>')
    b.append(f'<rect x="0" y="248" width="{W}" height="32" fill="#191233"/>')
    b.append(f'<rect x="0" y="248" width="{W}" height="4" fill="{C["mintD"]}"/>')
    for x in range(0, W, 12):
        if random.random() < .5:
            b.append(f'<rect x="{x}" y="244" width="4" height="4" fill="{C["mintD"]}"/>')
        if random.random() < .12:
            col = random.choice([C["pink"], C["gold"], C["lav"]])
            b.append(f'<rect x="{x}" y="258" width="4" height="4" fill="{col}"/>')
    # title
    b.append(text(NAME, 60, 52, 7, C["white"], shadow=C["pinkD"]))
    sub = "WEB DEVELOPER + UI/UX DESIGNER"
    b.append(text(sub, 62, 124, 3, C["mint"]))
    b.append(sprite(ICONS["heart"][0], ICONS["heart"][1], 62, 160, 2))
    b.append(text("BANGKOK, THAILAND", 88, 162, 2, C["gray"]))
    b.append(f'<g class="blink">{sprite(["k.", "kk", "kkk", "kk", "k."], {"k": C["gold"]}, 62, 200, 3)}'
             f'{text("PRESS START", 80, 200, 2, C["gold"])}</g>')
    # hero + cat
    b.append(f'<g transform="translate(740,140)"><g class="hop">{sprite(HERO, HERO_PAL, 0, 0, 6)}</g></g>')
    b.append(f'<g transform="translate(862,224)"><g class="hop" style="animation-delay:.6s">'
             f'{sprite(ICONS["cat"][0], ICONS["cat"][1], 0, 0, 3)}</g></g>')
    # speech bubble
    css.append("@keyframes talk{0%,8%{opacity:0}10%,80%{opacity:1}82%,100%{opacity:0}}"
               ".talk{animation:talk 5s steps(1) infinite}")
    msg = "HELLO, WORLD!"
    bw = tw(msg, 2) + 24
    b.append(f'<g class="talk">{pbox(560, 84, bw, 34, C["white"], C["out"], b=4)}'
             f'{text(msg, 572, 95, 2, C["ink"])}'
             f'<rect x="{560+bw-28}" y="114" width="8" height="8" fill="{C["white"]}"/>'
             f'<rect x="{560+bw-20}" y="122" width="8" height="6" fill="{C["white"]}"/></g>')
    # falling sakura petals
    css.append("@keyframes fall{from{transform:translate(0,-20px)}to{transform:translate(-180px,300px)}}")
    for i in range(16):
        x = random.randrange(80, W + 120)
        dur, dl = random.uniform(7, 12), random.uniform(-12, 0)
        col = random.choice([C["pink"], C["pinkL"]])
        b.append(f'<g transform="translate({x},0)"><g style="animation:fall {dur:.1f}s linear {dl:.1f}s infinite">'
                 f'{sprite([".p", "pp", "p."], {"p": col}, 0, 0, 3)}</g></g>')
    svg("header.svg", W, H, "".join(b), "".join(css),
        "Pixel night sky banner: Wittawat, Web Developer and UI/UX Designer from Bangkok")


# ================================================================= DIALOG ===
def dialog():
    W, H = 1000, 230
    b, css = [], []
    b.append(pbox(4, 4, W - 8, H - 8, C["ink"], C["white"], inner=C["lav"]))
    b.append(pbox(30, 30, 150, 170, C["n3"], C["lav"]))
    hx, hy, sc = 41, 43, 8
    b.append(sprite(HERO, HERO_PAL, hx, hy, sc))
    # eyelid overlay for blinking
    css.append("@keyframes lid{0%,94%{opacity:0}95%,99%{opacity:1}}.lid{animation:lid 4s steps(1) infinite;opacity:0}")
    lid = ["...sss....sss...", "...kkk....kkk..."]
    b.append(f'<g class="lid">{sprite(lid, {"s": C["skin"], "k": O}, hx, hy + 8 * sc, sc)}</g>')
    # name tag
    b.append(pbox(196, 16, tw(NAME, 2) + 28, 32, C["n3"], C["gold"]))
    b.append(text(NAME, 210, 25, 2, C["gold"]))
    # typed lines
    sc, x0, t = 3, 210, 0.4
    covers = []
    for i, line in enumerate(DIALOG):
        assert len(line) <= 42, f"dialog line too long: {line}"
        y = 66 + i * 36
        b.append(text(line, x0, y, sc, C["white"]))
        w, n = tw(line, sc) + 6, len(line)
        dur = n * 0.045
        covers.append(f'<rect class="cover" style="animation:type {dur:.2f}s steps({n}) {t:.2f}s forwards" '
                      f'x="{x0-3}" y="{y-3}" width="{w}" height="{7*sc+6}" fill="{C["ink"]}" '
                      f'data-w="{w}"/>')
        t += dur + 0.25
    # each cover slides right by its own width; use CSS var-free approach via per-rect keyframes
    b.append('<clipPath id="cl"><rect x="200" y="56" width="780" height="150"/></clipPath>')
    fixed = []
    for i, cv in enumerate(covers):
        w = int(cv.split('data-w="')[1].split('"')[0])
        css.append(f"@keyframes type{i}{{to{{transform:translateX({w}px)}}}}")
        fixed.append(cv.replace("animation:type ", f"animation:type{i} "))
    b.append(f'<g clip-path="url(#cl)">{"".join(fixed)}</g>')
    b.append(f'<g class="blink" style="animation-delay:{t:.1f}s">'
             f'{sprite(["kkkkk", ".kkk.", "..k.."], {"k": C["gold"]}, 950, 196, 3)}</g>')
    svg("dialog.svg", W, H, "".join(b), "".join(css),
        "Dialog box: Hi there! I'm Wittawat, web developer and UI/UX designer from Bangkok, Thailand. "
        "I design in Figma first, then build it with Laravel and React.")


# ================================================================= STATUS ===
def status():
    W = 1000
    H = 84 + len(SKILLS) * 36 + 20
    b, css = [], []
    css.append("@keyframes pop{from{opacity:0}to{opacity:1}}")
    b.append(pbox(4, 4, W - 8, H - 8, C["ink"], C["white"], inner=C["lav"]))
    b.append(text("STATUS", 30, 28, 3, C["gold"], shadow=C["out"]))
    # left: portrait + profile
    b.append(pbox(30, 66, 120, 136, C["n3"], C["lav"]))
    b.append(f'<g transform="translate(42,78)"><g class="hop">{sprite(HERO, HERO_PAL, 0, 0, 6)}</g></g>')
    rows = [("NAME", NAME, C["white"]), ("CLASS", "FULL-STACK MAGE", C["mint"]),
            ("HOME", "BANGKOK, TH", C["white"]), ("QUEST", "OPEN TO WORK", C["pink"])]
    for i, (k, v, col) in enumerate(rows):
        y = 70 + i * 36
        b.append(text(k, 168, y, 2, C["gray"]))
        b.append(text(v, 168, y + 16, 2, col))
    # HP / MP mini bars
    by = 226
    b.append(text("HP", 30, by, 2, C["pink"]))
    b.append(text("MP", 30, by + 30, 2, C["blue"]))
    for i in range(14):
        b.append(f'<rect x="{62+i*16}" y="{by-2}" width="12" height="18" fill="{C["pink"]}"/>')
        b.append(f'<rect x="{62+i*16}" y="{by+28}" width="12" height="18" fill="{C["blue"]}"/>')
    css.append("@keyframes mp{0%,10%{transform:translateX(0)}60%{transform:translateX(-160px)}"
               "70%,100%{transform:translateX(0)}}")
    b.append('<clipPath id="mpc"><rect x="62" y="252" width="224" height="22"/></clipPath>')
    b.append(f'<g clip-path="url(#mpc)"><rect style="animation:mp 6s steps(10) infinite" x="286" '
             f'y="252" width="230" height="22" fill="{C["ink"]}"/></g>')
    b.append(text("HP 999/999", 30, by + 62, 2, C["gray"]))
    b.append(text("MP = COFFEE", 182, by + 62, 2, C["gray"]))
    # divider
    b.append(f'<rect x="372" y="66" width="4" height="{H-96}" fill="{C["n4"]}"/>')
    # right: skill bars
    cells, cw = 20, 18
    for j, (label, val, col) in enumerate(SKILLS):
        y = 70 + j * 36
        b.append(text(label, 400, y + 2, 2, C["white"]))
        filled = round(val / 100 * cells)
        for i in range(cells):
            x = 540 + i * cw
            if i < filled:
                dl = 0.3 + j * 0.15 + i * 0.03
                b.append(f'<rect style="animation:pop .1s steps(1) {dl:.2f}s both" x="{x}" y="{y-2}" '
                         f'width="{cw-4}" height="18" fill="{col}"/>')
                b.append(f'<rect style="animation:pop .1s steps(1) {dl:.2f}s both" x="{x}" y="{y-2}" '
                         f'width="{cw-4}" height="4" fill="{C["white"]}" opacity=".45"/>')
            else:
                b.append(f'<rect x="{x}" y="{y-2}" width="{cw-4}" height="18" fill="{C["n3"]}"/>')
        b.append(text(str(val), 910, y + 2, 2, C["gold"] if val < 50 else C["gray"]))
    svg("status.svg", W, H, "".join(b), "".join(css),
        "Character status screen: skill levels for " + ", ".join(f"{l} {v}" for l, v, _ in SKILLS))


# ============================================================== INVENTORY ===
def inventory():
    cols, sw_, sh, gap, x0, y0 = 6, 140, 132, 12, 50, 74
    rows = math.ceil(len(ITEMS) / cols)
    W, H = 1000, y0 + rows * (sh + gap) + 18
    b, css = [], []
    b.append(pbox(4, 4, W - 8, H - 8, C["ink"], C["white"], inner=C["lav"]))
    b.append(text("INVENTORY", 30, 28, 3, C["gold"], shadow=C["out"]))
    cnt = f"{len(ITEMS)}/{len(ITEMS)} ITEMS"
    b.append(text(cnt, W - 30 - tw(cnt, 2), 32, 2, C["gray"]))
    pos = []
    for i, (label, key, pal, rar) in enumerate(ITEMS):
        cx, cy = x0 + (i % cols) * (sw_ + gap), y0 + (i // cols) * (sh + gap)
        pos.append((cx, cy))
        b.append(pbox(cx, cy, sw_, sh, C["n2"], rar))
        grid, base = ITEM_ART[key]
        p = {**base, **(pal or {})}
        gw, gh = size(grid, 6)
        b.append(f'<g transform="translate({cx+(sw_-gw)//2},{cy+14+(66-gh)//2})">'
                 f'<g class="hop" style="animation-delay:{-i*0.2:.1f}s;animation-duration:1.6s">'
                 f'{sprite(grid, p, 0, 0, 6)}</g></g>')
        b.append(text(label, cx + (sw_ - tw(label, 2)) // 2, cy + 98, 2, C["white"]))
    # moving cursor + highlight
    n, step = len(ITEMS), 100 / len(ITEMS)
    kf = "".join(f"{i*step:.2f}%,{(i+1)*step-0.01:.2f}%{{transform:translate({x-x0}px,{y-y0}px)}}"
                 for i, (x, y) in enumerate(pos))
    css.append(f"@keyframes cur{{{kf}}}.cur{{animation:cur {n*0.9:.1f}s linear infinite}}")
    hl = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{C["gold"]}"/>'
                 for x, y, w, h in [(x0 - 4, y0 - 4, sw_ + 8, 4), (x0 - 4, y0 + sh, sw_ + 8, 4),
                                    (x0 - 4, y0, 4, sh), (x0 + sw_, y0, 4, sh)])
    hand = sprite(["kk....", "kWk...", "kWWk..", "kWWWk.", "kWWk..", "kWk...", "kk...."],
                  {"k": O, "W": C["gold"]}, x0 - 14, y0 + 44, 4)
    b.append(f'<g class="cur">{hl}{hand}</g>')
    svg("inventory.svg", W, H, "".join(b), "".join(css),
        "Tech stack inventory: " + ", ".join(i[0] for i in ITEMS))


# ============================================================== QUEST MAP ===
def questmap():
    W, H = 1000, 330
    b, css = [], []
    b.append(pbox(4, 4, W - 8, H - 8, C["ink"], C["white"], inner=C["lav"]))
    b.append(text("DESIGN QUEST", 30, 28, 3, C["gold"], shadow=C["out"]))
    stages = [("EMPATHIZE", "heart"), ("DEFINE", "crystal"), ("IDEATE", "star"),
              ("PROTOTYPE", "gamepad"), ("TEST", "chest")]
    xs = [100 + i * 200 for i in range(5)]
    ny = 110
    # dotted road
    css.append("@keyframes road{0%,100%{opacity:.25}33%{opacity:1}}")
    for i in range(4):
        for k in range(10):
            x = xs[i] + 52 + k * 10
            b.append(f'<rect style="animation:road 1.2s steps(1) {k*0.12:.2f}s infinite" x="{x}" '
                     f'y="{ny+34}" width="6" height="6" fill="{C["mint"]}"/>')
    for i, (lab, ic) in enumerate(stages):
        x = xs[i] - 44
        b.append(pbox(x, ny - 8, 88, 88, C["n3"], C["lav"] if i < 4 else C["gold"]))
        grid, pal = ICONS[ic]
        gw, gh = size(grid, 5)
        b.append(sprite(grid, pal, xs[i] - gw // 2, ny + 36 - gh // 2, 5))
        b.append(text(f"1-{i+1}", xs[i] - tw("1-1", 2) // 2, ny + 92, 2, C["gray"]))
        b.append(text(lab, xs[i] - tw(lab, 2) // 2, ny + 112, 2, C["white"]))
    # slime walker hopping from stage to stage
    kf = []
    for i in range(5):
        a, z = i * 20, i * 20 + 14
        kf.append(f"{a}%,{z}%{{transform:translate({xs[i]-xs[0]}px,0)}}")
        if i < 4:
            kf.append(f"{z+3}%{{transform:translate({(xs[i]+xs[i+1])//2-xs[0]}px,-22px)}}")
    css.append("@keyframes walk{" + "".join(kf) + "}.walk{animation:walk 8s linear infinite}")
    b.append(f'<g transform="translate({xs[0]-18},{ny-46})"><g class="walk">'
             f'{sprite(ICONS["slime"][0], ICONS["slime"][1], 0, 0, 3)}</g></g>')
    # passive skills (design principles)
    b.append(text("PASSIVE SKILLS", 30, 262, 2, C["gold"]))
    perks = [("CLARITY FIRST", C["mint"]), ("CONSISTENCY", C["blue"]),
             ("ACCESSIBLE", C["lav"]), ("CLEAR FEEDBACK", C["pink"])]
    px = 30
    for lab, col in perks:
        w = tw(lab, 2) + 44
        b.append(pbox(px, 284, w, 30, C["n2"], col))
        b.append(f'<rect x="{px+12}" y="{295}" width="8" height="8" fill="{col}"/>')
        b.append(text(lab, px + 28, 292, 2, C["white"]))
        px += w + 14
    svg("questmap.svg", W, H, "".join(b), "".join(css),
        "Design process quest map: Empathize, Define, Ideate, Prototype, Test. "
        "Principles: clarity first, consistency, accessible, clear feedback.")


# ================================================================= FOOTER ===
def footer():
    W, H = 1000, 190
    b, css = [], []
    for i, col in enumerate(["#33266a", C["n3"], "#251c4b", C["n2"]]):
        b.append(f'<rect x="0" y="{i*36}" width="{W}" height="{H}" fill="{col}"/>')
    for _ in range(24):
        x, y = random.randrange(0, W, 4), random.randrange(4, 110, 4)
        b.append(f'<rect style="animation:tw {random.uniform(1.5,3):.1f}s steps(3) '
                 f'{random.uniform(-3,0):.1f}s infinite" x="{x}" y="{y}" width="2" height="2" '
                 f'fill="{C["white"]}"/>')
    msg = "THANKS FOR STOPPING BY!"
    b.append(text(msg, (W - tw(msg, 4)) // 2, 26, 4, C["white"], shadow=C["pinkD"]))
    m2 = "DESIGN WITH EMPATHY. BUILD WITH CARE."
    b.append(text(m2, (W - tw(m2, 2)) // 2, 70, 2, C["mint"]))
    b.append(text("CONTINUE?", 372, 102, 2, C["gold"]))
    b.append(f'<g class="blink">{sprite(["k.", "kk", "kkk", "kk", "k."], {"k": C["white"]}, 494, 102, 2)}</g>')
    b.append(text("YES", 506, 102, 2, C["white"]))
    b.append(text("NO", 566, 102, 2, C["gray"]))
    b.append(f'<rect x="0" y="150" width="{W}" height="40" fill="#191233"/>')
    b.append(f'<rect x="0" y="150" width="{W}" height="4" fill="{C["mintD"]}"/>')
    for x in range(0, W, 12):
        if random.random() < .5:
            b.append(f'<rect x="{x}" y="146" width="4" height="4" fill="{C["mintD"]}"/>')
        if random.random() < .15:
            col = random.choice([C["pink"], C["gold"], C["lav"]])
            b.append(f'<rect x="{x}" y="164" width="4" height="4" fill="{col}"/>')
    css.append("@keyframes roam{from{transform:translateX(-60px)}to{transform:translateX(1060px)}}")
    for d, ic, s in [(0, "slime", 3), (-6, "slime", 2), (-11, "cat", 3)]:
        grid, pal = ICONS[ic]
        gh = size(grid, s)[1]
        b.append(f'<g transform="translate(0,{150-gh})"><g style="animation:roam 16s linear {d}s infinite">'
                 f'<g class="hop" style="animation-duration:.6s">{sprite(grid, pal, 0, 0, s)}</g></g></g>')
    svg("footer.svg", W, H, "".join(b), "".join(css),
        "Thanks for stopping by! Design with empathy. Build with care.")


# ================================================================== ICONS ===
def small_icons():
    for name, (grid, pal) in ICONS.items():
        sc = 4
        w, h = size(grid, sc)
        pad = 4
        body = f'<g transform="translate({pad},{pad+6})"><g class="hop" style="animation-duration:1.4s">' \
               f'{sprite(grid, pal, 0, 0, sc)}</g></g>'
        svg(f"px/{name}.svg", w + pad * 2, h + pad * 2 + 6, body, "", name)


if __name__ == "__main__":
    header(); dialog(); status(); inventory(); questmap(); footer(); small_icons()
