Installing Glade on Windows (64 bit)
----------------------------------------------------------------------------

This version will autodetect whether to use OpenGL graphics or (if OpenGL
is not available) rendering using QPainter. You can disable OpenGL mode
if so required by setting the environment variable GLADE_USE_OPENGL to NO.

If you are using OpenGL, it is a good idea to turn vsync off. For example, if
using NVidia card, go to the Nvidia control panel and select 'Manage 3D
Settings' and set the feature 'Vertical sync' to 'Force off'.

NOTE: if you want to use libraries created with older versions of glade, you may
find this possible if you set the env var GLADE_READ_48_LIBS to 'yes'. This is
beause prior to version 4.4.44, most Linux versions used Qt4, rather than Qt5,
and the binary format used to wriite the libraries has changed since. Similarly,
it *is* possible for glade version 4.4.44 and beyond to write libraries
compatible with older versions using the env var GLADE_WRITE_48_LIBS, but this
is strongly discouraged.

1. 	Unzip the glade6_win64.zip file to any directory

2.	Run the VC_redist.x64 application, to install the VC++ 2022
	redistributables.

3. 	Set the environment variable GLADE_HOME to this directory.
	To set an environment variable on Windows 10, open the Control Panel,
	click on 'System and Security', click on 'System', then click on
	'Advanced system settings'. Click on the 'Environment Variables...'
	button and then click 'New...' to add the env var.

4. 	Add %GLADE_HOME% to your PATH environment variable

5. 	Add %GLADE_HOME% to your PYTHONPATH environment variable.
	If you are using PCells, you will also need to make sure the directory 
	they reside in is in your PYTHONPATH.
	*** DO NOT *** set PYTHONHOME on Windows; if incorrectly set Glade will
	silently abort during Python initialisation!

6.	For running drc/extraction etc. it is recommended that you set the env var
	GLADE_DRC_WORK_DIR to a writeable directory to use for temp file creation.
	Some other env vars you may wish to set include GLADE_DRC_FILE (seeds the
	DRC dialog), GLADE_EXT_FILE (seeds the LPE dialog) , GLADE_NETLIST_FILE 
	(seeds the LVS dialog), GLADE_LOGFILE_DIR (the directory where GLade
	logfiles are written).

7. 	You can make a shortcut to glade.exe and drag the shortcut
	onto the quick launch toolbar or on the desktop for easy launching.

8.	If you want to set up file associations so that e.g. double clicking
	on a GDS2 file starts Glade and imports the GDS file. Here is how 
	to do it in Windows 10:

	- Right click on any gds2 file icon. Select 'Properties', then click on
	  the 'Change' button in the dialog. Select 'More Apps' iand 'Look for
	  ianother app on this PC'. Select Glade as the program you wish to open 
	  this file with (you may need to use the browse button to find the 
	  location of your glade.exe file).

	- Glade will now start up automatically when the gds2 file is double
	  clicked on. This also works for Oasis files. If you want Glade to read
	  in a technology file before loading the GDS file, you can do this by
	  creating a .glade.py file in your home directory (under Windows, you
	  must set an environment variable HOME to point to this directory). The
	  .glade.py file is read before loading any files, so you could load a
	  techfile by adding the line:

	  ui().importTech("default", "myTechFileName")


The library 'example', the DRC rules file 'drc.py', the extraction rules 
file 'extract.py' and technology file 'example.tch' are provided as examples.

Please read the Glade documentation which can be found by clicking on the
Help->Contents... menu item, or pressing the F1 key.

A user forum for help and suggestions is at https://www.peardrop.co.uk


----------------------------------------------------------------------------

Legal mumbo-jumbo:

   	This package is provided "as is" and without any express or implied
   	warranties, including, without limitation, the implied warranties oF
   	merchantability and fitness for a particular purpose.

   	Various portions of this package are copyright:

		LEF/DEF interface: Cadence Design Systems and Si2
		(http://openeda.si2.org)

		Python: http://www.python.org

		SWIG: http://www.swig.org

		Qt: (http://www.qt.io)

		OpenGL: http://www.opengl.org

		BugSlayer: John Robbins (http://www.wintellect.com)

		Capo: University of Michigan 
		(http://vlsicad.eecs.umich.edu/BK/PDtools/Capo)

		zlib: http://www.zlib.org

		Gemini: Carl Ebeling (http://www.cs.washington.edu)

		Fastcap: MIT (http://www.rle.mit.edu/cpg/research_codes.htm)

----------------------------------------------------------------------------
