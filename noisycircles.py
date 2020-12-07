import drawSvg as draw
import requests
import random
import os
import math
import opensimplex
import time
import utils

w = 1000
h = 1000
r = requests.post("http://colormind.io/api/", json={"model": "default"})
pallet = [
    "#{0:0>2x}{1:0>2x}{2:0>2x}".format(i[0], i[1], i[2]) for i in r.json()["result"]
]

# pallet = ["#424d4f", "#47aa54", "#272d2d", "#f0da7c", "#b4db63"]

random.shuffle(pallet)


svg = draw.Drawing(w, h)

svg.append(draw.Rectangle(0, 0, w, h, fill=pallet[0]))


sn = opensimplex.OpenSimplex()
seed = time.time()
n = 150
transx = random.randint(w * 3 / 5, w)
transy = random.randint(-h * 4 / 5, -h / 5)

for i in range(n):
    rad = 20 + i * 6
    c = pallet[random.randint(1, len(pallet) - 1)]
    d = []
    for j in range(360):
        angle = j / 360 * math.tau
        cos = math.cos(angle)
        sin = math.sin(angle)
        noise = sn.noise3d(cos, sin, seed) * 3 + 2
        r = rad * (1 + noise * ((i / n) ** 3))
        x = cos * r
        y = sin * r * -1
        d.append(("M" if j == 0 else "L") + " {0} {1}".format(x, y))

    if i == 0:
        p = draw.Path(
            d=" ".join(d) + " Z",
            fill=c if i == 0 else "none",
            stroke=c,
            stroke_width=utils.map(i, 20, n, 4, 9, clamped=True),
            stroke_linejoin="round",
            stroke_linecap="round",
            transform="translate({0}, {1})".format(transx, transy),
        )
        svg.append(p)
    else:
        dasharray = " ".join(
            [
                str(
                    utils.randInt(5, i)
                    if j % 2 == 1 and i > 5
                    else (
                        utils.randInt(10, 200)
                        if random.random() < i / n
                        else utils.randInt(4, 10)
                    )
                )
                for j in range(200)
            ]
        )
        p = draw.Path(
            d=" ".join(d) + " Z",
            fill=c if i == 0 else "none",
            stroke=c,
            stroke_width=utils.map(i, 20, n, 4, 9, clamped=True),
            stroke_linejoin="round",
            stroke_linecap="round",
            stroke_dasharray=dasharray,
            transform="translate({0}, {1})".format(transx, transy),
        )
        svg.append(p)

svg.saveSvg("out.svg")

os.system("inkscape out.svg -o out.png")