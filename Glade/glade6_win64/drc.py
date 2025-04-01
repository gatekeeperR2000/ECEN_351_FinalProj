# 0.13um example DRC deck.
ui = cvar.uiptr

# Initialise DRC package. 
cv = ui.getEditCellView()
geomBegin(cv)

# Get raw layers
dnwell    = geomGetShapes("dnwell", "drawing")
nwell     = geomGetShapes("nwell", "drawing")
active    = geomGetShapes("od", "drawing")
od2       = geomGetShapes("od2", "drawing")
poly      = geomGetShapes("polyg", "drawing")
nimp      = geomGetShapes("nimp", "drawing")
pimp      = geomGetShapes("pimp", "drawing")
rpo       = geomGetShapes("rpo", "drawing")
cont      = geomGetShapes("cont", "drawing")
metal1    = geomGetShapes("metal1", "drawing")
via12     = geomGetShapes("via12", "drawing")
metal2    = geomGetShapes("metal2", "drawing")
via23     = geomGetShapes("via23", "drawing")
metal3    = geomGetShapes("metal3", "drawing")

# Form derived layers
psub      = geomNot(nwell)
gate      = geomAnd(poly, active)
polycon   = geomAnd(poly, cont)
activecon = geomAnd(active, cont)
allcon    = geomOr(polycon, activecon)
badcon    = geomAndNot(allcon, metal1)
diff      = geomAndNot(active, gate)
ndiff     = geomAnd(diff, nimp)
pdiff     = geomAnd(diff, pimp)
ntap      = geomAnd(ndiff, nwell)
ptap      = geomAndNot(pdiff, nwell)
npimp     = geomOr(nimp, pimp)
rwell     = geomAnd(psub, dnwell)
widem1    = geomSize(geomSize(metal1, -10.0), 10.0)
widem2    = geomSize(geomSize(metal2, -10.0), 10.0)
widem3    = geomSize(geomSize(metal3, -10.0), 10.0)

# Form connectivity
geomConnect( [
              [ptap, pdiff, psub],
              [ntap, ndiff, nwell],
              [cont, ndiff, pdiff, poly, metal1],
              [via12, metal1, metal2],
              [via23, metal2, metal3],
	     ] )

if geomNumShapes(nwell) > 0 :
	print("Check nwell")
	geomWidth(nwell, 1.8, "NW width < 0.62 (NW.W.1)")
	geomSpace(nwell, 0.62, samenet, "NW space < 0.62 (NW.S.1)")
	geomSpace(nwell, 1.0, diffnet, "NW space (different net) < 1.0 (NW.S.2)")
	geomArea(nwell, 1.0, 9e99, "NW area < 1.0 (NW.A.1)")
	geomHoleArea(nwell, 1.0, 9e99, "NW enclosed area < 0.384 (NW.A.2)")

if geomNumShapes(dnwell) > 0 :
	print("Check dnwell")
	geomWidth(dnwell, 3.0, "DNW width < 3.0 (DNW.W.1)")
	geomSpace(dnwell, 5.0, "DNW space < 5.0 (DNW.S.1)")
	geomSpace(dnwell, nwell, 3.5, diffnet, "DNW space to NW (different net) < 3.5 (DNW.S.2)")
	geomSpace(rwell, geomOr(rwell, psub), 1.0, "RW space to {RW or PW} < 1.0 (DNW.S.3)")
	geomSpace(geomOr(rwell, psub), geomInteracts(rwell, od2), diffnet, 1.2, "RW or PW space to RW interact OD2 (different net) < 1.2 (DNW.S.4)")
	geomSpace(dnwell, ndiff, 2.93, "DNW space to N+ACTIVE < 2.93 (DNW.S.5)")
	geomEnclose(nwell, dnwell, 1.5, "Recommended NW enclosure of DNW < 1.5 (DNW.EN.1)")
	geomOverlap(nwell, dnwell, 2.0, "DNW overlap NW < 2.0 (DNW.O.1)")

