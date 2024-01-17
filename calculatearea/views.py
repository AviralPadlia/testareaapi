from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ExtentSerializer, PolygonSerializer, GeometrySerializer
from arcgis.geometry import Geometry, LengthUnits, AreaUnits
from arcgis import geometry
from arcgis.gis import GIS

class CalculateAreaView(APIView):
    def computeArea(polygon,spatialReference,areaUnit):
        units={"Hectares":AreaUnits.HECTARES,
                "Ares":AreaUnits.ARES,
                "Square Meters":AreaUnits.SQUAREMETERS,
                "Square Decimeters":AreaUnits.SQUAREDECIMETERS,
                "Square Centimeters":AreaUnits.SQUARECENTIMETERS,
                "Square Millimeters":AreaUnits.SQUAREMILLIMETERS,
                "Square Miles":AreaUnits.SQUAREMILES,
                "Acres":AreaUnits.ACRES,
                "Square Yards":AreaUnits.SQUAREYARDS,
                "Square Feet":AreaUnits.SQUAREFEET,
                "Square Inches":AreaUnits.SQUAREINCHES,
                "Square Kilometers":AreaUnits.SQUAREKILOMETERS,
                }
        
        cal_type="geodesic" if spatialReference==4326 or spatialReference==3857 else "planar"
        length_unit = LengthUnits.METER
        gis=GIS()
        areas_lengths = geometry.areas_and_lengths(
            polygons=[polygon],
            area_unit=units[areaUnit],  
            length_unit=length_unit,            
            calculation_type=cal_type,
            gis=gis
        )
        return areas_lengths["areas"][0]

    def post(self, request, *args, **kwargs):
        serializer = GeometrySerializer(data=request.data)
        if serializer.is_valid():
            geometry_data = serializer.validated_data['geometry']
            areaUnit = serializer.validated_data['areaUnit']
            # return Response({'inif': [geometry_data,area_unit]})
            areas=[]
            for item in geometry_data:
                if 'xmin' in item and 'xmax' in item and 'ymin' in item and 'ymax' in item:
                    #return Response({'inif': [geometry_data,area_unit]})
                    # If extent coordinates are provided
                    extent_serializer = ExtentSerializer(data=item)
                    if extent_serializer.is_valid():
                        xmin = extent_serializer.validated_data['xmin']
                        xmax = extent_serializer.validated_data['xmax']
                        ymin = extent_serializer.validated_data['ymin']
                        ymax = extent_serializer.validated_data['ymax']
                        spatialReference = extent_serializer.validated_data['SpatialReference']
                        #return Response({'polygon': [xmin,ymin,xmax,ymax,spatialReference]})

                        
                        polygon = geometry.Geometry({
                                    "rings" : [[[xmin, ymin],[xmin, ymax],[xmax, ymax],[xmax, ymin],[xmin, ymin]]],
                                    "spatialReference" : {"wkid" : spatialReference}
                                    })
                        areas.append(CalculateAreaView.computeArea(polygon,spatialReference,areaUnit))
                        
                elif 'rings' in item:
                    # If polygon coordinates are provided
                    #return Response({'areas': "rings"})
                    polygon_serializer = PolygonSerializer(data=item)
                    if polygon_serializer.is_valid():
                        #return Response({'areas': "poly"})
                        coordinates = polygon_serializer.validated_data['rings']
                        srs = polygon_serializer.validated_data["SpatialReference"]

                        polygon = Geometry({
                            "rings": coordinates,
                            "spatialReference": {"wkid": srs}
                        })
                        areas.append(CalculateAreaView.computeArea(polygon,spatialReference,areaUnit))
                        
            return Response({'areas': areas})
        return Response(serializer.errors, status=400)

  
