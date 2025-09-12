from PIL import Image, ImageOps
import os

SOURCE = "static/beyondkaratlogo.png"   # your original 1843x1125
OUT_DIR = "static/icons"
os.makedirs(OUT_DIR, exist_ok=True)

def make_square_with_padding(im, fill=(255,255,255,0)):
    w, h = im.size
    size = max(w, h)  # pick the larger dimension
    # pad to square
    new_im = Image.new("RGBA", (size, size), fill)
    new_im.paste(im, ((size - w) // 2, (size - h) // 2))
    return new_im

def save_png(im, size, fname):
    im2 = im.resize((size, size), Image.LANCZOS)
    out_path = os.path.join(OUT_DIR, fname)
    im2.save(out_path, optimize=True)
    print("Saved:", out_path)

def save_favicon(im, sizes, fname="favicon.ico"):
    icons = [im.resize((s, s), Image.LANCZOS) for s in sizes]
    out_path = os.path.join(OUT_DIR, fname)
    icons[0].save(out_path, format='ICO', sizes=[(s, s) for s in sizes])
    print("Saved:", out_path)

if __name__ == "__main__":
    src = Image.open(SOURCE)
    padded = make_square_with_padding(src)

    save_png(padded, 192, "logo-192.png")
    save_png(padded, 512, "logo-512.png")
    save_png(padded, 180, "apple-touch-icon.png")
    save_favicon(padded, sizes=[16, 32, 48], fname="favicon.ico")
