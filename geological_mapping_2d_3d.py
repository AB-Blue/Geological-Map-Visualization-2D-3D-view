""" 
Class for Geological map/Interpreted horizons Visualization in 2D and 3D view, 
in addition to the plotting of well-head locations (2D) and entire well trajectory (3D)
Python version: 3.9

Author: Amir Abbas Babasafari (AB)
Date: April 2024
Email: a.babasafari@yahoo.com   
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Readme:
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
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Notes:
Make sure there is not any space in the file/folder directory and file/folder names
Make sure all the well track files have the same parameters (line number to skip, X, Y, Z columns)
Well trajectory could be vertical, deviated, and horizontal
The last argument related to the well location (2D) and well trajectory (3D) are optional, so if not included, only map is plotted
The elevation is plotted with (-) sign
In 2D plot, the well locations are the coordinates provided in well head file and are not necessarily the locations where the wells reach the map 
"""

# Import Libraries
import os
import sys
import glob
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import pyvista as pv
from scipy.interpolate import griddata
import statistics


class plot_geological_map:
    def __init__(self):
        self.initialize()
        
    # initializing
    def initialize(self):
        self.xi = None
        self.yi = None
        self.zi = None
        self.well_pd = None
        self.map = None
        self.trajectory_dataset = None


    # method to plot map in a 2D view
    def plot_2d_map(self, map_path, map_header_info):

        # Get parameters from map header info
        map_header = list(np.array(map_header_info.split(',')).astype(int))
        skip_row = map_header[0]
        x_col = map_header[1]-1
        y_col = map_header[2]-1
        z_col = map_header[3]-1

        # Read data from the text file
        map = np.loadtxt(map_path, skiprows = skip_row, usecols=[x_col, y_col, z_col],dtype=(float))
        X = map[:, 0]  
        Y = map[:, 1]  
        Z = map[:, 2]  

        # For consistency the elevation is plotted with (-) sign
        if statistics.mean(Z) > 0:
            Z = -Z 

        # Define grid
        x_min, x_max = X.min(), X.max()
        y_min, y_max = Y.min(), Y.max()

        # User can adjust number of point for gridding
        point_no = 100
        xi = np.linspace(x_min, x_max, point_no) 
        yi = np.linspace(y_min, y_max, point_no) 
        self.xi, self.yi = np.meshgrid(xi, yi)

        # Interpolate Z values onto the grid
        self.zi = griddata((X, Y), Z, (self.xi, self.yi), method='linear')

        # Plot contour map
        plt.contour(self.xi, self.yi, self.zi, colors = 'black', levels=10)
        # Plot colored contour map
        image = plt.contourf(self.xi, self.yi, self.zi, levels=50, cmap='jet') 

        # divider = make_axes_locatable(ax) 
        # colorbar_axes = divider.append_axes("right", 
        #                                     size="5%", 
        #                                     pad=0.1) 
        # plt.colorbar(image, cax=colorbar_axes, label='Elevation')

        # Identify map name
        map_name = os.path.splitext(os.path.basename(map_path))[0] 
        
        plt.colorbar(image, label='Elevation')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f"Elevation Contour Map \n Map Name: {map_name}")
        plt.grid(True)


    # method to plot well locations in a 2D view
    def plot_2d_well(self, well_path, well_header_info):
        
        # Get parameters from well header info
        well_header = list(np.array(well_header_info.split(',')).astype(int))
        skip_row = well_header[0]
        well_col = well_header[1]-1
        x_col = well_header[2]-1
        y_col = well_header[3]-1

        # Read data from the text file and create a dataframe consists of well name, X, and Y coordinates
        wellname_pd = pd.DataFrame(np.loadtxt(well_path, skiprows = skip_row, usecols=[well_col], dtype=(str)),columns=['Well'])
        wellxy_pd = pd.DataFrame(np.loadtxt(well_path, skiprows = skip_row, usecols=[x_col, y_col], dtype={'names': ('X', 'Y'),
                            'formats': (float, float)}))
        self.well_pd = pd.concat([wellname_pd, wellxy_pd], axis=1)
        well_name = list(self.well_pd['Well'])
        well_X = list(self.well_pd['X'])
        well_Y = list(self.well_pd['Y'])

        for i, txt in enumerate(well_name):
            plt.scatter(well_X[i], well_Y[i], marker="o", c="black", s=50)
            plt.text(well_X[i], well_Y[i], txt, fontsize=16)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)


    # method to plot map in a 3D view
    def plot_3d_map(self, map_path, map_header_info):

        # Get parameters from map header info
        map_header = list(np.array(map_header_info.split(',')).astype(int))
        skip_row = map_header[0]
        x_col = map_header[1]-1
        y_col = map_header[2]-1
        z_col = map_header[3]-1

        # Read data from the text file
        self.map = np.loadtxt(map_path, skiprows = skip_row, usecols=[x_col, y_col, z_col],dtype=(float))
        X = self.map[:, 0] 
        Y = self.map[:, 1]  
        Z = self.map[:, 2]

        # For consistency the elevation is plotted with (-) sign
        if statistics.mean(Z) > 0:
            Z = -Z 

        # Convert data points to PyVista structured grid
        geological_grid = pv.StructuredGrid(X, Y, Z)
        print(geological_grid)

        # Create a colormap
        colormap = 'jet'  
        # geological_grid_scaled = geological_grid.scale([1,1,1])
        plotter.add_mesh(geological_grid, scalars = Z, cmap = colormap, show_scalar_bar = True, style = 'points')
        plotter.show_axes()
        plotter.show_bounds()


    # method to plot well trajectories in a 3D view
    def plot_3d_well(self, well_path, well_header_info):
        
        # Get parameters from well header info
        well_header = list(np.array(well_header_info.split(',')).astype(int))
        skip_row = well_header[0]
        x_col = well_header[1]-1
        y_col = well_header[2]-1
        z_col = well_header[3]-1

        # Read data from the text files (all well tracks) and create a dataframe consists of well name, X, Y, and Z coordinates
        trajectory_files = glob.glob(well_path + '\*.*')
        all_well_trajectory = []

        for file in trajectory_files:

            well_trajectory = pd.DataFrame(np.loadtxt(file, skiprows = skip_row, usecols=[x_col, y_col, z_col], dtype={'names': ('X', 'Y', 'Z'),
                                'formats': (float, float, float)}))
            well_name = os.path.splitext(os.path.basename(file))[0] 
            well_trajectory['well_name'] = np.repeat(well_name, len(well_trajectory['Z']))
            all_well_trajectory.append(well_trajectory)

        self.trajectory_dataset = pd.concat(all_well_trajectory, ignore_index=True)

        # For consistency the elevation is plotted with (-) sign
        if self.trajectory_dataset['Z'].mean() > 0:
            self.trajectory_dataset['Z'] = -self.trajectory_dataset['Z']

        # Identify well names
        well_names = self.trajectory_dataset['well_name'].unique().tolist()

        # Convert data points to PyVista structured grid for all well trajectories
        for i, n in enumerate(trajectory_files):

            x = np.array(self.trajectory_dataset['X'][self.trajectory_dataset['well_name'] == well_names[i]])
            y = np.array(self.trajectory_dataset['Y'][self.trajectory_dataset['well_name'] == well_names[i]])
            z = np.array(self.trajectory_dataset['Z'][self.trajectory_dataset['well_name'] == well_names[i]])
            wellbores_data = pv.StructuredGrid(x, y, z)

            plotter.add_mesh(wellbores_data, color='black')
            plotter.add_point_labels([x[0], y[0], z[0]], [well_names[i]], font_size=20, show_points=False)
            plotter.show_axes()
            plotter.show_bounds()


