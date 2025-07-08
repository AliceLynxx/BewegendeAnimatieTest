from PIL import Image, ImageDraw
import os
import random
import math
from constants import *

def get_heatmap_color(intensity):
    """Geeft fMRI-achtige heatmap kleur gebaseerd op intensiteit (0-1)"""
    if intensity < 0.5:
        # Blauw naar geel
        r = int(255 * intensity * 2)
        g = int(255 * intensity * 2)
        b = 255 - int(255 * intensity * 2)
    else:
        # Geel naar rood
        r = 255
        g = 255 - int(255 * (intensity - 0.5) * 2)
        b = 0
    return (r, g, b)

def get_random_position_in_oval():
    """Genereert willekeurige positie binnen het ovaal"""
    while True:
        # Genereer willekeurige punt binnen rechthoek
        x = random.uniform(-OVAL_RADIUS_X, OVAL_RADIUS_X)
        y = random.uniform(-OVAL_RADIUS_Y, OVAL_RADIUS_Y)
        
        # Controleer of punt binnen ovaal ligt
        if (x/OVAL_RADIUS_X)**2 + (y/OVAL_RADIUS_Y)**2 <= 1:
            return OVAL_CENTER[0] + int(x), OVAL_CENTER[1] + int(y)

def create_animation_frame(frame_num, total_frames):
    """Creëert een enkel frame van de animatie"""
    # Laad achtergrond of maak placeholder
    if os.path.exists(BACKGROUND_PATH):
        background = Image.open(BACKGROUND_PATH).convert('RGBA')
    else:
        background = Image.new('RGBA', (800, 600), (200, 200, 200, 255))
    
    # Willekeurige positie binnen ovaal
    center_x, center_y = get_random_position_in_oval()
    
    # Teken animatie met graduele overgang
    overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Teken concentrische cirkels voor vloeiende overgang
    for i in range(50):
        radius = ANIMATION_SIZE - (i * ANIMATION_SIZE // 50)
        if radius <= 0:
            break
        intensity = 1.0 - (i / 50.0)  # Donker centrum, licht rand
        color = get_heatmap_color(intensity * 0.8)
        alpha = int(255 * intensity * 0.3)  # Zachte transparantie
        
        draw.ellipse([
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius
        ], fill=color + (alpha,))
    
    # Combineer achtergrond en overlay
    result = Image.alpha_composite(background, overlay)
    return result.convert('RGB')

def create_gif():
    """Creëert de GIF animatie"""
    frames = []
    for i in range(ANIMATION_FRAMES):
        frame = create_animation_frame(i, ANIMATION_FRAMES)
        frames.append(frame)
    
    # Sla op als GIF
    frames[0].save(
        OUTPUT_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=0
    )
    print(f"GIF opgeslagen als: {OUTPUT_PATH}")

if __name__ == "__main__":
    create_gif()