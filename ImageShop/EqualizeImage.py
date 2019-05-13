# file: EqualizeImage.py

'''
This program enhances an image via histogram equalization.
'''

from pgl import GImage
from GrayscaleImage import luminance

def createEqualizedImage(image):
	array = image.getPixelArray()
	equalized_array = equalizeArray(array)
	return GImage(equalized_array)

def equalizeArray(array):
	length = len(array)
	width = len(array[0])
	cumulative = computeCumulativeHistogram(array)
	for col in range(length):
		for row in range(width):
			pixel = array[col][row]
			new_lum = (255 * cumulative[luminance(pixel)]) // (length * width)
			new_pixel = GImage.createRGBPixel(new_lum, new_lum, new_lum)
			array[col][row] = new_pixel
	return array

def computeCumulativeHistogram(array):
	histogram = computeHistogram(array)
	cumulative = [histogram[1]]
	for i in range(1, len(histogram)):
		cumulative.append(cumulative[i - 1] + histogram[i])
	return cumulative

def computeHistogram(array):
	histogram = [0] * 256
	for col in range(len(array)):
		for row in range(len(array[0])):
			pixel = array[col][row]
			lum = luminance(pixel)
			histogram[lum] += 1
	return histogram