from PIL import Image, ImageOps
import os

SOURCE = "static/beyondkaratlogo.png"   # put your original here (copy your 1843x1125 file to this path)
OUT_DIR = "static/icons"
os.makedirs(OUT_DIR, exist_ok=True)

def make_square(im, fill=(255,255,255,0)):
    # Crop center to square then pad if needed
    w, h = im.size
    if w == h:
        square = im
    else:
        # Crop center square
        min_dim = min(w, h)
        left = (w - min_dim)//2
        top = (h - min_dim)//2
        square = im.crop((left, top, left + min_dim, top + min_dim))
    # Ensure alpha channel (RGBA)
    if square.mode != "RGBA":
        square = square.convert("RGBA")
    return square

def save_png(im, size, fname):
    im2 = im.resize((size, size), Image.LANCZOS)
    out_path = os.path.join(OUT_DIR, fname)
    im2.save(out_path, optimize=True)
    print("Saved:", out_path)

def save_favicon(im, sizes, fname="favicon.ico"):
    # Create ICO containing multiple sizes
    icons = [im.resize((s, s), Image.LANCZOS) for s in sizes]
    out_path = os.path.join(OUT_DIR, fname)
    icons[0].save(out_path, format='ICO', sizes=[(s, s) for s in sizes])
    print("Saved:", out_path)

if __name__ == "__main__":
    src = Image.open(SOURCE)
    square = make_square(src)  # crop center → square
    # optionally: add padding/background (already handled by cropping). If you want padding,
    # use ImageOps.pad or create a new RGBA background and paste centered.

    # Save PNGs
    save_png(square, 192, "logo-192.png")
    save_png(square, 512, "logo-512.png")
    save_png(square, 180, "apple-touch-icon.png")

    # Create favicon with typical sizes 16,32,48
    save_favicon(square, sizes=[16,32,48], fname="favicon.ico")
