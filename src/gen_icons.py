from PIL import Image, ImageDraw
import os

S = 24
DIR = os.path.join(os.path.dirname(__file__), "icons")
W = (255, 255, 255, 255)

ICONS = {
    "home": lambda d: (
        d.polygon([S//2, 2, 2, S//2+2, S-2, S//2+2], fill=W),
        d.rectangle([4, S//2+2, S-4, S-2], fill=W),
    ),
    "image": lambda d: (
        d.rectangle([2, 4, 22, 20], outline=W, width=2),
        d.polygon([3, 17, 8, 10, 13, 15, 17, 8, 21, 17], fill=W),
        d.ellipse([14, 7, 18, 11], fill=W),
    ),
    "file": lambda d: (
        d.polygon([3, 2, 16, 2, 21, 7, 21, 22, 3, 22], fill=W),
        d.line([7, 8, 17, 8], fill=W, width=2),
        d.line([7, 12, 17, 12], fill=W, width=2),
        d.line([7, 16, 14, 16], fill=W, width=2),
    ),
    "music": lambda d: (
        d.ellipse([4, 15, 11, 22], outline=W, width=2),
        d.ellipse([14, 12, 20, 18], outline=W, width=2),
        d.line([11, 18, 11, 3], fill=W, width=2),
        d.line([11, 3, 20, 5], fill=W, width=2),
    ),
    "folder": lambda d: (
        d.polygon([2, 4, 10, 4, 13, 8, 22, 8, 22, 22, 2, 22], fill=W),
        d.line([4, 6, 9, 6, 12, 10, 20, 10], fill=W, width=2),
        d.polygon([4, 6, 9, 6, 12, 10, 20, 10, 20, 20, 4, 20], fill=(0, 0, 0, 255)),
    ),
    "database": lambda d: (
        d.ellipse([3, 4, 21, 10], outline=W, width=2),
        d.line([3, 7, 3, 20], fill=W, width=2),
        d.line([21, 7, 21, 20], fill=W, width=2),
        d.ellipse([3, 17, 21, 23], outline=W, width=2),
        d.line([3, 20, 3, 17], fill=W, width=2),
        d.line([21, 20, 21, 17], fill=W, width=2),
    ),
    "cog": lambda d: (
        d.ellipse([6, 6, 18, 18], outline=W, width=2),
        d.ellipse([9, 9, 15, 15], fill=W),
        d.line([12, 2, 12, 6], fill=W, width=2),
        d.line([12, 18, 12, 22], fill=W, width=2),
        d.line([2, 12, 6, 12], fill=W, width=2),
        d.line([18, 12, 22, 12], fill=W, width=2),
    ),
    "history": lambda d: (
        d.ellipse([3, 3, 21, 21], outline=W, width=2),
        d.line([12, 6, 12, 13], fill=W, width=2),
        d.line([12, 13, 17, 16], fill=W, width=2),
    ),
    "terminal": lambda d: (
        d.rectangle([2, 4, 22, 20], outline=W, width=2),
        d.line([5, 8, 9, 12, 5, 16], fill=W, width=2),
        d.line([12, 16, 19, 16], fill=W, width=2),
    ),
    "convert": lambda d: (
        d.line([4, 12, 20, 12], fill=W, width=2),
        d.polygon([12, 4, 20, 12, 12, 20], fill=W),
        d.polygon([12, 4, 4, 12, 12, 20], outline=W, width=2),
    ),
    "search": lambda d: (
        d.ellipse([4, 4, 17, 17], outline=W, width=2),
        d.line([14, 14, 22, 22], fill=W, width=2),
    ),
    "plus": lambda d: (
        d.line([12, 4, 12, 20], fill=W, width=2),
        d.line([4, 12, 20, 12], fill=W, width=2),
    ),
    "check": lambda d: (
        d.line([3, 12, 10, 20], fill=W, width=3),
        d.line([10, 20, 22, 4], fill=W, width=3),
    ),
    "cross": lambda d: (
        d.ellipse([2, 2, 22, 22], outline=W, width=2),
        d.line([7, 7, 17, 17], fill=W, width=2),
        d.line([17, 7, 7, 17], fill=W, width=2),
    ),
    "download": lambda d: (
        d.line([12, 3, 12, 17], fill=W, width=2),
        d.polygon([5, 10, 12, 17, 19, 10], fill=W),
        d.line([3, 20, 21, 20], fill=W, width=2),
    ),
    "upload": lambda d: (
        d.line([12, 4, 12, 18], fill=W, width=2),
        d.polygon([5, 11, 12, 4, 19, 11], fill=W),
        d.line([3, 21, 21, 21], fill=W, width=2),
    ),
    "eye": lambda d: (
        d.ellipse([2, 6, 22, 18], outline=W, width=2),
        d.ellipse([8, 9, 16, 15], fill=W),
    ),
    "stop": lambda d: (
        d.rectangle([4, 4, 20, 20], fill=W),
    ),
    "refresh": lambda d: (
        d.arc([3, 3, 21, 21], 20, 160, fill=W, width=2),
        d.polygon([3, 11, 8, 3, 13, 11], fill=W),
        d.line([17, 17, 17, 22], fill=W, width=2),
    ),
    "video": lambda d: (
        d.rectangle([2, 6, 15, 19], outline=W, width=2),
        d.polygon([15, 10, 22, 7, 22, 17, 15, 14], fill=W),
    ),
}

def generate_icons():
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    for name, draw_func in ICONS.items():
        img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        try:
            draw_func(draw)
            fp = os.path.join(DIR, f"{name}.png")
            img.save(fp)
            print(f"  OK {name}")
        except Exception as e:
            print(f"  FAIL {name}: {e}")
    print(f"Total: {len(ICONS)} icons generated in {DIR}")

if __name__ == "__main__":
    generate_icons()
