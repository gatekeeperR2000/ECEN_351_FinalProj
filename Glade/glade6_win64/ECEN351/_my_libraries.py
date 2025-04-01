from ui import *

gui=cvar.uiptr

# Opening Libs
mylibs = ["C5N", "PCELL", "C5N_std_lib", "C5N_std_lib_bad", "C5N_std_lib_chk", "buffer_example"]
nlib = len(mylibs)
libinit = [0 for i in range(nlib)]
for n in range(nlib):
    libinit[n] = library(mylibs[n]) 
    libinit[n].dbOpenLib("./"+mylibs[n])

gui.updateLibBrowser()

