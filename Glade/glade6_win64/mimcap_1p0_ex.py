#------------------------------------------------------------------------------
#
# MIMCAP Pcell for extraction
#
# Note: The first argument is always the cellView of the subMaster.
#       All subsequent arguments should have default values and will
#       be passed by name. Each argument should be seperated by a comma
#       and whitespace.
#       Note the recognition region point list is always passed in dbu.
#
#------------------------------------------------------------------------------

# Import the db wrappers
from ui import *

# The entry point. The function name *must* match the filename.
def mimcap_1p0_ex(cv, ptlist=[[0,0],[1000,0],[1000,1000],[0,1000]]) :
	lib = cv.lib()
	dbu = lib.dbuPerUU()
	# Create the recognition region shape
	npts = len(ptlist)
	xpts = intarray(npts)
	ypts = intarray(npts)
	for i in range (npts) :
		xpts[i] = ptlist[i][0]
		ypts[i] = ptlist[i][1]
	# for
	cv.dbCreatePolygon(xpts, ypts, npts, TECH_Y0_LAYER);
	# Create pins
	net1 = cv.dbCreateNet('PLUS')
	cv.dbCreatePin('PLUS', net1, DB_PIN_INOUT)
	net2 = cv.dbCreateNet('MINUS')
	cv.dbCreatePin('MINUS', net2, DB_PIN_INOUT)

	# Set the device modelName property for netlisting
	cv.dbAddProp('modelName', 'mimcap_1p0')

    # Set the netlisting property
	cv.dbAddProp('NLPDeviceFormat', '[@instName] [|PLUS:%] [|MINUS:%] [@modelName] [@w:w=%] [@sp:sp=%] [@lr:lr=%] [@nr:nr=%]')

	# Device type
	cv.dbAddProp('type', 'cap')

	# Commit to db
	cv.update()
#