if geomNumShapes(active) > 0 :
	print("Check active")
	geomWidth(active, 0.15, "OD width < 0.15 (OD.W.1)")
	geomSpace(active, 0.21, 0, "OD space < 0.21 (OD.S.1)")
	geomNotch(active, 0.21, 0, "OD notch < 0.21 (OD.S.1)")
	geomSpace(ndiff, nwell, 0.31, 0, "N+ACTIVE space to NW < 0.31 (OD.S.3)")
	geomSpace(pdiff, nwell, 0.24, 0, "P+ACTIVE space to NW < 0.24 (OD.S.4)")
	geomEnclose(nwell, ndiff, 0.24, "NW enclosure of N+ACTIVE < 0.24 (OD.EN.1)")
	geomEnclose(nwell, pdiff, 0.31, "NW enclosure of P+ACTIVE < 0.31 (OD.EN.2)")
	geomArea(active, 0.122, 9e99, "OD area < 0.122 (OD.A.1)")
	geomHoleArea(active, 0.122, 9e99, "OD enclosed area < 0.122 (OD.A.2)")

if geomNumShapes(od2) > 0 :
	print("Check OD2")
	geomWidth(od2, 0.62, "OD2 width < 0.62 (OD2.W.1)")
	geomSpace(od2, 0.86, "OD2 space < 0.86 (OD2.S.1)")
	geomSpace(od2, geomOr(diff, gate), 0.27, "OD2 space to ACTIVE or GATE < 0.27 (OD2.S.2)")
	geomSpace(od2, nwell, 0.62, "OD2 space to NW < 0.62 (OD2.S.4)")
	geomEnclose(od2, gate, 0.34, "OD2 enclose GATE in S/D direction (OD2.EN.1)")
	geomExtension(od2, geomOr(diff, gate), 0.27, "OD2 extension on ACTIVE or GATE < 0.27 (OD2.EX.1)")
	geomExtension(nwell, od2, 0.62, "NW extension on OD2 < 0.62 (OD2.EX.2)")
	geomExtension(od2, nwell, 0.62, "OD2 extension on NW < 0.62 (OD2.EX.3)")
	geomOverlap(od2, nwell, 0.62, "OD2 overlap of NW < 0.62 (OD2.O.1)")

if geomNumShapes(poly) > 0 :
	print("Check poly")
	geomWidth(poly, 0.13, "PO width < 0.13 (PO.W.3)")
	geomSpace(poly, 0.18, 0, "PO space < 0.18 (PO.S.1)")
	geomNotch(poly, 0.18, 0, "PO notch < 0.18 (PO.S.1)")
	geomSpace(poly, active, 0.07, 0, "Field PO space to OD < 0.07 (PO.S.4)")
	geomExtension(poly, active, 0.18, "PO Extension on OD < 0.18 (PO.EX.1)")
	geomExtension(active, gate, 0.23, "OD extension on PO < 0.23 (PO.EX.2)")
	geomArea(poly, 0.09, 9e99, "PO area < 0.09 (PO.A.1)")
	geomHoleArea(poly, 0.15, 9e99, "PO enclosed area < 0.09 (PO.A.2)")
	geomEnclose(npimp, poly, 0.2, "NP or PP enclose PO < 0.2 (NP.EN.1, PP.EN.1)")

if geomNumShapes(nimp) > 0 :
	print("Check nimp")
	geomWidth(nimp, 0.31, "NP width < 0.31 (NP.W.1)")
	geomSpace(nimp, 0.31, 0, "NP space < 0.31 (NP.S.1)")
	geomNotch(nimp, 0.31, 0, "NP notch < 0.31 (NP.S.1)")
	geomSpace(pdiff, nimp, 0.18, 0, "NP space to P+ACTIVE < 0.18 (NP.S.2)")
	geomSpace(ptap, nimp, 0.03, 0, "NP space to P+STRAP < 0.18 (NP.S.3)")
	geomOverlap(nimp, active, 0.18, "NP overlap OD < 0.18 (NP.O.1)")
	geomArea(nimp, 0.25, 9e99, "NP area < 0.25 (NP.A.1)")
	geomArea(geomHoles(nimp), 0.25, 9e99, "NP enclosed area < 0.25 (NP.A.2)")
	badnp = geomAnd(pimp, nimp)
	saveDerived(badnp, "NP/PP overlap not allowed (NP.R.2 / PP.R.2)")

