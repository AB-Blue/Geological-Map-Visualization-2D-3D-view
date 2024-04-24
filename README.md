# Geological-Map-Visualization-2D-3D-view
--------------------------------------------------------------------------------------------------------------------------------------
Geological map/Interpreted horizons Visualization in 2D and 3D view 

in addition to the plotting of well-head locations (2D) and entire well trajectory (3D)

--------------------------------------------------------------------------------------------------------------------------------------
# Script files:

geological_mapping_2d_3d.py: Python

--------------------------------------------------------------------------------------------------------------------------------------

Author: Amir Abbas Babasafari (AB)

Date: April 2024

Email: a.babasafari@yahoo.com

--------------------------------------------------------------------------------------------------------------------------------------
# Installation Requirements:

Python 3.9

Libraries: numpy, pandas, matplotlib, pyvista, scipy

--------------------------------------------------------------------------------------------------------------------------------------
# Run the application:

Download the code from GitHub or clone the repository to your machine

Install the required dependencies using pip install 'library name'

Run the code on IDE

Please follow the steps below for plotting Geological Map:

Open a command prompt in the same directory as your python script is placed (just type 'cmd' in the address bar)

In the cmd shell please ensure you type the following arguments for 2D or 3D display as follows:

2D
"python geological_mapping_2d_3d.py plot2d 'Map/Horizon filepath' 'Wells_head filepath (optional)'"

Open the map file and specify line number to skip, X, Y, Z columns and type them respectively 

Open the well-head file and specify line number to skip, well name, X, Y columns and type them respectively 

3D
"python geological_mapping_2d_3d.py plot3d 'Map/Horizon filepath' 'Wells_trajectory folderpath (optional)'"

Open the map file and specify line number to skip, X, Y, Z columns and type them respectively 

Open one of the well track file and specify line number to skip, X, Y, Z columns and type them respectively 

--------------------------------------------------------------------------------------------------------------------------------------
# Notes:

Make sure there is not any space in the file/folder directory and file/folder names

Make sure all the well track files have the same parameters (line number to skip, X, Y, Z columns)

Well trajectory could be vertical, deviated, and horizontal

The last argument related to the well location (2D) and well trajectory (3D) are optional, so if not included, only map is plotted

The elevation is plotted with (-) sign

In 2D plot, the well locations are the coordinates provided in well head file and are not necessarily the locations where the wells reach the map 

--------------------------------------------------------------------------------------------------------------------------------------
# More information:

A full video on how to run the code step by step is available on my YouTube channel 

https://www.youtube.com/watch?v=5535GAPje14&t=1s 

https://www.linkedin.com/feed/update/urn:li:ugcPost:7188817464997072897/


