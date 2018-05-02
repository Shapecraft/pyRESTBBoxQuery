from flask import Flask, g
app = Flask(__name__)

@app.route('/<lang_code>/', methods=['GET'])
def querypoints(lang_code):
    import sys, os
    sys.path.append('/usr/lib/python2.7/dist-packages/osgeo')
    import gdal, ogr
    import re, unicodedata
    import numpy as np
    
    try:
        
        g.lang = lang_code

        'Format: Upper Y, Lower Y, Left X, Right X'
        coordinates = ""
        inList = re.split('\s|,',str(g.lang))
    
        response = " "
        'clean up common user mistakes with commas/spaces'
        inList = list(filter(None, inList))
            
        if len(inList) == 0:
            response = "No filter description provided"
            raise Exception("No filter description provided")
        
        bboxList = [inList[2], inList[0], inList[3], inList[0], inList[3], inList[1], inList[2], inList[1]]
            
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

        try:
            ds_fname = os.path.join(dirname, "sample_data.shp")
        except (TypeError, ValueError):
                response = "Dataset not found"
                raise Exception("Dataset not found")
        
        shapefile = ogr.Open(ds_fname)

        if not shapefile:
            response = "Could not open '%s'"%ds_fname
            raise Exception("Could not open '%s'"%ds_fname)
            
        shapeLayer = shapefile.GetLayer(0)        
        
        'make sure array values are float or integer values'
        for s in bboxList:
            try:
                float(s)
                continue
            except ValueError:
                pass
            try:
                unicodedata.numeric(s)
                continue
            except (TypeError, ValueError):
                response = "Coordinate not numeric or bad syntax"
                raise Exception("Coordinate not numeric or bad syntax")
        
        rows = len(bboxList)/2
        cols = 2
        
        'make sure coordinate pair count is 4 (bounding box)'
        if rows == 4:
            pass
        else:
            response = "Unmatched coordinate pairs"
            raise Exception("Unmatched coordinate pairs")
        
        'Organize coordinate pairs'
        coordinateArray = np.array(bboxList)
        rows = coordinateArray.size//cols
        coordinateArray.shape = (coordinateArray.size//cols, cols)
        coordinateArray = coordinateArray.astype(np.float)
        
        'if last coordinate pair not equal to first, then append'
        'for closing polygon(so user can just use 4 bounding box coordinates)'
        closedCoordArray = []
        for rowIndex in range(0,  rows):
                closedCoordArray.insert(rowIndex, coordinateArray[rowIndex])
        coordArrayMax = len(coordinateArray) - 1
        if not np.array_equal(coordinateArray[0], coordinateArray[coordArrayMax]):
            closedCoordArray.insert(rows+1,coordinateArray[0])

        CoordsForRing = ""
            
        'build polygon'
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for coordinatePair in closedCoordArray:
            coordX = coordinatePair[0] 
            coordY = coordinatePair[1]
            ring.AddPoint(coordX, coordY)
            
        filterPolygon = ogr.Geometry(ogr.wkbPolygon)
        filterPolygon.AddGeometry(ring)
        
        try:
            shapeLayer.SetSpatialFilter(filterPolygon)
        except:
            respone = "Bounding Box Geometry Invalid"
            raise Exception("Bounding Box Geometry Invalid")
        
        geoJSONOutput = ""
        
        try:
            for feature in shapeLayer:
                first = feature.ExportToJson()
                geoJSONOutput = geoJSONOutput + first + " "
        except:
            respone = "Iterating features failed"
            raise Exception("Iterating features failed")
                        
        response = geoJSONOutput.rstrip()
        
        # Save and close the data source
        data_source = None
        
    except:
        e = sys.exc_info()[0]
        response = "Error: " + response + "\n" + str(e)

    return response

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')