if geomNumShapes(pimp) > 0 :
	print("Check pimp")
	geomWidth(pimp, 0.31, "PP width < 0.31 (PP.W.1)")
	geomSpace(pimp, 0.31, 0, "PP space < 0.31 (PP.S.1)")
	geomNotch(pimp, 0.31, 0, "PP notch < 0.31 (NP.S.1)")
	geomSpace(ndiff, pimp, 0.18, 0, "PP space to N+ACTIVE < 0.18 (PP.S.2)")
	geomSpace(ntap, pimp, 0.03, 0, "PP space to N+STRAP < 0.18 (PP.S.3)")
	geomOverlap(pimp, active, 0.18, "PP overlap OD < 0.18 (PP.O.1)")
	geomArea(pimp, 0.25, 9e99, "PP area < 0.25 (PP.A.1)")
	geomArea(geomHoles(pimp), 0.25, 9e99, "PP enclosed area < 0.25 (PP.A.2)")

if geomNumShapes(rpo) > 0 :
	print("Check rpo")
	geomWidth(rpo, 0.43, "RPO width < 0.43 (RPO.W.1)")
	geomSpace(rpo, 0.43, 0, "RPO space < 0.43 (RPO.S.1)")
	geomNotch(rpo, 0.43, 0, "RPO notch < 0.43 (RPO.S.1)")
	geomSpace(rpo, active, 0.22, 0, "RPO space to OD < 0.22 (RPO.S.2)")
	geomSpace(rpo, cont, 0.22, 0, "RPO space to CO < 0.22 (RPO.S.3)")
	geomSpace(rpo, gate, 0.38, 0, "RPO space to gate < 0.38 (RPO.S.4)")
	geomSpace(rpo, poly, 0.22, 0, "RPO space to PO < 0.3 (RPO.S.5)")
	geomExtension(rpo, active, 0.22, "RPO Extension on OD < 0.22 (RPO.EX.1)")
	geomExtension(active, rpo, 0.22, "OD Extension on RPO < 0.22 (RPO.EX.2)")
	geomArea(rpo, 1.0, 9e99, "RPO area < 1.0 (RPO.A.1)")
	geomHoleArea(rpo, 1.0, 9e99, "RPO enclosed area < 1.0 (RPO.A.2)")

if geomNumShapes(cont) > 0 :
	print("Check cont")
	geomWidth(cont, 0.16, "CO width < 0.16 (CO.W.1)")
	geomArea(cont, 0.0256, 0.0256, "CO width != 0.16 (CO.W.1)")
	geomSpace(cont, 0.18, 0, "CO space < 0.18 (CO.S.1)")
	geomSpace(gate, cont, 0.11, 0, "CO space to gate < 0.11 (CO.S.3)")
	geomSpace(active, polycon, 0.14, 0, "CO inside PO space to OD < 0.14 (CO.S.5)")
	geomEnclose(active, cont, 0.07, "CO enclosure by OD < 0.07 (CO.EN.1)")
	geomEnclose(poly, cont, 0.07, "CO enclosure by PO < 0.07 (CO.EN.2)")
	geomEnclose(pimp, cont, 0.09, "CO enclose by PP < 0.09 (CO.EN.3)")
	geomEnclose(nimp, cont, 0.09, "CO enclose by NP < 0.09 (CO.EN.4)")

if geomNumShapes(metal1) > 0 :
	print("Check metal1")
	geomWidth(metal1, 0.16, "M1 width < 0.16 (M1.W.1)")
	geomWidth(metal1, 0.2, diagonal, "M1 diagonal width < 0.2 (M1.W.2)")
	geomSpace(metal1, 0.18, 0, "M1 space < 0.18 (M1.S.1)")
	geomNotch(metal1, 0.18, 0, "M1 notch < 0.18 (M1.S.1)")
	geomSpace(widem1, 0.6, "M1 space (width > 10u) < 0.6 (M1.S.2)")
	geomSpace2(metal1, 0.22, 0.3, 1.0, project, "M1 space with M1 width > 0.3 and length > 1.0 < 0.22 (M1.S.3)")
	geomSpace(metal1, 0.22, diagonal, "M1 diagonal space < 0.22 (M1.S.4)")
	geomEnclose2(metal1, cont, 0.0, 0.05, 0.05, 2, "M1 enclosure of CO (M1.EN.1 / M1.EN.2)")
	geomArea(metal1, 0.122, 9e99, "M1 area < 0.122 (M1.A.1)")
	geomHoleArea(metal1, 0.2, 9e99, "M1 enclosed area < 0.2 (M1.A.2)")

