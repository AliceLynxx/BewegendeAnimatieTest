from PIL import Image, ImageDraw, ImageFont
import os
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

def create_animation_frame(frame_num, total_frames):
    """Creëert een enkel frame van de animatie"""
    # Laad achtergrond of maak placeholder
    if os.path.exists(BACKGROUND_PATH):
        background = Image.open(BACKGROUND_PATH).convert('RGBA')
    else:
        background = Image.new('RGBA', (800, 600), (200, 200, 200, 255))
    
    overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Tekst animatie - geleidelijk meer tekst tonen
    chars_to_show = int((frame_num / total_frames) * len(ANIMATION_TEXT)) + 1
    visible_text = ANIMATION_TEXT[:chars_to_show]
    
    try:
        font = ImageFont.truetype("arial.ttf", TEXT_SIZE)
    except:
        font = ImageFont.load_default()
    
    # Teken tekst met heatmap kleuren
    for i, char in enumerate(visible_text):
        char_intensity = (i + 1) / len(ANIMATION_TEXT)
        char_color = get_heatmap_color(char_intensity)
        char_x = TEXT_POSITION[0] + (i * TEXT_SIZE // 2)
        draw.text((char_x, TEXT_POSITION[1]), char, fill=char_color + (255,), font=font)
    
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