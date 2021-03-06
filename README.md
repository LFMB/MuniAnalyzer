# Muni Analyzer

## Author Info
Created by Lucas Blom for a UMaine - Orono's SIE 508 Spring '21 final project.

All rights reserved.

## Development Notes
This is a GIS focused app that needs the following to run:
- Python 3.9
- numpy
- matplotlib
- pandas
- geopandas
- fiona
- shapely

It is recommended to enable `Anaconda` and create a separate `Conda` environment to help with clean `conda-forge` installs.

i.e. run `$ conda activate [your_geo_env]` through your Conda prompt before launching app in PyCharm

The project currently is not linked to a GitHub repo

## Data 
The data can be extracted from the City of Biddeford's GIS Catalog page: https://www.biddefordmaine.org/2522/GIS-Data-Catalog

## Objectives
Create simple UI that allows a user to select from a list of options that redirects the user to a view with two graphs:
- a heat map of the municipality with a legend
- a histogram or scatter plot with a side blurb with population stat descriptions

Current desired statistics for heat mapping:
- land value per sq foot
- land value % of total assessed value
- total value per sq foot
- improvement value per sq foot
- number of bedrooms
- percent built to legally permissible

*Note:* Only `land value % of total assessed value` and `total value per sq foot` are in `buttons_model` 

Potential demographic mapping parameters:
- parcel ownership by state
- property type

### Video Walk Through URL
https://maine.zoom.us/rec/share/fyS5Rv_8BMb7NyCQeeRmZffcSp3p-tM_CNhAtolyZ8Sa_XMfUdHDYTU6SuQstVmH.GrFqH0wQ4qVfHkdW (Access Password: NX58%6gE)


### Issues

- UI view controller only brings user to Home view even though in the code each button is linked to a
specific view.
- Spacing between UI view controllers (the buttons) suggests more tinkering with grids is needed.
- The ModelsManger abstract class is not complete.
- Neither is the logic for showcasing appropriate data models in graphs


## Software Architecture
### Main
`main.py` imports static models from `model.py` and the `Controller` class from `controller.py` to:
- import multiple spatial and attribute focused databases generated by the City of Biddeford.
- create separate views by iterating through parameters of objects that leverage logic maintained by Model and Controller classes.


### View
Uses: `Themed Tkinter(ttk)`, `Tkinter`, `Matplotlib`'s `Figure` and its `backend_tkagg` module.

The `numpy` is strictly for placeholder dataframe data for graphing.

`Window` Class is the base view and the container for all other views for the app.
It has two separate view components. One is for the controllers and the other is for the views.
All its methods minus the `create_ui_controllers` are private and are called during `init`.


`BasicView` Class is text laden views that will eventually be linked to the UI view controllers.

`HeatMapDistributionContainer` Class takes controller segmented data to create static views of data visualisations  

BasicView and HeatMapDistributionContainer are subclasses of the ttk.Frame class provided by Tkinter while the Window class is a subclass to the base Tk class.

### Controller
This class has all its methods minus the constructor public and directs the functionality of the software.
It does not inherit from other classes but does leverage to the ModelsManager abstract class to handle the interaction between models.

The show_view class uses the tk grid packing to 'elevate' different frames within the designated parent container frame.

### Model
The model section is broken into a handful of different static models/ python dictionaries, a `ModelFromFile` class and a `ModelsManager` abstract class.
The segmented static models are used to walk the through steps in launching the app. This was done to allow for the controller to be passed to the view.

`ModelFromFile` is not a subclass but does create an instance of a GeoPandaDataFrame class that is used throughout the app as a parameter.
`ModelsManager` is a subclass with `ABC` being the super. It's an interface class used by the `Controller` class to appropriately segment portions of Geo DFs.








   