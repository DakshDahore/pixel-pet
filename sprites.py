import math
from PIL import Image, ImageDraw, ImageTk

CANVAS_SIZE = 96
SCALE = 2

PALETTE = {
    "outline": (18, 17, 26, 255),
    "fur_main": (35, 34, 45, 255),
    "fur_shadow": (26, 25, 36, 255),
    "fur_light": (53, 52, 68, 255),
    "ear_inner": (244, 114, 182, 255),
    "ear_inner_shadow": (219, 39, 119, 255),
    "blush": (253, 164, 175, 180),
    "eye_white": (255, 255, 255, 255),
    "eye_color_top": (34, 197, 94, 255),
    "eye_color_bot": (250, 204, 21, 255),
    "pupil": (15, 23, 42, 255),
    "sparkle": (255, 255, 255, 255),
    "nose": (251, 113, 133, 255),
    "mouth": (180, 50, 80, 255),
    "collar": (239, 68, 68, 255),
    "bell": (250, 204, 21, 255),
    "scratch": (255, 255, 255, 230),
    "tear": (96, 165, 250, 255),
    "heart": (244, 63, 94, 255),
    "transparent": (0, 0, 0, 0)
}

def create_base_canvas():
    return Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), PALETTE["transparent"])

def draw_ears(draw, mode="normal", ear_twitch=0):
    p = PALETTE
    if mode == "turned":
        draw.polygon([(26, 12), (38, 30), (20, 32)], fill=p["fur_main"], outline=p["outline"])
        draw.polygon([(70, 12), (76, 32), (58, 30)], fill=p["fur_main"], outline=p["outline"])
        return

    if mode == "angry":
        draw.polygon([(16, 26), (36, 32), (24, 38)], fill=p["fur_main"], outline=p["outline"])
        draw.polygon([(80, 26), (72, 38), (60, 32)], fill=p["fur_main"], outline=p["outline"])
        draw.polygon([(19, 28), (33, 33), (25, 36)], fill=p["ear_inner"])
        draw.polygon([(77, 28), (70, 36), (63, 33)], fill=p["ear_inner"])
        return

    if mode == "sad":
        draw.polygon([(18, 22), (36, 30), (22, 36)], fill=p["fur_main"], outline=p["outline"])
        draw.polygon([(78, 22), (74, 36), (60, 30)], fill=p["fur_main"], outline=p["outline"])
        draw.polygon([(21, 24), (33, 31), (24, 34)], fill=p["ear_inner"])
        draw.polygon([(75, 24), (72, 34), (63, 31)], fill=p["ear_inner"])
        return

    left_tip_x = 24 + ear_twitch
    left_tip_y = 10
    right_tip_x = 72 - ear_twitch
    right_tip_y = 10

    draw.polygon([(left_tip_x, left_tip_y), (38, 28), (20, 30)], fill=p["fur_main"], outline=p["outline"])
    draw.polygon([(left_tip_x + 3, left_tip_y + 4), (35, 27), (23, 28)], fill=p["ear_inner"])

    draw.polygon([(right_tip_x, right_tip_y), (76, 30), (58, 28)], fill=p["fur_main"], outline=p["outline"])
    draw.polygon([(right_tip_x - 3, right_tip_y + 4), (73, 28), (61, 27)], fill=p["ear_inner"])

