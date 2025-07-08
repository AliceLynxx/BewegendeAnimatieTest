from PIL import Image, ImageDraw
import math
import constants

def create_animation_frame(background, frame_number):
    """
    Creëert een enkel frame van de animatie.
    
    Args:
        background: PIL Image object van de achtergrond
        frame_number: Huidige frame nummer (0, 1, 2)
    
    Returns:
        PIL Image object van het gecreëerde frame
    """
    # Kopieer de achtergrond
    frame = background.copy()
    draw = ImageDraw.Draw(frame)
    
    # Bereken positie binnen het ovaal gebaseerd op frame nummer
    angle = (frame_number * 2 * math.pi) / constants.ANIMATION_FRAMES
    
    # Bereken x,y positie binnen het ovaal
    x_offset = (constants.OVAL_WIDTH / 2 - 20) * math.cos(angle)
    y_offset = (constants.OVAL_HEIGHT / 2 - 20) * math.sin(angle)
    
    x = constants.OVAL_CENTER_X + x_offset
    y = constants.OVAL_CENTER_Y + y_offset
    
    # Teken een simpele vorm als placeholder voor de fMRI/ECG animatie
    # Dit wordt later vervangen door de echte animatie
    draw.ellipse([x-10, y-10, x+10, y+10], fill="red", outline="darkred")
    
    return frame

def create_gif():
    """
    Creëert de GIF animatie met de bewegende elementen binnen het ovaal.
    """
    try:
        # Laad de achtergrond afbeelding
        background = Image.open(constants.BACKGROUND_PATH)
    except FileNotFoundError:
        print(f"Achtergrond bestand niet gevonden: {constants.BACKGROUND_PATH}")
        print("Maak een placeholder achtergrond aan...")
        # Maak een placeholder achtergrond
        background = Image.new('RGB', (800, 600), color='lightblue')
        draw = ImageDraw.Draw(background)
        # Teken het ovaal als referentie
        oval_bounds = [
            constants.OVAL_CENTER_X - constants.OVAL_WIDTH/2,
            constants.OVAL_CENTER_Y - constants.OVAL_HEIGHT/2,
            constants.OVAL_CENTER_X + constants.OVAL_WIDTH/2,
            constants.OVAL_CENTER_Y + constants.OVAL_HEIGHT/2
        ]
        draw.ellipse(oval_bounds, outline="black", width=2)
    
    # Genereer alle frames
    frames = []
    for i in range(constants.ANIMATION_FRAMES):
        frame = create_animation_frame(background, i)
        frames.append(frame)
    
    # Sla de GIF op
    frames[0].save(
        constants.OUTPUT_FILENAME,
        save_all=True,
        append_images=frames[1:],
        duration=constants.FRAME_DURATION,
        loop=0
    )
    
    print(f"GIF animatie opgeslagen als: {constants.OUTPUT_FILENAME}")

if __name__ == "__main__":
    create_gif()