import math
from PIL import Image, ImageDraw, ImageTk

CANVAS_SIZE = 96
SCALE = 2

PALETTE = {
    "outline": (16, 15, 24, 255),
    "fur_deep": (22, 21, 30, 255),
    "fur_main": (36, 35, 48, 255),
    "fur_highlight": (56, 55, 74, 255),
    "chest_fluff": (72, 70, 92, 255),
    "chest_fluff_light": (94, 92, 118, 255),
    "ear_shadow": (168, 85, 247, 255),
    "ear_inner": (244, 114, 182, 255),
    "ear_fluff": (253, 226, 236, 255),
    "blush": (251, 113, 133, 190),
    "eye_white": (255, 255, 255, 255),
    "eye_color_top": (34, 197, 94, 255),
    "eye_color_mid": (74, 222, 128, 255),
    "eye_color_bot": (250, 204, 21, 255),
    "pupil": (12, 18, 32, 255),
    "sparkle_big": (255, 255, 255, 255),
    "sparkle_small": (255, 255, 255, 230),
    "nose": (251, 113, 133, 255),
    "mouth_dark": (136, 19, 55, 255),
    "tongue": (244, 114, 182, 255),
    "collar": (239, 68, 68, 255),
    "bell": (250, 204, 21, 255),
    "scratch": (255, 255, 255, 235),
    "tear": (96, 165, 250, 255),
    "heart": (244, 63, 94, 255),
    "transparent": (0, 0, 0, 0)
}

BREED_PRESETS = {
    "black": {
        "outline": (16, 15, 24, 255),
        "fur_deep": (22, 21, 30, 255),
        "fur_main": (36, 35, 48, 255),
        "fur_highlight": (56, 55, 74, 255),
        "chest_fluff": (72, 70, 92, 255),
        "chest_fluff_light": (94, 92, 118, 255),
        "ear_shadow": (168, 85, 247, 255),
        "ear_inner": (244, 114, 182, 255),
        "ear_fluff": (253, 226, 236, 255),
        "eye_color_top": (34, 197, 94, 255),
        "eye_color_mid": (74, 222, 128, 255),
        "eye_color_bot": (250, 204, 21, 255),
    },
    "orange": {
        "outline": (120, 53, 15, 255),
        "fur_deep": (194, 65, 12, 255),
        "fur_main": (249, 115, 22, 255),
        "fur_highlight": (251, 146, 60, 255),
        "chest_fluff": (254, 243, 199, 255),
        "chest_fluff_light": (255, 251, 235, 255),
        "ear_shadow": (234, 88, 12, 255),
        "ear_inner": (253, 164, 175, 255),
        "ear_fluff": (255, 241, 242, 255),
        "eye_color_top": (217, 119, 6, 255),
        "eye_color_mid": (245, 158, 11, 255),
        "eye_color_bot": (252, 211, 77, 255),
    },
    "white": {
        "outline": (100, 116, 139, 255),
        "fur_deep": (203, 213, 225, 255),
        "fur_main": (248, 250, 252, 255),
        "fur_highlight": (255, 255, 255, 255),
        "chest_fluff": (241, 245, 249, 255),
        "chest_fluff_light": (255, 255, 255, 255),
        "ear_shadow": (244, 114, 182, 255),
        "ear_inner": (251, 164, 185, 255),
        "ear_fluff": (255, 245, 248, 255),
        "eye_color_top": (2, 132, 199, 255),
        "eye_color_mid": (56, 189, 248, 255),
        "eye_color_bot": (125, 211, 252, 255),
    },
    "siamese": {
        "outline": (41, 24, 18, 255),
        "fur_deep": (68, 43, 33, 255),
        "fur_main": (243, 232, 217, 255),
        "fur_highlight": (254, 249, 243, 255),
        "chest_fluff": (255, 255, 255, 255),
        "chest_fluff_light": (255, 255, 255, 255),
        "ear_shadow": (55, 30, 22, 255),
        "ear_inner": (214, 143, 143, 255),
        "ear_fluff": (250, 230, 220, 255),
        "eye_color_top": (29, 78, 216, 255),
        "eye_color_mid": (59, 130, 246, 255),
        "eye_color_bot": (147, 197, 253, 255),
    },
    "calico": {
        "outline": (30, 27, 36, 255),
        "fur_deep": (180, 83, 9, 255),
        "fur_main": (245, 245, 247, 255),
        "fur_highlight": (255, 255, 255, 255),
        "chest_fluff": (254, 215, 170, 255),
        "chest_fluff_light": (255, 237, 213, 255),
        "ear_shadow": (217, 119, 6, 255),
        "ear_inner": (244, 114, 182, 255),
        "ear_fluff": (255, 250, 250, 255),
        "eye_color_top": (13, 148, 136, 255),
        "eye_color_mid": (20, 184, 166, 255),
        "eye_color_bot": (94, 234, 212, 255),
    }
}