def draw_head_shape(draw, head_y=26, mode="normal"):
    p = PALETTE
    draw.ellipse([22, head_y, 74, head_y + 36], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([26, head_y + 3, 70, head_y + 34], fill=p["fur_main"])

    draw.polygon([(23, head_y + 18), (17, head_y + 22), (23, head_y + 25)], fill=p["fur_main"])
    draw.polygon([(73, head_y + 18), (79, head_y + 22), (73, head_y + 25)], fill=p["fur_main"])

def draw_eyes(draw, head_y=26, mode="normal", blink=False):
    p = PALETTE
    if mode == "turned":
        return

    if blink or mode == "sleeping":
        draw.arc([32, head_y + 16, 44, head_y + 22], start=180, end=360, fill=p["outline"], width=2)
        draw.arc([52, head_y + 16, 64, head_y + 22], start=180, end=360, fill=p["outline"], width=2)
        return

    if mode == "petted" or mode == "happy":
        draw.arc([32, head_y + 12, 44, head_y + 20], start=0, end=180, fill=p["outline"], width=2)
        draw.arc([52, head_y + 12, 64, head_y + 20], start=0, end=180, fill=p["outline"], width=2)
        draw.ellipse([28, head_y + 20, 34, head_y + 24], fill=p["blush"])
        draw.ellipse([62, head_y + 20, 68, head_y + 24], fill=p["blush"])
        return

    if mode == "frightened":
        draw.ellipse([31, head_y + 8, 45, head_y + 24], fill=p["eye_white"], outline=p["outline"])
        draw.ellipse([51, head_y + 8, 65, head_y + 24], fill=p["eye_white"], outline=p["outline"])
        draw.ellipse([36, head_y + 14, 40, head_y + 18], fill=p["pupil"])
        draw.ellipse([56, head_y + 14, 60, head_y + 18], fill=p["pupil"])
        return

    draw.ellipse([31, head_y + 10, 45, head_y + 24], fill=p["eye_white"], outline=p["outline"])
    draw.ellipse([51, head_y + 10, 65, head_y + 24], fill=p["eye_white"], outline=p["outline"])

    draw.ellipse([33, head_y + 11, 43, head_y + 23], fill=p["eye_color_top"])
    draw.ellipse([53, head_y + 11, 63, head_y + 23], fill=p["eye_color_top"])
    draw.chord([33, head_y + 16, 43, head_y + 23], start=0, end=180, fill=p["eye_color_bot"])
    draw.chord([53, head_y + 16, 63, head_y + 23], start=0, end=180, fill=p["eye_color_bot"])

    if mode == "angry":
        draw.ellipse([35, head_y + 12, 41, head_y + 22], fill=p["pupil"])
        draw.ellipse([55, head_y + 12, 61, head_y + 22], fill=p["pupil"])
        draw.line([(30, head_y + 9), (45, head_y + 15)], fill=p["outline"], width=2)
        draw.line([(66, head_y + 9), (51, head_y + 15)], fill=p["outline"], width=2)
    elif mode == "sad":
        draw.ellipse([34, head_y + 13, 42, head_y + 22], fill=p["pupil"])
        draw.ellipse([54, head_y + 13, 62, head_y + 22], fill=p["pupil"])
        draw.ellipse([35, head_y + 14, 37, head_y + 16], fill=p["sparkle"])
        draw.ellipse([55, head_y + 14, 57, head_y + 16], fill=p["sparkle"])
        draw.ellipse([29, head_y + 22, 33, head_y + 26], fill=p["tear"])
    elif mode == "empathy":
        draw.ellipse([33, head_y + 12, 43, head_y + 22], fill=p["pupil"])
        draw.ellipse([53, head_y + 12, 63, head_y + 22], fill=p["pupil"])
        draw.ellipse([34, head_y + 13, 38, head_y + 17], fill=p["sparkle"])
        draw.ellipse([54, head_y + 13, 58, head_y + 17], fill=p["sparkle"])
        draw.ellipse([39, head_y + 18, 41, head_y + 20], fill=p["sparkle"])
        draw.ellipse([59, head_y + 18, 61, head_y + 20], fill=p["sparkle"])
    else:
        draw.ellipse([35, head_y + 12, 41, head_y + 22], fill=p["pupil"])
        draw.ellipse([55, head_y + 12, 61, head_y + 22], fill=p["pupil"])
        draw.ellipse([36, head_y + 13, 38, head_y + 16], fill=p["sparkle"])
        draw.ellipse([56, head_y + 13, 58, head_y + 16], fill=p["sparkle"])

def draw_muzzle(draw, head_y=26, mode="normal"):
    p = PALETTE
    if mode == "turned":
        return

    draw.polygon([(46, head_y + 23), (50, head_y + 23), (48, head_y + 25)], fill=p["nose"])

    if mode == "angry":
        draw.line([(44, head_y + 27), (52, head_y + 27)], fill=p["mouth"], width=2)
    elif mode == "sad":
        draw.arc([44, head_y + 26, 52, head_y + 31], start=0, end=180, fill=p["outline"], width=1)
    elif mode == "happy" or mode == "petted":
        draw.polygon([(45, head_y + 26), (51, head_y + 26), (48, head_y + 29)], fill=p["mouth"])
    else:
        draw.line([(48, head_y + 25), (48, head_y + 27)], fill=p["outline"])
        draw.arc([44, head_y + 25, 48, head_y + 28], start=180, end=360, fill=p["outline"])
        draw.arc([48, head_y + 25, 52, head_y + 28], start=180, end=360, fill=p["outline"])

    draw.line([(22, head_y + 21), (12, head_y + 19)], fill=p["outline"], width=1)
    draw.line([(22, head_y + 24), (11, head_y + 25)], fill=p["outline"], width=1)
    draw.line([(74, head_y + 21), (84, head_y + 19)], fill=p["outline"], width=1)
    draw.line([(74, head_y + 24), (85, head_y + 25)], fill=p["outline"], width=1)

def draw_body_and_paws(draw, mode="normal", bounce=0):
    p = PALETTE
    by = 56 + bounce

    if mode == "sleeping":
        draw.ellipse([26, 60, 70, 84], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([46, 68, 56, 76], fill=p["fur_light"])
        return

    if mode == "turned":
        draw.ellipse([32, by, 64, by + 28], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([38, by + 4, 58, by + 22], fill=p["fur_shadow"])
        return

    draw.ellipse([32, by, 64, by + 28], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([40, by + 2, 56, by + 20], fill=p["fur_light"])

    draw.line([(36, by - 1), (60, by - 1)], fill=p["collar"], width=2)
    draw.ellipse([46, by, 50, by + 4], fill=p["bell"])

    if mode == "scratching":
        draw.ellipse([36, by + 16, 44, by + 27], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([52, by + 16, 60, by + 27], fill=p["fur_main"], outline=p["outline"])
        draw.line([(22, by + 10), (28, 38)], fill=p["fur_main"], width=4)
        draw.ellipse([24, 34, 30, 40], fill=p["fur_light"], outline=p["outline"])
    elif mode == "falling":
        draw.ellipse([24, by + 6, 32, by + 14], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([64, by + 6, 72, by + 14], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([30, by + 20, 38, by + 28], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([58, by + 20, 66, by + 28], fill=p["fur_main"], outline=p["outline"])
    elif mode == "peeking":
        draw.ellipse([34, by - 2, 42, by + 6], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([54, by - 2, 62, by + 6], fill=p["fur_main"], outline=p["outline"])
    else:
        draw.ellipse([36, by + 16, 44, by + 27], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([52, by + 16, 60, by + 27], fill=p["fur_main"], outline=p["outline"])
        draw.line([(38, by + 24), (38, by + 27)], fill=p["outline"])
        draw.line([(42, by + 24), (42, by + 27)], fill=p["outline"])
        draw.line([(54, by + 24), (54, by + 27)], fill=p["outline"])
        draw.line([(58, by + 24), (58, by + 27)], fill=p["outline"])

def draw_fluffy_tail(draw, tail_phase=0.0, mode="normal"):
    p = PALETTE
    if mode == "sleeping":
        draw.arc([16, 58, 48, 86], start=90, end=270, fill=p["fur_main"], width=10)
        draw.ellipse([16, 58, 28, 70], fill=p["fur_main"], outline=p["outline"])
        return

    if mode == "turned":
        draw.arc([48, 52, 84, 82], start=270, end=90, fill=p["fur_main"], width=11)
        draw.ellipse([70, 50, 84, 64], fill=p["fur_main"], outline=p["outline"])
        return

    wiggle = math.sin(tail_phase) * 10
    base_x = 60
    base_y = 74
    mid_x = 76 + wiggle * 0.5
    mid_y = 60
    tip_x = 74 + wiggle
    tip_y = 38

    draw.ellipse([base_x - 3, base_y - 4, base_x + 9, base_y + 8], fill=p["fur_main"])
    draw.ellipse([mid_x - 7, mid_y - 7, mid_x + 13, mid_y + 13], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([tip_x - 8, tip_y - 8, tip_x + 14, tip_y + 14], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([mid_x - 4, mid_y - 4, mid_x + 10, mid_y + 10], fill=p["fur_main"])
    draw.ellipse([tip_x - 5, tip_y - 5, tip_x + 11, tip_y + 11], fill=p["fur_light"])

def draw_dust_feathers(draw, tail_x, tail_y):
    p = PALETTE
    draw.ellipse([tail_x - 14, tail_y - 12, tail_x + 22, tail_y + 24], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([tail_x - 8, tail_y - 6, tail_x + 16, tail_y + 18], fill=p["fur_light"])
    for i in range(-2, 3):
        draw.line([(tail_x + i * 6, tail_y + 22), (tail_x + i * 8, tail_y + 30)], fill=p["fur_shadow"], width=2)

def draw_hearts(draw, frame=0):
    p = PALETTE
    offset_y = (frame * 3) % 18
    hx = 70
    hy = 24 - offset_y
    draw.polygon([(hx, hy), (hx + 4, hy - 4), (hx + 8, hy), (hx + 4, hy + 5)], fill=p["heart"])
    draw.polygon([(24, hy + 6), (28, hy + 2), (32, hy + 6), (28, hy + 11)], fill=p["heart"])

def draw_zzz(draw, frame=0):
    p = PALETTE
    offset = (frame * 2) % 16
    draw.text((70, 20 - offset), "Z", fill=(192, 132, 252, 255))
    draw.text((78, 12 - offset), "z", fill=(192, 132, 252, 200))

def render_cat_frame(mode="idle", frame_idx=0):
    img = create_base_canvas()
    draw = ImageDraw.Draw(img)

    head_y = 26
    bounce = 0
    ear_twitch = 0
    tail_phase = (frame_idx * 0.4)

    if mode == "happy":
        bounce = -2 if (frame_idx % 2 == 0) else 0
        head_y += bounce
    elif mode == "petted":
        bounce = 1 if (frame_idx % 2 == 0) else 0
        head_y += bounce
    elif mode == "falling":
        head_y += 6
        bounce = 4

    blink = False
    if mode == "idle" and (frame_idx % 8 == 0):
        blink = True

    if mode == "scratching":
        ear_twitch = 3 if (frame_idx % 2 == 0) else -2

    draw_fluffy_tail(draw, tail_phase=tail_phase, mode=mode)
    draw_body_and_paws(draw, mode=mode, bounce=bounce)
    draw_ears(draw, mode=mode, ear_twitch=ear_twitch)
    draw_head_shape(draw, head_y=head_y, mode=mode)
    draw_eyes(draw, head_y=head_y, mode=mode, blink=blink)
    draw_muzzle(draw, head_y=head_y, mode=mode)

    if mode == "happy" or mode == "petted":
        draw_hearts(draw, frame_idx)
    elif mode == "sleeping":
        draw_zzz(draw, frame_idx)

    scaled_img = img.resize((CANVAS_SIZE * SCALE, CANVAS_SIZE * SCALE), Image.NEAREST)
    return scaled_img

def render_screen_scratch():
    w, h = 320, 240
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    p = PALETTE

    draw.line([(40, 30), (140, 190)], fill=p["scratch"], width=4)
    draw.line([(70, 20), (170, 210)], fill=p["scratch"], width=4)
    draw.line([(100, 35), (200, 195)], fill=p["scratch"], width=3)
    draw.line([(50, 45), (135, 175)], fill=(200, 200, 220, 180), width=2)
    return img

class SpriteManager:
    def __init__(self):
        self.cache = {}

    def get_tk_image(self, mode="idle", frame_idx=0):
        key = f"{mode}_{frame_idx}"
        if key not in self.cache:
            pil_img = render_cat_frame(mode, frame_idx)
            self.cache[key] = ImageTk.PhotoImage(pil_img)
        return self.cache[key]

    def get_scratch_tk_image(self):
        key = "scratch_overlay"
        if key not in self.cache:
            pil_img = render_screen_scratch()
            self.cache[key] = ImageTk.PhotoImage(pil_img)
        return self.cache[key]

sprite_manager = SpriteManager()

if __name__ == "__main__":
    print("Generating and saving test sprite frames...")
    modes = ["idle", "happy", "petted", "sad", "angry", "turned", "scratching", "peeking", "sleeping", "falling", "frightened", "empathy"]
    for m in modes:
        img = render_cat_frame(m, 0)
        img.save(f"assets/sprite_{m}.png")
    print("Done! Test frames saved to assets/.")

