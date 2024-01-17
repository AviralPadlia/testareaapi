from rest_framework import serializers

class ExtentSerializer(serializers.Serializer):
    xmin = serializers.FloatField()
    ymin = serializers.FloatField()
    xmax = serializers.FloatField()
    ymax = serializers.FloatField()
    SpatialReference = serializers.IntegerField()  # Assuming the spatial reference ID

class PolygonSerializer(serializers.Serializer):
    rings = serializers.ListField()     #child=serializers.ListField(child=serializers.FloatField())
    SpatialReference = serializers.IntegerField()  # Assuming the spatial reference ID

class GeometrySerializer(serializers.Serializer):
    geometry = serializers.ListField(child=serializers.DictField())
    areaUnit = serializers.CharField()
