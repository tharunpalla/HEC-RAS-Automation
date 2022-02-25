from shapely.geometry import Polygon
import geopandas as gpd

# """Define bounds"""
left_long = -78.2
right_long = -77.7
bottom_lat = 35.4
top_lat = 35.6

# """make lists of points"""
lat_points = [bottom_lat, top_lat, top_lat, bottom_lat, bottom_lat]
long_points = [left_long, left_long, right_long, right_long, left_long]

# """Create Polygon"""
bounds_geom = Polygon(zip(long_points, lat_points))
print(bounds_geom)

# """define polygon with geogrpahic projectation and reproject to match HMS projection"""
crs = "EPSG:4326"
bounds_WGS = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[bounds_geom])
bounds = bounds_WGS.to_crs("EPSG:5070")

# """Export to Shapfile"""
bounds.to_file(filename='shape.shp', driver="ESRI Shapefile")
