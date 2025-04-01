###############################################################################
##
## utility.py
##
## Copyright Keith Sabine (keith@peardrop.co.uk) 18/05/2020
##
###############################################################################

from ui import *

###############################################################################
## Populate a rectangle with contacts.
## Args:
##     cellView  (dbId)
##     box       (Rect)
##     box layer (int)
##     cut layer (int)
## Return value: 
##     nil
###############################################################################
def fillRect(cv, box, boxLayer, cutLayer) :
	## The techfile
	lib = cv.lib()
	tech = lib.tech()	

	## Cut width
	cut_width = tech.getLayerWidth(cutLayer)
	if cut_width < 0 :
		print("No width rule for layer", cutLayer)
		raise ValueError

	cut_space = tech.getLayerSpacing(cutLayer)
	if cut_space < 0 :
		print("No spacing rule for layer", cutLayer)
		raise ValueError

	box_ovlp_cut = tech.getLayerEnc(cutLayer, boxLayer)
	if box_ovlp_cut < 0 :
		print("No enclosure rule of layer %d by layer", cutLayer, boxLayer)
		raise ValueError

	## Now work out how many rows and cols of cuts there can be
	## NB the following does not handle adjacent via rule... fix this
	## by estimating number of row/col cuts, if >= 2 then use larger
	## cut spacing.
	w = box.width()
	h = box.height()

	## Number of cuts per row i.e. x direction
	numRowCuts = int( (abs(w) - box_ovlp_cut) / (cut_width + cut_space))
	if numRowCuts == 0 :
		numRowCuts = 1

	## offset of cuts from left of box
	rowInitialOffset = box.left() + (w - numRowCuts * cut_width - (numRowCuts - 1) * cut_space) / 2

	## Number of cuts per col i.e. y direction
	numColCuts = int( (abs(h) - box_ovlp_cut) / (cut_width + cut_space))
	if numColCuts == 0 :
		numColCuts = 1

	## offset of cuts from bottom of box
	colInitialOffset = box.bottom() + (h - numColCuts * cut_width - (numColCuts - 1) * cut_space) / 2

	rowOffset = rowInitialOffset
	## for each row
	for row in range(numRowCuts) :
		## foreach col
		colOffset = colInitialOffset
		for col in range(numColCuts) :
			## Create a cut shape
			cut_rect = Rect( int(rowOffset),              int(colOffset),
					  	     int(rowOffset + cut_width),  int(colOffset + cut_width))
			cv.dbCreateRect(cut_rect, cutLayer)
			colOffset = colOffset + cut_width + cut_space
		rowOffset = rowOffset + cut_width + cut_space
