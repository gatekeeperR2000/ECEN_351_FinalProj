set GLADE_HOME=..
set PATH=%GLADE_HOME%;%PATH%
set PYTHONPATH=Python;..
set GLADE_LOGFILE_DIR=.
set GLADE_DRC_WORK_DIR=.
set GLADE_DRC_FILE=Python\C5N_DRC.py
set GLADE_EXT_FILE=Python\C5N_EXT_LVS.py
set GLADE_FASTCAP_WORK_DIR=.
del .\*.log
start /b ..\glade.exe -script .\_my_libraries.py -noOpenGL