if geomNumShapes(via12) > 0 :
	print("Check via12")
	geomWidth(via12, 0.19, "VIA1 width < 0.19 (VIA1.W.1)")
	geomArea(via12, 0.0361, 0.0361, "VIA1 width != 0.19 (VIA1.W.1)")
	geomSpace(via12, 0.22, 0, "VIA1 space < 0.22 (VIA1.S.1)")
	geomEnclose2(metal1, via12, 0.01, 0.01, 0.05, 2, "M1 enclosure of VIA1 (VIA1.EN.1 / VIA1.EN.2)")
	saveDerived(geomGetNon90(via12), "45 degree VIA1 not allowed (VIA1.R.1)")

if geomNumShapes(metal2) > 0 :
	print("Check metal2")
	geomWidth(metal2, 0.2, "M2 width < 0.2 (M2.W.1)")
	geomWidth(metal2, 0.24, diagonal, "M2 diagonal width < 0.24 (M2.W.2)")
	geomSpace(metal2, 0.21, 0, "M2 space < 0.21 (M2.S.1)")
	geomNotch(metal2, 0.21, 0, "M2 notch < 0.21 (M2.S.1)")
	geomSpace(widem2, 0.6, "M2 space (width > 10u) < 0.6 (M2.S.2)")
	geomSpace2(metal2, 0.24, 0.39, 1.0, project, "M2 space with M2 width > 0.39 and length > 1.0 < 0.24 (M2.S.3)")
	geomSpace(metal2, 0.24, diagonal, "M2 diagonal space < 0.24 (M2.S.4)")
	geomEnclose2(metal2, via12, 0.005, 0.05, 0.05, 2, "M2 enclosure of VIA1 (M2.EN.1 / M2.EN.2)")
	geomArea(metal2, 0.144, 9e99, "M2 area < 0.144 (M2.A.1)")
	geomHoleArea(metal2, 0.265, 9e99, "M2 enclosed area < 0.265 (M2.A.2)")

if geomNumShapes(via23) > 0 :
	print("Check via23")
	geomWidth(via23, 0.19, "VIA2 width < 0.19 (VIA2.W.1)")
	geomArea(via23, 0.0361, 0.0361, "VIA2 width != 0.19 (VIA2.W.1)")
	geomSpace(via23, 0.22, 0, "VIA2 space < 0.22 (VIA2.S.1)")
	geomEnclose2(metal2, via23, 0.01, 0.01, 0.05, 2, "M2 enclosure of VIA2 (VIA2.EN.2)")
	saveDerived(geomGetNon90(via23), "45 degree VIA2 not allowed (VIA2.R.1)")

if geomNumShapes(metal3) > 0 :
	print("Check metal3")
	geomWidth(metal3, 0.2, "M3 width < 0.2 (M3.W.1)")
	geomWidth(metal3, 0.24, diagonal, "M3 diagonal width < 0.24 (M3.W.2)")
	geomSpace(metal3, 0.21, 0, "M3 space < 0.21 (M3.S.1)")
	geomNotch(metal3, 0.21, 0, "M3 notch < 0.21 (M3.S.1)")
	geomSpace(widem2, 0.6, "M3 space (width > 10u) < 0.6 (M3.S.2)")
	geomSpace2(metal3, 0.24, 0.39, 1.0, project, "M3 space with M3 width > 0.39 and length > 1.0 < 0.24 (M3.S.3)")
	geomSpace(metal3, 0.24, diagonal, "M3 diagonal space < 0.24 (M3.S.4)")
	geomEnclose2(metal3, via23, 0.005, 0.05, 0.05, 2, "M3 enclosure of VIA2 (M3.EN.1 / M3.EN.2)")
	geomArea(metal3, 0.144, 9e99, "M3 area < 0.144 (M3.A.1)")
	geomHoleArea(metal3, 0.265, 9e99, "M3 area < 0.265 (M3.A.2)")

# Add more metal layers as you like...

# Exit DRC package, freeing memory
geomEnd()
ui.winFit()
