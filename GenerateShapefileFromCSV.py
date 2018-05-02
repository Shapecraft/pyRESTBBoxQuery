def generateShapefile():
    # Parse a delimited text file of volcano data and create a shapefile
    
    import sys, os
    import osgeo.osr as osr
    import csv

    # use a dictionary reader so we can access by field name
    reader = csv.DictReader(open("sample_data.csv","rb"),
    quoting=csv.QUOTE_NONE)
    
    # set up the shapefile driver
    driver = ogr.GetDriverByName("ESRI Shapefile")
    
    # create the data source
    data_source = driver.CreateDataSource("sample_data.shp")
    
    # create the spatial reference, WGS84
    spatialRef = osr.SpatialReference()
    spatialRef.ImportFromEPSG(2927) 
    
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(2225)
    
    # create the layer
    layer = data_source.CreateLayer("sample_data", srs, ogr.wkbPoint)
    
    # Add the fields we're interested in
    field_name = ogr.FieldDefn("value", ogr.OFTReal)
    field_name.SetWidth(5)
    layer.CreateField(field_name)
    field_nameY = ogr.FieldDefn("y",ogr.OFTReal)
    field_nameY.SetWidth(9)
    layer.CreateField(field_nameY)
    field_nameX = ogr.FieldDefn("x",ogr.OFTReal)
    field_nameX.SetWidth(9)
    layer.CreateField(field_nameX)
    
    # Process the text file and add the attributes and features to the shapefile
    for row in reader:
        # create the feature
        feature = ogr.Feature(layer.GetLayerDefn())
        # Set the attributes using the values from the delimited text file
        feature.SetField("value", row['value'])
        feature.SetField("y", row['y'])
        feature.SetField("x", row['x'])
        
        # create the WKT for the feature using Python string formatting
        wkt = "POINT(%f %f)" %  (float(row['x']) , float(row['y']))
        
        # Create the point from the Well Known Txt
        point = ogr.CreateGeometryFromWkt(wkt)
        
        # Set the feature geometry using the point
        feature.SetGeometry(point)
        # Create the feature in the layer (shapefile)
        layer.CreateFeature(feature)
        # Dereference the feature
        feature = None
    
    # Save and close the data source
    data_source = None
    
generateShapefile()


