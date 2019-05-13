# File: palettes.py

'''
Color palettes for the Posterize function. 
Themed Palettes Credit: colourlovers.com.
'''

# Constants

HALLOWEEN_PALETTE = [ 
    [0, 0, 0],
    [124, 16, 173],
    [27, 165, 44],
    [241, 88, 2],
    [61, 61, 61],
    [255, 255, 255]
]
PREDEFINED_PALETTE = [
    [0, 0, 0],
    [0, 0, 255],
    [0, 255, 255],
    [64, 64, 64],
    [128, 128, 128],
    [0, 255, 0],
    [192, 192, 192],
    [255, 0, 255],
    [255, 200, 0],
    [255, 175, 175],
    [255, 0, 0],
    [255, 255, 255],
    [255, 255, 0]
]
COOL_PALETTE = [
    [207, 240, 158],
    [186, 219, 168],
    [121, 189, 154],
    [59, 134, 134],
    [11, 72, 107]
]
WARM_PALETTE = [
    [236, 208, 120],
    [217, 91, 67],
    [192, 41, 66],
    [84, 36, 55],
    [83, 119, 122]
]

def choosePalette():
    def clickAction(e):
        choice = gw.getElementAt(e.getX(), e.getY())
        if choice.getType() == GLabel: 
            palette = choice.getLabel()
            gw.close()
            return palette

    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 300
    BOX_WIDTH = 200
    BOX_HEIGHT = 50
    palettes = ['HALLOWEEN_PALLETE', 'PREDEFINED_PALETTE', 'COOL_PALETTE', 'WARM_PALETTE']
    font = "30px 'Helvetica Neue', 'Arial', 'Sans-serif'"
    gw = GWindow(WINDOW_WIDTH, WINDOW_HEIGHT)
    instruction = GLabel('Please select a color palette.')
    instruction.setFont(font)
    gw.add(instruction, (WINDOW_WIDTH - instruction.getWidth()) / 2, WINDOW_HEIGHT / 3)
    for i in range(len(palettes)):
        box = GCompound()
        label = GLabel(palettes[i][:-8])
        label.setFont(font)
        x = (WINDOW_WIDTH / 2 - BOX_WIDTH) / 2
        y = 125 + (75 * (i % 2))
        rect = GRect(BOX_WIDTH, BOX_HEIGHT)
        rect.setFilled(True)
        rect.setColor('lightgrey')
        box.add(rect, 0, 0)
        box.add(label, (BOX_WIDTH - label.getWidth()) / 2, (BOX_HEIGHT - label.getAscent()) / 2)
        if i > 1:
            gw.add(box, x + (WINDOW_WIDTH / 2), y)
        else:
            gw.add(box, x, y)
    gw.addEventListener('click', clickAction)