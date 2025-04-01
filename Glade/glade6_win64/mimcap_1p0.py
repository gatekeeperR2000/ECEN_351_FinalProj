###############################################################################
##
## mimcap_1p0.py
##
## Pcell with parameters w (width of finger), lr (length of finger), 
## nr (number of fingers)
##
## Copyright Keith Sabine (keith@peardrop.co.uk) 18/05/2020
##
###############################################################################

from ui import *
from utility import *

def mimcap_1p0( cv, w=0.2e-6, sp=0.21e-6, lr=5e-6, nr=26) :

	## Conversion factor, metres to dbu
	lib = cv.lib()
	dbu = float(cv.dbu())

	## Convert args and check
	if w < 0.2e-6 or w > 1e-5 :
		print('w parameter not in range 0.2u - 10u', w)
		w = 0.2e-6
	if sp < 0.21-6 or sp > 1e-5 :
		print('sp parameter not in range 0.21u - 10u', sp)
		sp = 0.21-6
	if lr < 1e-6 or lr > 1e-3 :
		print('lr parameter not in range 1.0u - 1000u', lr)
		l = 1.0e-6
	if nr < 1 :
		print('nr parameter must be > 0', nr)
		nr = 1

	wf = int(round(w / dbu))
	lf = int(round(lr / dbu))
	ws = int(round(sp / dbu))
	nf = int(nr)
	if nf <= 0 :
		print('Number of segments muct be an integer')
		raise ValueError

	## The techfile
	tech = lib.tech()

	## Via rules
	via_width = tech.getLayerWidth('via12', 'drawing')
	if via_width <= 0 :
		print('No width rule for layer via12')
		raise ValueError
	#
	via_space = tech.getLayerSpacing('via12', 'drawing')
	if via_space <= 0 :
		print('No spacing rule for layer via12')
		raise ValueError
	#

	## Metal rules
	met_ovlp_via = tech.getLayerEnc('metal2', 'drawing', 'via12', 'drawing')
	if met_ovlp_via <= 0 :
		print('No enclosure rule for layer via12 by layer metal2')
		raise ValueError
	#
	met_width = tech.getLayerWidth('metal2', 'drawing')
	if met_width  <= 0 :
		print('No width rule for layer metal2')
		raise ValueError
	#
	met_space = tech.getLayerSpacing('metal2', 'drawing' )
	if met_space <= 0 :
		print('No spacing rule for layer metal2')
		raise ValueError
	#

	## Layers.
	layer_list = [
					tech.getLayerNum('metal1', 'drawing'),
					tech.getLayerNum('metal2', 'drawing')
				 ]
	## Vias. There should be 1 less than the number of layers.
	via_list = [  
					tech.getLayerNum('via12', 'drawing')
			   ]
	cap_layer = tech.getLayerNum('cap', 'drawing')

	## Adjust min metal width - should be done in callback?
	if wf < met_width :
		wf = met_width
	#
	height = int(( wf * nf ) + ( ( nf - 1 ) * met_space ))
	pin_width = int((2 * met_ovlp_via ) + via_width)
	far_pin_start = int(pin_width + met_space + lf)

	## Define nets
	plus_net  = cv.dbCreateNet('PLUS')
	minus_net = cv.dbCreateNet('MINUS')

	## The left and right pin rectangles
	leftPinRect =  Rect( 0,             0, pin_width,                 height)
	rightPinRect = Rect( far_pin_start, 0, far_pin_start + pin_width, height)

	## Go thru the layers low to high and create mesh
	for lyr in range(0 , 2) :

		## Create the pin rectangles either side of mesh
		rp1 = cv.dbCreateRect(leftPinRect, layer_list[lyr])
		plus_pin = cv.dbCreatePin('PLUS', plus_net, DB_PIN_INOUT)
		cv.dbCreatePort(plus_pin, rp1)


		rp2 = cv.dbCreateRect(rightPinRect, layer_list[lyr])
		minus_pin = cv.dbCreatePin('MINUS', minus_net, DB_PIN_INOUT)
		cv.dbCreatePort(minus_pin, rp2)

		## foreach finger, create a rectangle. Stagger according to odd/even
		for f in range(nf) :
			if (f % 2) == 1 :
				## odd fingers. y is the offset of a single finger
				y = (( wf + met_space ) * f )
				box = Rect(  pin_width + met_space, y, 
				             far_pin_start,         y + wf)
				r = cv.dbCreateRect(box, layer_list[lyr])
			else :
				## even fingers
				y = wf + (( wf + met_space ) * f )
				box = Rect( pin_width,              y - wf, 
				            pin_width + lf,         y )
				r = cv.dbCreateRect(box, layer_list[lyr])
			#
		## for

		## Create vias for the pin rects. No via is needed for top layer.
		if lyr < 1 :
			fillRect(cv, leftPinRect,  layer_list[lyr], via_list[lyr]) 
			fillRect(cv, rightPinRect, layer_list[lyr], via_list[lyr]) 
		#

	## for layer

	## Draw the definition layer
	box = Rect( pin_width, 0, lf + pin_width + met_space, height)
	cv.dbCreateRect(box, cap_layer)

	## Device type
	cv.dbAddProp('type', 'cap')

	## Commit to db
	cv.update()
