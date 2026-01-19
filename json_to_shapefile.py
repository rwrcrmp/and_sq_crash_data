# Import os for file system operations (creating directories)
import os

# Import pandas for data manipulation (similar to tidyverse in R)
import pandas as pd

# Import geopandas for spatial data handling (similar to sf in R)
import geopandas as gpd

# Import Point class from shapely to create point geometries
# shapely is the underlying geometry library (like sf uses s2/GEOS)
from shapely.geometry import Point

# Import matplotlib for plotting (similar to base R plotting)
import matplotlib.pyplot as plt

# Import contextily for adding basemaps to plots
# Requires separate install: pip install contextily
import contextily as ctx

# Read the JSON file into a pandas DataFrame
# pd.read_json() is similar to jsonlite::fromJSON() in R
df = pd.read_json("crash_data.json")

# Print column names to verify coordinate fields exist
# This helps us confirm the lat/lon column names
print("Columns:", df.columns.tolist())
print(f"Total records: {len(df)}")

# Create Point geometries from longitude (x) and latitude (y) columns
# Note: Point takes (x, y) order, which is (longitude, latitude)
# The apply() function works like purrr::map() or lapply() in R
# lambda is an anonymous function (like \(x) in R)
geometry = df.apply(lambda row: Point(row["longitude"], row["latitude"]), axis=1)

# Create a GeoDataFrame by combining the data with the geometry
# crs="EPSG:4326" sets the coordinate reference system to WGS84 (standard GPS coordinates)
# This is similar to st_as_sf() with coords argument in R
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Define a reference point for geoprocessing
# Coordinates: (30.349979, -97.717035) - note Point takes (lon, lat) order
reference_point = Point(-97.717035, 30.349979)

# Reproject to Texas State Plane Central (EPSG:2277) which uses feet
# Distance calculations require a projected CRS, not geographic (lat/lon)
# Similar to st_transform() in R
gdf_projected = gdf.to_crs("EPSG:2277")

# Create a GeoSeries for the reference point and reproject it to match
# GeoSeries is needed to use geopandas spatial methods
ref_point_gdf = gpd.GeoSeries([reference_point], crs="EPSG:4326").to_crs("EPSG:2277")

# Buffer the reference point by 300 feet
# In EPSG:2277, the unit is US survey feet
# Similar to st_buffer() in R
buffer_300ft = ref_point_gdf.buffer(500).iloc[0]

# Filter crashes within the 300ft buffer
# .within() returns True/False for each geometry
# Similar to st_within() or st_intersection() in R
gdf_filtered = gdf_projected[gdf_projected.within(buffer_300ft)]

print(f"Crashes within 300ft of reference point: {len(gdf_filtered)}")

# Reproject back to WGS84 for output (more portable)
gdf_filtered = gdf_filtered.to_crs("EPSG:4326")

# Define output directory for shapefile
# Shapefiles consist of multiple files (.shp, .shx, .dbf, .prj, etc.)
output_dir = "crash_records_extract"

# Create the output directory if it doesn't exist
# exist_ok=True prevents an error if the directory already exists
# Similar to dir.create(showWarnings = FALSE) in R
os.makedirs(output_dir, exist_ok=True)

# Export to Shapefile
# .to_file() is similar to st_write() in R
# Note: Shapefiles truncate column names to 10 characters
output_path = os.path.join(output_dir, "crash_data.shp")
gdf_filtered.to_file(output_path)

print(f"Saved {len(gdf_filtered)} records to {output_path}")

# =============================================================================
# VISUALIZATION OPTIONS
# Uncomment the method you want to use
# =============================================================================

# OPTION 1: Simple matplotlib plot
# Basic plot without basemap - quick visual check
gdf_filtered.plot(color="red", markersize=50)
plt.title("Crashes within 300ft of reference point")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

# OPTION 2: Matplotlib with basemap (contextily)
# Adds street map background for context
# Requires: pip install contextily
# ax = gdf_filtered.to_crs(epsg=3857).plot(figsize=(10, 10), color="red", markersize=50)
# ctx.add_basemap(ax)
# plt.title("Crashes within 300ft of reference point")
# plt.show()

# OPTION 3: Interactive web map (folium via geopandas)
# Creates an HTML file you can open in browser - pan/zoom enabled
# Similar to leaflet/mapview in R
# m = gdf_filtered.explore(color="red")
# m.save(os.path.join(output_dir, "crash_map.html"))
# print(f"Interactive map saved to {output_dir}/crash_map.html")