if __name__ == '__main__':

    plot_map = plot_geological_map()

    print("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
    print("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
    print('Please ensure you type the following arguments for 2D or 3D display:')
    print("python geological_mapping_2d_3d.py plot2d 'Map/Horizon filepath' 'Wells_head filepath (optional)'")
    print("or")
    print("python geological_mapping_2d_3d.py plot3d 'Map/Horizon filepath' 'Wells_trajectory folderpath (optional)'")
    print("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
    print("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")

    try:
        os.system('color 1F')
    except:
        pass

    if str(sys.argv[1]) == 'plot2d':
        map_path = str(sys.argv[2])

        try:
            map_header_info = input('In Map file, please specify number of lines to skip, X coordinate, Y coordinate, and Z elevation columns, respectively separated with comma (,) and press enter, e.g., 1,1,2,3:\n')
            print("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
            if len(sys.argv) == 4:
                well_path = str(sys.argv[3])
                well_header_info = input('In well_head file, please specify number of lines to skip, well name column, X coordinate, and Y coordinate columns, respectively separated with comma (,) and press enter, e.g., 1,1,2,3:\n')

        except:
            print("Something went wrong, Please check out the steps above")


        try:
            print("Please wait...")
            plt.figure()
            plot_map.plot_2d_map(map_path, map_header_info)
            try:
                plot_map.plot_2d_well(well_path, well_header_info)
            except:
                pass
            plt.show()

        except:
            print("Something went wrong, Please check out the steps above")


    elif str(sys.argv[1]) == 'plot3d':
        map_path = str(sys.argv[2])

        try:
            map_header_info = input('In Map file, please specify number of lines to skip, X coordinate, Y coordinate, and Z elevation columns, respectively separated with comma (,) and press enter, e.g., 1,1,2,3:\n')
            print("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
            if len(sys.argv) == 4:
                well_path = str(sys.argv[3])
                well_header_info = input('In well trajectory file, please specify number of lines to skip, X coordinate, Y coordinate, and MD elevation columns, respectively separated with comma (,) and press enter, e.g., 1,1,2,3:\n')

        except:
            print("Something went wrong, Please check out the steps above")


        try:
            print("Please wait...")
            plotter = pv.Plotter()
            plot_map.plot_3d_map(map_path, map_header_info)
            try:
                plot_map.plot_3d_well(well_path, well_header_info)
            except:
                pass
            # Enable mouse interaction (rotation, zoom, pan)
            plotter.show(interactive=True)

        except:
            print("Something went wrong, Please check out the steps above")
