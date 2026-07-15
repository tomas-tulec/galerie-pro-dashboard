# Generuje PWA ikony pro Galerie Dashboard — motiv fotomřížky se zaškrtnutým výběrem
from PIL import Image, ImageDraw

GOLD = (212, 160, 23, 255)
GOLD_DIM = (212, 160, 23, 140)
BG = (17, 17, 17, 255)
WHITE = (255, 255, 255, 255)

def draw_icon(size):
    img = Image.new("RGBA", (size, size), BG)
    d = ImageDraw.Draw(img)

    pad = round(size * 0.18)
    gap = round(size * 0.07)
    cell = (size - 2 * pad - gap) / 2
    r = round(cell * 0.14)

    cells = [
        (pad, pad),
        (pad + cell + gap, pad),
        (pad, pad + cell + gap),
        (pad + cell + gap, pad + cell + gap),
    ]

    stroke_w = max(2, round(size * 0.028))

    for i, (x, y) in enumerate(cells):
        box = [x, y, x + cell, y + cell]
        if i == 3:
            # vybraná fotka - plná zlatá s ptáčkem
            d.rounded_rectangle(box, radius=r, fill=GOLD)
            cx, cy = x + cell / 2, y + cell / 2
            s = cell * 0.28
            check = [
                (cx - s, cy),
                (cx - s * 0.3, cy + s * 0.7),
                (cx + s, cy - s * 0.6),
            ]
            d.line(check, fill=BG, width=max(2, round(size * 0.045)), joint="curve")
        else:
            d.rounded_rectangle(box, radius=r, outline=GOLD_DIM, width=stroke_w)
            # naznačení "obrázku" - malé slunce/hory
            cx, cy = x + cell / 2, y + cell * 0.42
            d.ellipse([cx - cell * 0.09, cy - cell * 0.09, cx + cell * 0.09, cy + cell * 0.09], outline=GOLD_DIM, width=max(1, round(size*0.02)))
            m = [
                (x + cell * 0.15, y + cell * 0.78),
                (x + cell * 0.4, y + cell * 0.5),
                (x + cell * 0.58, y + cell * 0.68),
                (x + cell * 0.78, y + cell * 0.42),
                (x + cell * 0.9, y + cell * 0.78),
            ]
            d.line(m, fill=GOLD_DIM, width=max(1, round(size * 0.022)), joint="curve")

    return img

for size, name in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "icon-180.png"), (32, "icon-32.png")]:
    icon = draw_icon(size)
    icon.save(f"C:/Tulec-Claude-Cowork-Projekty/galerie-dashboard/{name}")

print("hotovo")
