Query Points Overview:

This is a REST API application for querying points within a bounding box in a Docker container. The application is built on Ubuntu 14.04, Python 2.7, Flask 0.10.1, and gdal/ogr 1.10.

Building and compiling the application:

1) In Docker CLI, or equivalent, go to the directory of the downloaded files:

2) Enter: docker build -t query_points_polygon .

3) Enter: docker run -it -p 5000:5000 query_points_polygon


Running the application:

1) Open your browser or postman, etc..

2) Enter the ip address and port of the created container

3) Enter your bounding box coordinates in the following order, separated by a space or comma:

Example: http://192.168.99.100:5000/<Upper Y> <Lower Y> <Left X> <Right X>


Sample, tested bounding boxes (with provided 600,000 sample_data.csv points):

'Upper Y, Lower Y, Left X, Right X'

SMALL: 97.78 95.38 72.96 76.95

MEDIUM: 50.33 39.05 198.60 213.72

LARGE: 105 79 144 170


SHAPEFILE (sample_data.shp):

The sample_data.shp shapefile was generated using the python module: GenerateShapefileFromCSV.py

If you decide to generate the shapefile yourself, consider adding an FID, unique feature identifier column. It may enhance performace. QGIS -> Field Calculator: $rownum

EXTENT: 183, 0, 0, 108 - ('Upper Y, Lower Y, Left X, Right X')

Spatial Reference: Stateplane - California: Zone 1 (NAD83)





