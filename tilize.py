#!/usr/bin/env python

# Write every n-th frame into a single image
# Author: Sascha Hagedorn

import cv,sys,math,os,time

movie = sys.argv[1]
capture = cv.CaptureFromFile(movie)
totalFrames = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT)
fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
captureWidth = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)
captureHeight = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)

# final poster to be 100x70 minus 2cm border on each side
# final image width in cm
imageWidthInCm = 66
# final image height in cm
imageHeightInCm = 96
# well, the dpi of the final image
dpi = 300
# tile width in cm
tileWidthInCm = 2
# tile height in cm
tileHeightInCm = captureHeight / captureWidth * tileWidthInCm
# tile width in px
tileWidthInPx = int(math.floor(dpi * tileWidthInCm / 2.54))
# tile height in px
tileHeightInPx = int(math.floor(dpi * tileHeightInCm / 2.54))
# tiles per row
tilesPerRow = int(math.floor(imageWidthInCm / tileWidthInCm))
# tiles per column
tilesPerColumn = int(math.floor(imageHeightInCm / tileHeightInCm))

skip = math.floor(totalFrames / (tilesPerRow * tilesPerColumn))
width = tileWidthInPx*tilesPerRow
height = tileHeightInPx*tilesPerColumn
image = cv.CreateImage((width, height), 8, 3)
currentFrame = skip - 1
totalTilesPlaced = 0
currentRow = 0
currentColumn = 0
start = time.time()

print "file: %s" % movie
print "frames: %d" % totalFrames
print "fps: %d" % fps
print "skip: %d" % skip
print "frame width: %d" % captureWidth
print "frame height: %d" % captureHeight
print "tiles: %d" % (tilesPerRow * tilesPerColumn)
print "tile rows: %d" % tilesPerColumn
print "tile columns: %d" % tilesPerRow
print "tile width: %dpx" % tileWidthInPx
print "tile height: %dpx" % tileHeightInPx
print "image width: %dpx" % width
print "image height: %dpx" % height

while(totalTilesPlaced < tilesPerRow * tilesPerColumn):
	try:
		frame = cv.QueryFrame(capture)

		if currentFrame % skip == 0:
			smallImage = cv.CreateImage((tileWidthInPx, tileHeightInPx), 8, 3)
			cv.Resize(frame, smallImage)

			cv.SetImageROI(smallImage, (0, 0, tileWidthInPx, tileHeightInPx))
			x = currentColumn*tileWidthInPx
			y = currentRow*tileHeightInPx

			if ((x <= width-tileWidthInPx) and (y <= height-tileHeightInPx)):
				cv.SetImageROI(image, (x, y, tileWidthInPx, tileHeightInPx))
				cv.Add(image, smallImage, image, None)
			
			cv.ResetImageROI(image)
			cv.ResetImageROI(smallImage)

			totalTilesPlaced += 1
			currentColumn += 1

			if currentColumn != 0 and currentColumn % tilesPerRow == 0:
				currentColumn = 0
				currentRow += 1

			sys.stdout.write("\rplaced tile %d of %d (%d%%) " % (totalTilesPlaced, tilesPerRow * tilesPerColumn, int(float(totalTilesPlaced)/(tilesPerRow*tilesPerColumn)*100)))
			sys.stdout.flush()
		currentFrame += 1
	except:
		print "Unexpected error:", sys.exc_info()[0]
		cv.SaveImage("result-temp.jpg", image)

print "\nsaving image ..."
cv.SaveImage("%s-tiled.jpg" % os.path.basename(movie), image)
print "done in %.2f minutes" % ((time.time() - start) / 60.0)
