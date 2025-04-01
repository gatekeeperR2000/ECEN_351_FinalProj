*
.include 'Diff_Amp_layout_netlist.cdl'
*
.include 'C5N_models_Glade.txt'
*
.GLOBAL vdd vss
xdiffamp vinp vout vinn ibias Diff_Amp
ibias vdd ibias 10u
vinp vinp 0 pwl 0 2.45 10u 2.55
vinn vinn 0 pwl 0 2.55 10u 2.45
ediff_in vin 0 vinp vinn 1
vdd vdd 0 5v
vss vss 0 0v

.tran .1u 10u 0 10p

*
.end
