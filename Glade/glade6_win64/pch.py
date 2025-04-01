#------------------------------------------------------------------------------
#
# PMOS Pcell example. 
#	    Create a Pcell with parameters w (width of gate),
#	    l (length of gate), nf (number of gate fingers).
#
# Note: The first argument is always the cellView of the subMaster.
#       All subsequent arguments should have default values and will
#       be passed by name. Each argument should be seperated by a comma
#	    and whitespace. 
#       This Pcell uses w/l units of metres. This is compatible with schematics
#       where the symbols have values of e.g. w=2u (spice syntax)
#
#------------------------------------------------------------------------------

# Import the db wrappers
from ui import *

# The entry point. The function name *must* match the filename.
def pch(cv, w=1.1e-6, l=0.13e-6, nf=1, polyCnt=False, leftCnt=True,
rightCnt=True) :
	lib = cv.lib()
	tech = lib.tech()
	dbu = float(cv.dbu())
	width = int(round(w / dbu ))
	length = int(round(l / dbu ))
	fingers = int(nf)

	# Get the rules. Error if they are missing.
	cut_width = tech.getLayerWidth('cont', 'drawing')
	if cut_width <= 0 :
		print('No width rule for layer cont')
		raise ValueError
	cut_space = tech.getLayerSpacing('cont', 'drawing')
	if cut_space <= 0 :
		print('No spacing rule for layer cont')
		raise ValueError
	nwell_ovlp_active = tech.getLayerEnc('nwell', 'drawing', 'od', 'drawing')
	if nwell_ovlp_active <= 0 :
		print('No enclosure rule for layer od by layer nwell')
		raise ValueError
	poly_to_cut = tech.get2LayerSpacing('cont', 'drawing', 'polyg', 'drawing')
	if poly_to_cut <= 0 :
		print('No space rule for layer cont to layer polyg')
		raise ValueError
	active_ovlp_cut = tech.getLayerEnc('od', 'drawing', 'cont', 'drawing')
	if active_ovlp_cut <= 0 :
		print('No enclosure rule for layer cont by layer od')
		raise ValueError
	poly_ovlp_active = tech.getLayerExt('polyg', 'drawing', 'od', 'drawing')
	if poly_ovlp_active <= 0 :
		print('No extension rule for layer od by layer poly')
		raise ValueError
	poly_ovlp_cut = tech.getLayerEnc('polyg', 'drawing', 'cont', 'drawing')
	if poly_ovlp_cut <= 0 :
		print('No enclosure rule for layer cont by layer poly')
		raise ValueError
	pplus_ovlp_active = tech.getLayerEnc('pimp', 'drawing', 'od', 'drawing')
	if pplus_ovlp_active <= 0 :
		print('No enclosure rule for layer od by layer pimp')
		raise ValueError
	metal_ovlp_cut = tech.getLayerEnc('metal1', 'drawing', 'cont', 'drawing')
	if metal_ovlp_cut <= 0 :
		print('No enclosure rule for layer cont by layer metal1')
		raise ValueError
	poly_via_size = int(cut_width + 2 * poly_ovlp_cut)
	poly_via_neck_offset = int(poly_via_size / 2 - length / 2)

	# Create active
	od = tech.getLayerNum('od', 'drawing')
	height = active_ovlp_cut*2 + cut_width*(fingers + 1) + poly_to_cut*2*fingers + length*fingers
	r = Rect(int(-height/2), int(-width/2), int(height/2), int(width/2))
	active = cv.dbCreateRect(r, od);

	# Create nwell
	nwell = tech.getLayerNum('nwell', 'drawing')
	r.bias(nwell_ovlp_active)
	nwell = cv.dbCreateRect(r, nwell);
	net = cv.dbCreateNet('B')
	pin = cv.dbCreatePin('B', net, DB_PIN_INPUT)
	cv.dbCreatePort(pin, nwell)

	# Create pplus
	pimp = tech.getLayerNum('pimp', 'drawing')
	r = Rect(int(-height/2 - pplus_ovlp_active), int(-width/2 - pplus_ovlp_active), 
		     int(height/2 + pplus_ovlp_active),  int(width/2 + pplus_ovlp_active))
	cv.dbCreateRect(r, pimp);

	# Create poly fingers
	poly = tech.getLayerNum('polyg', 'drawing')
	metal1 = tech.getLayerNum('metal1', 'drawing')
	cont = tech.getLayerNum('cont', 'drawing')
	xoffset = int(active_ovlp_cut + cut_width + poly_to_cut -height/2)
	for i in range(fingers) :
		p = Rect(int(xoffset),          int(-width/2 -poly_ovlp_active),
			     int(xoffset + length), int(width/2 + poly_ovlp_active))
		gate = cv.dbCreateRect(p, poly)
		net = cv.dbCreateNet('G')
		pin = cv.dbCreatePin('G', net, DB_PIN_INPUT)
		if polyCnt :
			numCuts = int(length / (cut_width + cut_space))
			xoffset = int(active_ovlp_cut + cut_width + poly_to_cut -height/2)
			if width < poly_via_size :
				q = Rect(int(xoffset - poly_via_neck_offset), int(width/2 + poly_ovlp_active),
					     int(xoffset + length + poly_via_neck_offset), int(width/2 + poly_ovlp_active + poly_via_size))
				cv.dbCreateRect(q, poly)
				metpin = cv.dbCreateRect(q, metal1)
				cv.dbCreatePort(pin, metpin)
			else :
				q = Rect(int(xoffset),          int(width/2 + poly_ovlp_active),
					     int(xoffset + length), int(width/2 + poly_ovlp_active + poly_via_size))
				cv.dbCreateRect(q, poly)
				metpin = cv.dbCreateRect(q, metal1)
				cv.dbCreatePort(pin, metpin)
			xfudge = int((length - numCuts * (cut_width + cut_space)) / 2)
			xoffset = int(active_ovlp_cut + cut_width + poly_to_cut + poly_ovlp_cut + xfudge -height/2)
			for j in range(numCuts) :
				r = Rect(int(xoffset),             int(width/2 + poly_ovlp_active + poly_ovlp_cut),
				 	     int(xoffset + cut_width), int(width/2 + poly_ovlp_active + poly_ovlp_cut + cut_width))
				cv.dbCreateRect(r, cont)
				xoffset = int(xoffset + cut_width + cut_space)
		else :
			cv.dbCreatePort(pin, gate)
		xoffset = int(xoffset + length + 2*poly_to_cut + cut_width)

	# Create S/D contacts
	cont = tech.getLayerNum('cont', 'drawing')
	numCuts = int((width - 2*active_ovlp_cut + cut_space) / (cut_width + cut_space))
	yfudge = int((width - numCuts * (cut_width + cut_space)) / 2)
	xoffset = int(active_ovlp_cut - height/2)
	if (leftCnt and rightCnt) :
		for i in range(fingers+1) :
			yoffset = int(active_ovlp_cut + yfudge -width/2 )
			for j in range(numCuts) :
				cut = Rect(0, 0, cut_width, cut_width)
				cut.offset(xoffset, yoffset)
				cv.dbCreateRect(cut, cont)
				yoffset = int(yoffset + cut_width + cut_space)
			xoffset = int(xoffset + length + 2*poly_to_cut + cut_width)
	if (leftCnt and not rightCnt) :
		for i in range(fingers+1) :
			yoffset = int(active_ovlp_cut + yfudge -width/2)
			for j in range(numCuts) :
				cut = Rect(0, 0, cut_width, cut_width)
				cut.offset(xoffset, yoffset)
				cv.dbCreateRect(cut, cont)
				yoffset = int(yoffset + cut_width + cut_space)
			xoffset = int(xoffset + length + 2*poly_to_cut + cut_width)
	if (not leftCnt and rightCnt) :
		for i in range(fingers+1) :
			int(yoffset = active_ovlp_cut + yfudge -width/2)
			for j in range(numCuts) :
				cut = Rect(0, 0, cut_width, cut_width)
				cut.offset(xoffset, yoffset)
				cv.dbCreateRect(cut, cont)
				yoffset = int(yoffset + cut_width + cut_space)
			xoffset = int(xoffset + length + 2*poly_to_cut + cut_width)
			
	# Create metal
	metal1 = tech.getLayerNum('metal1', 'drawing')
	xoffset = int(active_ovlp_cut - metal_ovlp_cut - height/2)
	for i in range(fingers+1) :
		met = Rect(0, int(-width/2), cut_width + 2*metal_ovlp_cut, int(width/2))
		met.offset(xoffset, 0)
		if (i+1) % 2 :
			source = cv.dbCreateRect(met, metal1)
			net = cv.dbCreateNet('S')
			pin = cv.dbCreatePin('S', net, DB_PIN_INOUT)
			cv.dbCreatePort(pin, source)
		else :
			drain = cv.dbCreateRect(met, metal1)
			net = cv.dbCreateNet('D')
			pin = cv.dbCreatePin('D', net, DB_PIN_INOUT)
			cv.dbCreatePort(pin, drain)
		xoffset = int(xoffset + length + 2*poly_to_cut + cut_width)
	
	# Device type
	cv.dbAddProp('type', 'mos')

	# Commit to db the bounding box
	cv.update()