def set_cat_breed(breed_name):
    if breed_name in BREED_PRESETS:
        PALETTE.update(BREED_PRESETS[breed_name])
        sprite_manager.cache.clear()

def create_base_canvas():
    return Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), PALETTE["transparent"])

def draw_ears(draw, mode="normal", ear_twitch=0):
    p = PALETTE
    if mode == "turned":
        draw.polygon([(26, 10), (40, 28), (18, 30)], fill=p["fur_main"], outline=p["outline"])
        draw.polygon([(70, 10), (78, 30), (56, 28)], fill=p["fur_main"], outline=p["outline"])
        return

    if mode == "angry":
        draw.polygon([(14, 26), (36, 32), (22, 38)], fill=p["fur_main"], outline=p["outline"])
        draw.polygon([(82, 26), (74, 38), (60, 32)], fill=p["fur_main"], outline=p["outline"])
        draw.polygon([(17, 28), (33, 33), (24, 36)], fill=p["ear_inner"])
        draw.polygon([(79, 28), (72, 36), (63, 33)], fill=p["ear_inner"])
        return

    if mode == "sad":
        draw.polygon([(16, 22), (36, 29), (20, 36)], fill=p["fur_main"], outline=p["outline"])
        draw.polygon([(80, 22), (76, 36), (60, 29)], fill=p["fur_main"], outline=p["outline"])
        draw.polygon([(19, 24), (33, 30), (22, 34)], fill=p["ear_inner"])
        draw.polygon([(77, 24), (74, 34), (63, 30)], fill=p["ear_inner"])
        return

    ltx = 24 + ear_twitch
    lty = 9
    rtx = 72 - ear_twitch
    rty = 9

    draw.polygon([(ltx, lty), (40, 28), (18, 29)], fill=p["fur_main"], outline=p["outline"])
    draw.polygon([(ltx + 3, lty + 4), (37, 27), (22, 27)], fill=p["ear_shadow"])
    draw.polygon([(ltx + 4, lty + 6), (35, 26), (24, 26)], fill=p["ear_inner"])
    draw.polygon([(ltx + 6, lty + 10), (33, 25), (26, 25)], fill=p["ear_fluff"])

    draw.polygon([(rtx, rty), (78, 29), (56, 28)], fill=p["fur_main"], outline=p["outline"])
    draw.polygon([(rtx - 3, rty + 4), (74, 27), (59, 27)], fill=p["ear_shadow"])
    draw.polygon([(rtx - 4, rty + 6), (72, 26), (61, 26)], fill=p["ear_inner"])
    draw.polygon([(rtx - 6, rty + 10), (70, 25), (63, 25)], fill=p["ear_fluff"])

