import drawSvg as draw
import requests
import random
import os

w = 1000
h = 1000
r = requests.post("http://colormind.io/api/", json={"model": "default"})
pallet = [
    "#{0:0>2x}{1:0>2x}{2:0>2x}".format(i[0], i[1], i[2]) for i in r.json()["result"]
]

random.shuffle(pallet)


svg = draw.Drawing(w, h)

svg.append(draw.Rectangle(0, 0, w, h, fill=pallet[0]))

for i in range(500):
    c = draw.Circle(
        0,
        0,
        50 + i * 3,
        transform="translate({0}, {1})  rotate({2})".format(
            w / 2, -h / 2, random.randint(1, 360)
        ),
        fill="none",
        stroke=pallet[random.randint(1, len(pallet) - 1)],
        stroke_width=random.randint(2, 32),
        stroke_dasharray=[random.randint(0, 800) for i in range(200)],
    )
    svg.append(c)

    c = draw.Circle(
        0,
        0,
        30 + i * 3,
        fill="none",
        transform="translate({0}, {1})  rotate({2})".format(
            w / 2, -h / 2, random.randint(1, 360)
        ),
        stroke=pallet[random.randint(1, len(pallet) - 1)],
        stroke_width=random.randint(1, 5 + int(i / 3)),
        stroke_dasharray=[
            random.randint(1, 100) if i % 2 == 1 else random.randint(1, 6)
            for i in range(200)
        ],
    )
    svg.append(c)
svg.saveSvg("out.svg")

os.system("inkscape out.svg -o out.png")