# Fetch NASA FIRMS NRT fire detections for the AOI from the past 24 hours
# and save them as data/fires.geojson.
# Same steps as 02_fetch_fires.ipynb, run on a schedule by GitHub Actions.
# Requires the FIRMS_MAP_KEY environment variable.
import os

import geopandas as gpd
import pandas as pd

data_folder = 'data'
map_key = os.environ['FIRMS_MAP_KEY']

# Read the AOI and get its bounding box as west,south,east,north
aoi_gdf = gpd.read_file(os.path.join(data_folder, 'aoi.geojson'))
west, south, east, north = aoi_gdf.total_bounds
bbox = f'{west},{south},{east},{north}'

# Fetch the last 2 days from each NRT source
sources = ['MODIS_NRT', 'VIIRS_SNPP_NRT', 'VIIRS_NOAA20_NRT', 'VIIRS_NOAA21_NRT']
day_range = 2

dfs = []
for source in sources:
    url = (
        'https://firms.modaps.eosdis.nasa.gov/api/area/csv/'
        f'{map_key}/{source}/{bbox}/{day_range}'
    )
    df = pd.read_csv(url)
    print(f'{source}: {len(df)} detections')
    dfs.append(df)

fires_df = pd.concat(dfs, ignore_index=True)

# Combine acq_date and acq_time (HHMM, UTC) into a timestamp
acq_time = fires_df['acq_time'].astype(str).str.zfill(4)
fires_df['acq_datetime'] = pd.to_datetime(
    fires_df['acq_date'] + ' ' + acq_time, format='%Y-%m-%d %H%M', utc=True)

# Keep the past 24 hours
now = pd.Timestamp.now(tz='UTC')
last_24h = fires_df[fires_df['acq_datetime'] >= now - pd.Timedelta(hours=24)]
print(f'Detections in the past 24 hours: {len(last_24h)}')

# Convert to points and clip to the AOI
columns = ['acq_datetime', 'satellite', 'instrument', 'confidence', 'frp', 'daynight']

fires_gdf = gpd.GeoDataFrame(
    last_24h[columns],
    geometry=gpd.points_from_xy(last_24h['longitude'], last_24h['latitude']),
    crs='EPSG:4326')

fires_gdf['confidence'] = fires_gdf['confidence'].astype(str)
fires_gdf['acq_datetime'] = fires_gdf['acq_datetime'].dt.strftime('%Y-%m-%dT%H:%MZ')

fires_gdf = gpd.clip(fires_gdf, aoi_gdf)
print(f'Detections in the AOI: {len(fires_gdf)}')

output_path = os.path.join(data_folder, 'fires.geojson')
fires_gdf.to_file(output_path)
print(f'Saved to {output_path}')