def draw_head_shape(draw, head_y=26, mode="normal"):
    p = PALETTE

    draw.ellipse([21, head_y - 1, 75, head_y + 36], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([24, head_y + 2, 72, head_y + 34], fill=p["fur_main"])

    draw.ellipse([28, head_y + 1, 68, head_y + 12], fill=p["fur_highlight"])

    draw.polygon([(22, head_y + 15), (12, head_y + 20), (22, head_y + 23)], fill=p["fur_main"], outline=p["outline"])
    draw.polygon([(22, head_y + 21), (14, head_y + 25), (23, head_y + 28)], fill=p["fur_main"], outline=p["outline"])
    draw.polygon([(23, head_y + 26), (17, head_y + 30), (25, head_y + 32)], fill=p["fur_main"], outline=p["outline"])
    draw.polygon([(22, head_y + 16), (15, head_y + 20), (23, head_y + 28)], fill=p["fur_main"])

    draw.polygon([(74, head_y + 15), (84, head_y + 20), (74, head_y + 23)], fill=p["fur_main"], outline=p["outline"])
    draw.polygon([(74, head_y + 21), (82, head_y + 25), (73, head_y + 28)], fill=p["fur_main"], outline=p["outline"])
    draw.polygon([(73, head_y + 26), (79, head_y + 30), (71, head_y + 32)], fill=p["fur_main"], outline=p["outline"])
    draw.polygon([(74, head_y + 16), (81, head_y + 20), (73, head_y + 28)], fill=p["fur_main"])

def draw_eyes(draw, head_y=26, mode="normal", blink=False):
    p = PALETTE
    if mode == "turned":
        return

    if blink or mode == "sleeping":
        draw.arc([30, head_y + 16, 44, head_y + 23], start=180, end=360, fill=p["outline"], width=3)
        draw.arc([52, head_y + 16, 66, head_y + 23], start=180, end=360, fill=p["outline"], width=3)
        draw.ellipse([26, head_y + 21, 34, head_y + 26], fill=p["blush"])
        draw.ellipse([62, head_y + 21, 70, head_y + 26], fill=p["blush"])
        return

    if mode == "petted" or mode == "happy" or mode == "eating":
        draw.arc([30, head_y + 11, 45, head_y + 21], start=0, end=180, fill=p["outline"], width=3)
        draw.arc([51, head_y + 11, 66, head_y + 21], start=0, end=180, fill=p["outline"], width=3)
        draw.ellipse([25, head_y + 19, 35, head_y + 25], fill=p["blush"])
        draw.ellipse([61, head_y + 19, 71, head_y + 25], fill=p["blush"])
        return

    if mode == "frightened":
        draw.ellipse([29, head_y + 7, 46, head_y + 25], fill=p["eye_white"], outline=p["outline"])
        draw.ellipse([50, head_y + 7, 67, head_y + 25], fill=p["eye_white"], outline=p["outline"])
        draw.ellipse([35, head_y + 13, 40, head_y + 19], fill=p["pupil"])
        draw.ellipse([56, head_y + 13, 61, head_y + 19], fill=p["pupil"])
        return

    draw.ellipse([29, head_y + 9, 45, head_y + 25], fill=p["eye_white"], outline=p["outline"])
    draw.ellipse([51, head_y + 9, 67, head_y + 25], fill=p["eye_white"], outline=p["outline"])

    draw.ellipse([31, head_y + 10, 43, head_y + 24], fill=p["eye_color_top"])
    draw.ellipse([53, head_y + 10, 65, head_y + 24], fill=p["eye_color_top"])

    draw.chord([31, head_y + 14, 43, head_y + 24], start=0, end=180, fill=p["eye_color_mid"])
    draw.chord([53, head_y + 14, 65, head_y + 24], start=0, end=180, fill=p["eye_color_mid"])

    draw.chord([32, head_y + 18, 42, head_y + 24], start=0, end=180, fill=p["eye_color_bot"])
    draw.chord([54, head_y + 18, 64, head_y + 24], start=0, end=180, fill=p["eye_color_bot"])

    draw.ellipse([25, head_y + 21, 33, head_y + 26], fill=p["blush"])
    draw.ellipse([63, head_y + 21, 71, head_y + 26], fill=p["blush"])

    if mode == "angry":
        draw.ellipse([34, head_y + 12, 40, head_y + 22], fill=p["pupil"])
        draw.ellipse([56, head_y + 12, 62, head_y + 22], fill=p["pupil"])
        draw.line([(28, head_y + 8), (45, head_y + 15)], fill=p["outline"], width=3)
        draw.line([(68, head_y + 8), (51, head_y + 15)], fill=p["outline"], width=3)
    elif mode == "sad":
        draw.ellipse([33, head_y + 12, 42, head_y + 22], fill=p["pupil"])
        draw.ellipse([54, head_y + 12, 63, head_y + 22], fill=p["pupil"])
        draw.ellipse([34, head_y + 12, 38, head_y + 16], fill=p["sparkle_big"])
        draw.ellipse([55, head_y + 12, 59, head_y + 16], fill=p["sparkle_big"])
        draw.ellipse([27, head_y + 23, 32, head_y + 28], fill=p["tear"])
    elif mode == "empathy":
        draw.ellipse([32, head_y + 11, 43, head_y + 23], fill=p["pupil"])
        draw.ellipse([53, head_y + 11, 64, head_y + 23], fill=p["pupil"])
        draw.ellipse([33, head_y + 12, 38, head_y + 17], fill=p["sparkle_big"])
        draw.ellipse([54, head_y + 12, 59, head_y + 17], fill=p["sparkle_big"])
        draw.ellipse([39, head_y + 18, 42, head_y + 21], fill=p["sparkle_small"])
        draw.ellipse([60, head_y + 18, 63, head_y + 21], fill=p["sparkle_small"])
    else:
        draw.ellipse([33, head_y + 11, 42, head_y + 23], fill=p["pupil"])
        draw.ellipse([54, head_y + 11, 63, head_y + 23], fill=p["pupil"])
        draw.ellipse([34, head_y + 12, 38, head_y + 16], fill=p["sparkle_big"])
        draw.ellipse([55, head_y + 12, 59, head_y + 16], fill=p["sparkle_big"])
        draw.ellipse([38, head_y + 18, 41, head_y + 21], fill=p["sparkle_small"])
        draw.ellipse([59, head_y + 18, 62, head_y + 21], fill=p["sparkle_small"])

def draw_muzzle(draw, head_y=26, mode="normal"):
    p = PALETTE
    if mode == "turned":
        return

    draw.polygon([(46, head_y + 22), (50, head_y + 22), (48, head_y + 25)], fill=p["nose"])

    if mode == "angry":
        draw.line([(44, head_y + 27), (52, head_y + 27)], fill=p["mouth_dark"], width=2)
    elif mode == "sad":
        draw.arc([44, head_y + 26, 52, head_y + 31], start=0, end=180, fill=p["outline"], width=1)
    elif mode == "happy" or mode == "petted" or mode == "eating":
        draw.polygon([(45, head_y + 25), (51, head_y + 25), (48, head_y + 29)], fill=p["mouth_dark"])
        draw.ellipse([46, head_y + 26, 50, head_y + 29], fill=p["tongue"])
    else:
        draw.line([(48, head_y + 25), (48, head_y + 27)], fill=p["outline"])
        draw.arc([43, head_y + 25, 48, head_y + 28], start=180, end=360, fill=p["outline"], width=1)
        draw.arc([48, head_y + 25, 53, head_y + 28], start=180, end=360, fill=p["outline"], width=1)

    draw.line([(22, head_y + 21), (8, head_y + 18)], fill=p["outline"], width=1)
    draw.line([(22, head_y + 24), (7, head_y + 25)], fill=p["outline"], width=1)
    draw.line([(22, head_y + 27), (10, head_y + 31)], fill=p["outline"], width=1)

    draw.line([(74, head_y + 21), (88, head_y + 18)], fill=p["outline"], width=1)
    draw.line([(74, head_y + 24), (89, head_y + 25)], fill=p["outline"], width=1)
    draw.line([(74, head_y + 27), (86, head_y + 31)], fill=p["outline"], width=1)

def draw_body_and_paws(draw, mode="normal", bounce=0):
    p = PALETTE
    by = 56 + bounce

    if mode == "sleeping":
        draw.ellipse([24, 60, 72, 84], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([40, 64, 56, 78], fill=p["chest_fluff"])
        return

    if mode == "turned":
        draw.ellipse([30, by, 66, by + 28], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([36, by + 4, 60, by + 22], fill=p["fur_deep"])
        return

    draw.ellipse([30, by, 66, by + 28], fill=p["fur_main"], outline=p["outline"])

    draw.polygon([(48, by + 2), (40, by + 16), (48, by + 24), (56, by + 16)], fill=p["chest_fluff"])
    draw.polygon([(48, by + 4), (43, by + 14), (48, by + 20), (53, by + 14)], fill=p["chest_fluff_light"])

    draw.line([(34, by - 1), (62, by - 1)], fill=p["collar"], width=3)
    draw.ellipse([45, by - 1, 51, by + 5], fill=p["bell"], outline=p["outline"])

    if mode == "scratching":
        draw.ellipse([34, by + 16, 44, by + 27], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([52, by + 16, 62, by + 27], fill=p["fur_main"], outline=p["outline"])
        draw.line([(22, by + 8), (28, 38)], fill=p["fur_main"], width=5)
        draw.ellipse([23, 34, 30, 41], fill=p["chest_fluff"], outline=p["outline"])
    elif mode == "falling":
        draw.ellipse([22, by + 6, 32, by + 15], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([64, by + 6, 74, by + 15], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([28, by + 20, 38, by + 28], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([58, by + 20, 68, by + 28], fill=p["fur_main"], outline=p["outline"])
    elif mode == "peeking":
        draw.ellipse([32, by - 2, 42, by + 7], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([54, by - 2, 64, by + 7], fill=p["fur_main"], outline=p["outline"])
    elif mode == "walking":
        paw_offset = 4 if (bounce != 0) else -4
        draw.ellipse([34 + paw_offset, by + 16, 44 + paw_offset, by + 27], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([52 - paw_offset, by + 16, 62 - paw_offset, by + 27], fill=p["fur_main"], outline=p["outline"])
    elif mode == "eating":
        draw.ellipse([34, by + 16, 44, by + 27], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([52, by + 16, 62, by + 27], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([40, by + 20, 55, by + 27], fill=(56, 189, 248, 255), outline=p["outline"])
        draw.polygon([(55, by + 23), (60, by + 19), (60, by + 27)], fill=(56, 189, 248, 255), outline=p["outline"])
    else:
        draw.ellipse([34, by + 16, 44, by + 27], fill=p["fur_main"], outline=p["outline"])
        draw.ellipse([52, by + 16, 62, by + 27], fill=p["fur_main"], outline=p["outline"])
        draw.line([(37, by + 24), (37, by + 27)], fill=p["outline"])
        draw.line([(41, by + 24), (41, by + 27)], fill=p["outline"])
        draw.line([(55, by + 24), (55, by + 27)], fill=p["outline"])
        draw.line([(59, by + 24), (59, by + 27)], fill=p["outline"])

def draw_fluffy_tail(draw, tail_phase=0.0, mode="normal"):
    p = PALETTE
    if mode == "sleeping":
        draw.arc([14, 56, 50, 88], start=90, end=270, fill=p["fur_main"], width=13)
        draw.ellipse([14, 56, 28, 70], fill=p["fur_main"], outline=p["outline"])
        return

    if mode == "turned":
        draw.arc([46, 50, 86, 84], start=270, end=90, fill=p["fur_main"], width=14)
        draw.ellipse([68, 48, 86, 66], fill=p["fur_main"], outline=p["outline"])
        return

    wiggle = math.sin(tail_phase) * 11
    base_x = 60
    base_y = 74
    mid_x = 77 + wiggle * 0.5
    mid_y = 58
    tip_x = 75 + wiggle
    tip_y = 34

    draw.ellipse([base_x - 4, base_y - 5, base_x + 12, base_y + 10], fill=p["fur_main"])
    draw.ellipse([mid_x - 9, mid_y - 9, mid_x + 17, mid_y + 17], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([tip_x - 11, tip_y - 11, tip_x + 18, tip_y + 18], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([mid_x - 5, mid_y - 5, mid_x + 13, mid_y + 13], fill=p["fur_main"])
    draw.ellipse([tip_x - 7, tip_y - 7, tip_x + 14, tip_y + 14], fill=p["fur_highlight"])

def draw_hearts(draw, frame=0):
    p = PALETTE
    offset_y = (frame * 3) % 18
    hx = 70
    hy = 24 - offset_y
    draw.polygon([(hx, hy), (hx + 4, hy - 4), (hx + 8, hy), (hx + 4, hy + 5)], fill=p["heart"])
    draw.polygon([(24, hy + 6), (28, hy + 2), (32, hy + 6), (28, hy + 11)], fill=p["heart"])

def draw_zzz(draw, frame=0):
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
    elif mode == "walking":
        bounce = -1 if (frame_idx % 2 == 0) else 1
        head_y += bounce
    elif mode == "eating":
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
    print("Regenerating all high-definition cute sprite frames...")
    modes = [
        "idle", "happy", "petted", "sad", "angry", "turned",
        "scratching", "peeking", "sleeping", "falling",
        "frightened", "empathy", "walking", "eating"
    ]
    for m in modes:
        img = render_cat_frame(m, 0)
        img.save(f"assets/sprite_{m}.png")
    print("Done! High-definition cute cat sprites saved to assets/.")
