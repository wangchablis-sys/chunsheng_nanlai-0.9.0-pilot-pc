# Draw a side-view metal flashlight for the Wang torch task.
from PIL import Image, ImageDraw, ImageFilter

W, H = 1200, 400


def new_canvas():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def shade_round(box, radius, top, mid, bot):
    x0, y0, x1, y1 = box
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius, fill=255)
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    span = max(1, y1 - y0 - 1)
    for y in range(y0, y1):
        t = (y - y0) / span
        if t < 0.42:
            u = t / 0.42
            col = tuple(int(top[i] * (1 - u) + mid[i] * u) for i in range(3))
        else:
            u = (t - 0.42) / 0.58
            col = tuple(int(mid[i] * (1 - u) + bot[i] * u) for i in range(3))
        gd.line([(x0 - 4, y), (x1 + 4, y)], fill=col + (255,))
    grad.putalpha(mask)
    return grad


def lamp(lit):
    im = new_canvas()
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((180, 318, 1080, 372), fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    im.alpha_composite(shadow)

    if lit:
        beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bd = ImageDraw.Draw(beam)
        bd.polygon([(250, 200), (8, 40), (8, 360)], fill=(255, 214, 90, 70))
        bd.polygon([(250, 200), (20, 90), (20, 310)], fill=(255, 236, 160, 110))
        beam = beam.filter(ImageFilter.GaussianBlur(6))
        im.alpha_composite(beam)

    im.alpha_composite(shade_round((250, 78, 1040, 322), 70, (92, 90, 86), (48, 46, 44), (22, 20, 18)))
    im.alpha_composite(shade_round((150, 48, 390, 352), 90, (120, 116, 108), (62, 58, 54), (28, 24, 22)))

    d = ImageDraw.Draw(im)
    d.ellipse((168, 78, 332, 322), fill=(186, 176, 160, 255))
    d.ellipse((186, 96, 314, 304), fill=(34, 36, 32, 255) if not lit else (255, 236, 170, 255))
    if lit:
        d.ellipse((214, 124, 286, 220), fill=(255, 252, 230, 255))
    else:
        d.ellipse((214, 118, 268, 172), fill=(90, 96, 88, 180))
    d.arc((186, 96, 314, 304), 200, 330, fill=(230, 220, 200, 200), width=3)

    for x in (430, 470, 860, 900):
        d.rounded_rectangle((x, 86, x + 16, 314), radius=4, fill=(28, 26, 24, 255))
        d.line([(x + 3, 100), (x + 3, 300)], fill=(110, 104, 96, 255), width=2)

    im.alpha_composite(shade_round((930, 64, 1140, 336), 36, (140, 132, 118), (78, 72, 64), (36, 32, 28)))
    d = ImageDraw.Draw(im)
    for x in range(960, 1110, 14):
        d.line([(x, 92), (x, 308)], fill=(40, 36, 30, 220), width=3)
        d.line([(x + 4, 92), (x + 4, 308)], fill=(170, 158, 136, 160), width=1)
    d.ellipse((1084, 118, 1168, 282), fill=(150, 140, 122, 255))
    d.ellipse((1100, 136, 1152, 264), fill=(70, 64, 56, 255))

    im.alpha_composite(shade_round((520, 36, 790, 128), 28, (232, 196, 120), (184, 142, 64), (110, 78, 28)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((575, 18, 735, 108), radius=18, fill=(245, 214, 140, 255))
    d.rounded_rectangle((592, 34, 718, 92), radius=12, fill=(120, 78, 28, 255))
    d.line([(654, 46), (654, 80)], fill=(245, 214, 140, 255), width=4)
    d.ellipse((500, 108, 560, 150), fill=(90, 84, 76, 255))
    d.ellipse((760, 108, 820, 150), fill=(90, 84, 76, 255))

    shine = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shine)
    sd.rounded_rectangle((300, 108, 1000, 148), radius=16, fill=(255, 255, 255, 46))
    im.alpha_composite(shine)
    return im


def cell():
    im = Image.new("RGBA", (120, 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((18, 28, 102, 200), radius=16, fill=(196, 168, 92, 255))
    d.rounded_rectangle((28, 40, 92, 188), radius=10, fill=(232, 206, 130, 255))
    d.rounded_rectangle((36, 8, 84, 40), radius=8, fill=(92, 92, 96, 255))
    d.rectangle((52, 14, 68, 28), fill=(210, 210, 214, 255))
    d.line([(34, 70), (86, 70)], fill=(160, 120, 50, 255), width=3)
    d.line([(34, 150), (86, 150)], fill=(160, 120, 50, 255), width=3)
    return im


out = r"C:\Users\Wyf\OneDrive\Desktop\本科课程\课程安排\大二上\毛概\chunsheng_nanlai-0.9.0-pilot-pc\game\gui"
lamp(False).save(out + r"\torch_off.png")
lamp(True).save(out + r"\torch_on.png")
cell().save(out + r"\torch_cell.png")
print("ok")
