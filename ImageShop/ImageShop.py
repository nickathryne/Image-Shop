# File: ImageShop.py

"""
This program is the file for the ImageShop application, which
implements the "Load", "Flip Vertical", 'Flip Horizontal',
'Rotate Left', 'Rotate Right', 'Grayscale', 'Green Screen',
'Equalize', 'Posterize', and 'Pixelize' buttons.
"""

from filechooser import chooseInputFile
from pgl import GWindow, GImage, GRect, GButton, GLabel, GCompound
from GrayscaleImage import createGrayscaleImage
from EqualizeImage import createEqualizedImage

# Constants

GWINDOW_WIDTH = 1024
GWINDOW_HEIGHT = 700
BUTTON_WIDTH = 125
BUTTON_HEIGHT = 20
BUTTON_MARGIN = 10
BUTTON_BACKGROUND = "#CCCCCC"
PALETTE = [
    [236, 208, 120],
    [217, 91, 67],
    [192, 41, 66],
    [84, 36, 55],
    [83, 119, 122]
]
TILE_SIZE = 6

# Derived constants

BUTTON_AREA_WIDTH = 2 * BUTTON_MARGIN + BUTTON_WIDTH
IMAGE_AREA_WIDTH = GWINDOW_WIDTH - BUTTON_AREA_WIDTH

# The ImageShop application

def ImageShop():
    def addButton(label, action):
        """
        Adds a button to the region on the left side of the window
        """
        nonlocal nextButtonY
        x = BUTTON_MARGIN
        y = nextButtonY
        button = GButton(label, action)
        button.setSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        gw.add(button, x, y)
        nextButtonY += BUTTON_HEIGHT + BUTTON_MARGIN

    def setImage(image):
        """
        Sets image as the current image after removing the old one.
        """
        nonlocal currentImage
        if currentImage is not None:
            gw.remove(currentImage)
        currentImage = image
        x = BUTTON_AREA_WIDTH + (IMAGE_AREA_WIDTH - image.getWidth()) / 2
        y = (gw.getHeight() - image.getHeight()) / 2
        gw.add(image, x, y)

    def loadButtonAction():
        """Callback function for the Load button"""
        filename = chooseInputFile()
        if filename != "":
            setImage(GImage(filename))

    def flipVerticalAction():
        """Callback function for the FlipVertical button"""
        if currentImage is not None:
            setImage(flipVertical(currentImage))

    def flipHorizontalAction():
        '''Callback function for the FlipHorizontal button'''
        if currentImage is not None:
            setImage(flipHorizontal(currentImage))

    def rotateLeftAction():
        '''Callback function for the RotateLeft button'''
        if currentImage is not None:
            setImage(rotateLeft(currentImage))

    def rotateRightAction():
        '''Callback function for the RotateRight button'''
        if currentImage is not None:
            setImage(rotateRight(currentImage))

    def grayscaleAction():
        '''Callback function for the Grayscale button'''
        if currentImage is not None:
            setImage(createGrayscaleImage(currentImage))

    def greenScreenAction():
        '''Callback function for the GreenScreen button'''
        if currentImage is not None:
            filename = chooseInputFile()
            if filename != '':
                setImage(greenScreen(currentImage, GImage(filename)))

    def equalizeAction():
        '''Callback function for the Equalize button'''
        if currentImage is not None:
            setImage(createEqualizedImage(currentImage))

    def posterizeAction():
        '''Callback function for the Posterize button'''
        if currentImage is not None:
            setImage(posterize(currentImage))

    def pixelizeAction():
        '''Callback function for the Pixelize button'''
        if currentImage is not None:
            setImage(pixelize(currentImage))

    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    buttonArea = GRect(0, 0, BUTTON_AREA_WIDTH, GWINDOW_HEIGHT)    
    buttonArea.setFilled(True)
    buttonArea.setColor(BUTTON_BACKGROUND)
    gw.add(buttonArea)
    nextButtonY = BUTTON_MARGIN
    currentImage = None
    addButton("Load", loadButtonAction)
    addButton("Flip Vertical", flipVerticalAction)
    addButton('Flip Horizontal', flipHorizontalAction)
    addButton('Rotate Left', rotateLeftAction)
    addButton('Rotate Right', rotateRightAction)
    addButton('Grayscale', grayscaleAction)
    addButton('Green Screen', greenScreenAction)
    addButton('Equalize', equalizeAction)
    addButton('Posterize', posterizeAction)
    addButton('Pixelize', pixelizeAction)

# Creates a new GImage from the original one by flipping it vertically.

def flipVertical(image):
    array = image.getPixelArray()
    return GImage(array[::-1])

# Creates a new GImage from the original one by flipping it horizontally.

def flipHorizontal(image):
    array = image.getPixelArray()
    new_array = []
    for row in array:
        new_array.append(row[::-1])
    return GImage(new_array)

# Creates a new GImage from the original one by rotating it to the left 90 degrees.

def rotateLeft(image):
    array = image.getPixelArray()
    new_array = []
    for i in range(len(array[0])):
        new_array.append([])
    for row in array:
        for i in range(len(row)):
            new_array[i].append(row[len(row) - 1 - i])
    return GImage(new_array)

# Creates a new GImage from the original one by rotating it to the right 90 degrees.

def rotateRight(image):
    array = image.getPixelArray()
    new_array = []
    for i in range(len(array[0])):
        new_array.append([])
    for row in array[::-1]:
        for i in range(len(row)):
            new_array[i].append(row[i])
    return GImage(new_array)

# Creates a new GImage from the original and the new file by chroma keying.

def greenScreen(old, new):
    old_array = old.getPixelArray()
    new_array = new.getPixelArray()
    for col in range(len(old_array)):
        for row in range(len(old_array[0])):
            if col < len(new_array) and row < len(new_array[0]):
                pixel = new_array[col][row]
                max_rb = max(GImage.getRed(pixel), GImage.getBlue(pixel))
                green = GImage.getGreen(pixel)
                if green < 2 * max_rb:
                    old_array[col][row] = pixel
    return GImage(old_array)

# Creates a new GImage from the original by converting pixels to a ristrictive set.

def posterize(image):
    array = image.getPixelArray()
    for col in range(len(array)):
        for row in range(len(array[0])):
            pixel = array[col][row]
            red = GImage.getRed(pixel)
            green = GImage.getGreen(pixel)
            blue = GImage.getBlue(pixel)
            d_min = 500**2
            for i in range(len(PALETTE)):
                pre_red = PALETTE[i][0]
                pre_green = PALETTE[i][1]
                pre_blue = PALETTE[i][2]
                d = ((2 * (pre_red - red)**2) + (4 * (pre_green - green)**2) + (3 * (pre_blue - blue)**2) 
                    + ((((pre_red + red) / 2) * ((pre_red - red)**2) - ((pre_blue - blue)**2)) / 256))
                if d < d_min:
                    d_min = d
                    new_pixel = GImage.createRGBPixel(pre_red, pre_green, pre_blue)
            array[col][row] = new_pixel
    return GImage(array)

# Creates a new GImage from the original by tiling pixels

def pixelize(image):
    array = image.getPixelArray()
    length = len(array)
    width = len(array[0])
    for col in range(0, length, TILE_SIZE):
        for row in range(0, width, TILE_SIZE):
            pixel = array[col - (TILE_SIZE // 2)][row - (TILE_SIZE // 2)]
            for i in range(col - TILE_SIZE - 1, col + 1):
                for j in range(row - TILE_SIZE - 1, row + 1):
                    array[i][j] = pixel
    return GImage(array)

# Startup code

if __name__ == "__main__":
    ImageShop()
