#------------------------------------------------------------------------------
#
# Poly resistor Pcell example for python3. 
#       Takes 3 parameters - w (width) , r (resistance)
#       and numsegs (number of resistor segments)
#
# Note: The first argument is always the cellView of the subMaster.
#       All subsequent arguments should have default values and will
#       be passed by name
#       This Pcell uses w/l units of metres. This is compatible with schematics
#       where the symbols have values of e.g. w=2u (spice syntax)
#
#------------------------------------------------------------------------------

# Import the db wrappers
from ui import *

# The entry point. The function name *must* match the filename.
def rppolywo(cv, w=0.66e-6, r=5000.0, numsegs=1) :
	lib = cv.lib()
	tech = lib.tech()
	dbu = float(cv.dbu())
	width = int(round(w / dbu ))
	res = float(r)

	# Get the rules. Error if they are missing.
	cut_width = tech.getLayerWidth('cont', 'drawing')
	if cut_width <= 0 :
		print('Error: No width rule for layer cont')
		raise ValueError
	cut_space = tech.getLayerSpacing('cont', 'drawing')
	if cut_space <= 0 :
		print('Error: No spacing rule for layer cont')
		raise ValueError
	poly_width = tech.getLayerWidth('polyg', 'drawing')
	if poly_width <= 0 :
		print('Error: No width rule for layer polyg')
		raise ValueError
	poly_space = tech.getLayerSpacing('polyg', 'drawing')
	if poly_space <= 0 :
		print('Error: No space rule for layer polyg')
		raise ValueError
	poly_to_cut = tech.get2LayerSpacing('cont', 'drawing', 'polyg', 'drawing')
	if poly_to_cut <= 0 :
		print('Error: No space rule for layer cont to layer polyg')
		raise ValueError
	poly_ovlp_cut = tech.getLayerEnc('polyg', 'drawing', 'cont', 'drawing')
	if poly_ovlp_cut <= 0 :
		print('Error: No enclosure rule for layer cont by layer polyg')
		raise ValueError
	rpo_ovlp_poly = tech.getLayerEnc('rpo', 'drawing', 'polyg', 'drawing')
	if rpo_ovlp_poly <= 0 :
		print('Error: No enclosure rule for layer polyg by layer rpo')
		raise ValueError
	pplus_ovlp_poly = tech.getLayerEnc('pimp', 'drawing', 'polyg', 'drawing')
	if pplus_ovlp_poly <= 0 :
		print('Error: No enclosure rule for layer polyg by layer pimp')
		raise ValueError
	rpo_space_cut = tech.get2LayerSpacing('rpo', 'drawing', 'cont', 'drawing')
	if rpo_space_cut <= 0 :
		print('Error: No space rule for layer rpo to layer cont')
		raise ValueError
	metal_ovlp_cut = tech.getLayerEnc('metal1', 'drawing', 'cont', 'drawing')
	if metal_ovlp_cut <= 0 :
		print('Error: No enclosure rule for layer cont by layer metal1')
		raise ValueError

	# Check width is OK
	if width < poly_width :
		print('Width is less than design rule!')

	# Sheet res in ohms/square
	rho = 1000.0
	bendFactor = 0.56
	
	# length is the length of the resistor body
	length = int(res * width / rho)

	# Create poly
	layer = tech.getLayerNum('polyg', 'drawing')

	# resistor may have bends - use a path
	bendLength = (poly_space + poly_width) * (numsegs - 1)
	mainLength = (length - bendLength) / numsegs
	# Adjust length for centre cut to rpo
	mainLength = mainLength - 2 * (cut_width/2 + rpo_space_cut)
	# Todo: adjust for number of bends	
	numPoints = numsegs * 2
	xpts = intarray(numPoints)
	ypts = intarray(numPoints)
	i = 0
	while i < numPoints :
		xpts[i]   = int(width/2 + i * (width + poly_space))
		xpts[i+1] = int(width/2 + i * (width + poly_space))
		# Alternate the Y points per segment
		if (i/2 % 2) :
			ypts[i]   = int(width / 2 + mainLength)
			ypts[i+1] = int(width / 2)
		else :
			ypts[i]   = int(width / 2)
			ypts[i+1] = int(width / 2 + mainLength)
		i = i + 2

	# Save ptlist
	xsavepts = intarray(numPoints)
	ysavepts = intarray(numPoints)
	for i in range(0, numPoints) :
		xsavepts[i] = xpts[i]
		ysavepts[i] = ypts[i]

	# Extend by halfwidth
	ypts[0] = int(ypts[0] - width/2)
	if numsegs % 2 :
		ypts[numPoints-1] = int(ypts[numPoints-1] + width/2)
	else :
		ypts[numPoints-1] = int(ypts[numPoints-1] - width/2)
	poly = cv.dbCreatePath(xpts, ypts, numPoints, layer, width, 0, 0, 0)
	# Restore ptlist
	for i in range(0, numPoints) :
		xpts[i] = xsavepts[i]
		ypts[i] = ysavepts[i]

	# Create P+ layer overlapping poly
	layer = tech.getLayerNum('pimp', 'drawing')
	pplus_width = width + pplus_ovlp_poly * 2
	ypts[0] = int(ypts[0] - (width/2 + pplus_ovlp_poly))
	if numsegs % 2 :
		ypts[numPoints-1] = int(ypts[numPoints-1] + width/2 + pplus_ovlp_poly)
	else :
		ypts[numPoints-1] = int(ypts[numPoints-1] - (width/2 + pplus_ovlp_poly))
	pplus = cv.dbCreatePath(xpts, ypts, numPoints, layer, pplus_width, 0, 0, 0)
	# Restore ptlist
	for i in range(0, numPoints) :
		xpts[i] = xsavepts[i]
		ypts[i] = ysavepts[i]

	# Create rpo 
	layer = tech.getLayerNum('rpo', 'drawing')
	rpo_width = width + rpo_ovlp_poly * 2
	ypts[0] = int(ypts[0] - width/2 + (poly_ovlp_cut + cut_width + rpo_space_cut))
	if numsegs % 2 :
		ypts[numPoints-1] = int(ypts[numPoints-1] + width/2 - (poly_ovlp_cut + cut_width + rpo_space_cut))
	else :
		ypts[numPoints-1] = int(ypts[numPoints-1] - width/2 + (poly_ovlp_cut + cut_width + rpo_space_cut))
	rpo = cv.dbCreatePath(xpts, ypts, numPoints, layer, rpo_width, 0, 0, 0)
	# Restore ptlist
	for i in range(0, numPoints) :
		xpts[i] = xsavepts[i]
		ypts[i] = ysavepts[i]

	# Create contacts
	layer = tech.getLayerNum('cont', 'drawing')
	numCuts = int((width + cut_space - 2 * poly_ovlp_cut) / (cut_width + cut_space))
	xoffset = int(( width - numCuts * cut_width - (numCuts-1) * cut_space) / 2)
	yoffset = poly_ovlp_cut
	for i in range(numCuts) :
		# contacts at start
		cut = Rect(int(xpts[0]-width/2),           int(ypts[0]-width/2), 
		           int(xpts[0]-width/2+cut_width), int(ypts[0]-width/2+cut_width))
		cut.offset(xoffset, yoffset)
		cv.dbCreateRect(cut, layer)
		# contacts at end
		if numsegs % 2 :
			cut2 = Rect(int(xpts[numPoints-1]-width/2),           int(ypts[numPoints-1]+(width/2-cut_width)), 
			            int(xpts[numPoints-1]-width/2+cut_width), int(ypts[numPoints-1]+width/2))
			cut2.offset(xoffset, -yoffset)
		else :
			cut2 = Rect(int(xpts[numPoints-1]-width/2),           int(ypts[numPoints-1]-(width/2-cut_width)), 
			            int(xpts[numPoints-1]-width/2+cut_width), int(ypts[numPoints-1]-width/2))
			cut2.offset(xoffset, yoffset)
		cv.dbCreateRect(cut2, layer)
		xoffset = int(xoffset + cut_width + cut_space)
	# Restore ptlist
	for i in range(0, numPoints) :
		xpts[i] = xsavepts[i]
		ypts[i] = ysavepts[i]

	# Create metal for 1st pin
	layer = tech.getLayerNum('metal1', 'drawing')
	met = Rect(int(xpts[0]-width/2), int(ypts[0]-width/2), 
	           int(xpts[0]+width/2), int(ypts[0]-width/2 + cut_width + metal_ovlp_cut*2))

	plus = cv.dbCreateRect(met, layer)
	net = cv.dbCreateNet('PLUS')
	pin = cv.dbCreatePin('PLUS', net, DB_PIN_INPUT)
	cv.dbCreatePort(pin, plus)

	# Create metal for 2nd pin
	if numsegs % 2 :
		met = Rect(int(xpts[numPoints-1]-width/2), int(ypts[numPoints-1] + width/2), 
	               int(xpts[numPoints-1]+width/2), int(ypts[numPoints-1] + width/2 - cut_width - metal_ovlp_cut*2))
	else :
		met = Rect(int(xpts[numPoints-1]-width/2), int(ypts[numPoints-1] - width/2), 
	               int(xpts[numPoints-1]+width/2), int(ypts[numPoints-1] - width/2 + cut_width + metal_ovlp_cut*2))

	minus = cv.dbCreateRect(met, layer)
	net = cv.dbCreateNet('MINUS')
	pin = cv.dbCreatePin('MINUS', net, DB_PIN_INPUT)
	cv.dbCreatePort(pin, minus)
	
	# Device type
	cv.dbAddProp('type', 'res')

	# Commit to db
	cv.update()

