*
.include 'D_Flip_Flop_schem_netlist.cdl'
*
.include 'C5N_models_Glade.txt'
*
.GLOBAL vdd vss
vdd vdd 0 5v
vss vss 0 0v
vclk clk 0 pulse 5v 0 0n 0.1n 0.1n 9.9n 20n
vd_in D_in 0 pulse 5v 0 0n 0.1n 0.1n 39.9n 80n


xdff D_in clk Q_out Qn_out D_Flip_Flop

.tran .1ns 160ns

*
.end
