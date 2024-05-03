from pathlib import Path

import pandas as pd
import requests
import geopandas
from geopandas import GeoDataFrame
from matplotlib import pyplot as plt

from app.paths import get_data_path, eda_results_folder
from app.plots_faculties import applications_per_faculties

import warnings

warnings.filterwarnings('ignore')


PROGRAM_NAME = {"Bachelor's Programme in Psychology": "BS Psychology",
                "Master's Programme in Pharmacy": "MS Pharmacy",
                "Bachelor's Programme in Logopedics": "BS Logopedics",
                "Bachelor's Programme in Social Research": "BS Social Research",
                "Bachelor's Programme in Law": "BS Law",
                "Bachelor's Programme in Politics, Media and Communication": "BS Politics, Media and Communication",
                "Bachelor's Programme in History": "BS History",
                "Degree Programme in Medicine": "Medicine",
                "Bachelor's Programme in Society and Change": "BS Society and Change",
                "Bachelor's Programme in Philosophy": "BS Philosophy",
                "Bachelor's Programme in Biology": "BS Biology",
                "Master's Programme in Food Economy and Consumption": "BS Food Economy and Consumption",
                "Bachelor's Programme in Art Studies": "BS Art Studies",
                "Bachelor's Programme in Cultural Studies": "BS Cultural Studies",
                "Bachelor's Programme in Molecular Biosciences": "BS Molecular Biosciences",
                "Degree Programme in Dentistry": "Dentistry",
                "Bachelor's Programme in Veterinary Medicine": "BS Veterinary Medicine",
                "Bachelor's Programme in Economics": "BS Economics",
                "Bachelor's Programme in Geography": "BS Geography",
                "Bachelor's Programme in Education": "BS Education",
                "Bachelor's Programme in Enviromental Sciences": "BS Enviromental Sciences",
                "Bachelor's Programme in Pharmacy": "BS Pharmacy",
                "Bachelor's Programme in Languages": "BS Languages",
                "Bachelor's Programme in Food Sciences": "BS Food Sciences",
                "Bachelor's Programme in Chemistry": "BS Chemistry",
                "Bachelor's Programme in Geosciences": "BS Geosciences",
                "Bachelor's Programme in Forest Sciences": "BS Forest Sciences",
                "Bachelor's Programme in Computer Science": "BS Computer Science",
                "Master's Programme in Translation and Interpreting": "MS Translation and Interpreting",
                "Bachelor's Programme in Physical Sciences": "BS Physical Sciences",
                "Bachelor's Programme in the Languages and Literatures of Finland": "BS Languages and Literatures of Finland",
                "Bachelor's Programme in Enviromental and Food Economics": "BS Enviromental and Food Economics",
                "Master's Programme in Finnish and Finno-Ugrian Languages and Cultures": "MS Finnish and Finno-Ugrian Languages and Cultures",
                "Bachelor's Programme in Theology and Religious Studies": "BS Theology and Religious Studies",
                "Bachelor's Programme in Mathematical Sciences": "BS Mathematical Sciences",
                "Bachelorâ€™s program in Social Sciences": "BS Social Sciences",
                "Bachelor's Programme for Teachers of Mathematics, Physics and Chemistry": "BS Teachers of Mathematics, Physics and Chemistry",
                "Bachelor's Programme in Agricultural Sciences": "BS Agricultural Sciences"}


def geocode_address_to_coordinates(address: str):
    if address == 'Abroad':
        return 59.5, 24.75

    """ Geocoding procedure using free ArcGIS service """
    params = {'SingleLine': address, 'outFields': '*', 'f': 'json',
              'langCode': 'ENG', 'preferredLabelValues': 'matchedCity'}
    url = 'https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates'
    try:
        response = requests.get(url, params=params)
        candidates = response.json()['candidates']

        first_assumption = candidates[0]
        lat = first_assumption['location']['y']
        lon = first_assumption['location']['x']
    except Exception:
        lat, lon = 0, 0

    return lat, lon


def prepare_points_layer(spatial_dataframe: pd.DataFrame,
                         epsg_code: str = "4326",
                         lon: str = 'lon',
                         lat: str = 'lat') -> GeoDataFrame:
    """
    Prepare geopandas dataframe with points and spatial geometries from simple
    pandas DataFrame

    :param spatial_dataframe: table to convert
    :param epsg_code: code for CRS
    :param lon: name of column in pandas DataFrame with info about longitude
    :param lat: name of column in pandas DataFrame with info about latitude
    """
    geometry = geopandas.points_from_xy(spatial_dataframe[lon].astype(float), spatial_dataframe[lat].astype(float))
    gdf = GeoDataFrame(spatial_dataframe, crs=f"EPSG:{epsg_code}", geometry=geometry)
    return gdf


def explore_applicants():
    """ Show some patterns related to applicanta """
    df = pd.read_csv(Path(get_data_path(), 'applicant_data.csv'),
                     sep=';', encoding='cp1252')

    plot_path = eda_results_folder('applicants')

    # Generate maps
    df = df[['Applicant.ID', 'Year.of.application', 'Faculty', 'Degree.Programme',
             'Priority', 'Year.of.birth', 'First.time.applicant', 'Municipality',
             'Gender', 'Admission.status', 'previous.qualifications']]
    df = df.dropna()
    df['Degree.Programme'] = df['Degree.Programme'].replace(PROGRAM_NAME)

    # Show some information about age
    for program in list(df['Degree.Programme'].unique()):
        df_program = df[df['Degree.Programme'] == program]

        df_program['Age'] = df_program['Year.of.application'] - df_program['Year.of.birth']
        print(f'{program}: Mean age {df_program["Age"].mean():.2f}')

        # Information about location
        if program == 'BS Psychology':
            # per_location = df_program.groupby('Municipality').agg({'Applicant.ID': 'count'})
            # per_location = per_location.reset_index()
            # # Remove too small locations
            # per_location = per_location[per_location['Applicant.ID'] >= 5]
            #
            # # Add coordinates
            # lats = []
            # longs = []
            # for i, row in per_location.iterrows():
            #     print(f'Receiving coordinates for {row["Municipality"]}')
            #     lat, lon = geocode_address_to_coordinates(row['Municipality'])
            #     lats.append(lat)
            #     longs.append(lon)
            #
            # per_location['lat'] = lats
            # per_location['lon'] = longs
            per_location = pd.read_csv('program_with_locations.csv')
            per_location = per_location[per_location['lat'] > 0]
            per_location = prepare_points_layer(per_location)
            # per_location = per_location.to_crs(epsg=3857)
            per_location['ratio'] = per_location['Applicant.ID'] / per_location['Applicant.ID'].sum()

            import contextily as cx

            fig_size = (12.0, 9.0)
            fig, ax = plt.subplots(figsize=fig_size)
            ax = per_location.plot(zorder=1, alpha=0.9, column='ratio',
                                   legend=True, cmap='Reds', markersize='ratio',
                                   legend_kwds={'label': 'Number of applicants'})
            cx.add_basemap(ax, crs=per_location.crs.to_string(),
                           source=cx.providers.CartoDB.Voyager)
            plt.title('Municipalities of applicants')

            plt.savefig(Path(plot_path, f'applicants_map.png'))
            plt.close()

            print(f'Map was generated')
            exit()


if __name__ == '__main__':
    explore_applicants()
