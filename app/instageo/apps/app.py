import glob
import json
import os
from pathlib import Path

import streamlit as st
import pycountry

from instageo import INSTAGEO_APPS_PATH
from instageo.apps.viz import create_map_with_geotiff_tiles


def generate_map(directory: str, year: int, month: int, country_tiles: list[str]) -> None:
    try:
        if not directory or not Path(directory).is_dir():
            raise ValueError("Invalid directory path.")
        prediction_tiles = glob.glob(os.path.join(directory, f"{year}/{month}/*.tif"))
        tiles_to_consider = [
            tile
            for tile in prediction_tiles
            if os.path.basename(tile).split("_")[1].strip("T") in country_tiles
        ]
        if not tiles_to_consider:
            raise FileNotFoundError("No GeoTIFF files found for the given year, month, and country.")
        fig = create_map_with_geotiff_tiles(tiles_to_consider)
        st.plotly_chart(
            fig,
            use_container_width=True,
            height=800,
            config={
                'modeBarButtons': [[]],
                'scrollZoom': True,
                'displaylogo': False
            }
        )
    except (ValueError, FileNotFoundError, Exception) as e:
        st.error(f"An error occurred: {str(e)}")


def main() -> None:
    st.set_page_config(layout="wide")
    with open(INSTAGEO_APPS_PATH / "utils/country_code_to_mgrs_tiles.json") as json_file:
        countries_to_tiles_map = json.load(json_file)
    st.plotly_chart(
        create_map_with_geotiff_tiles([]),
        use_container_width=True,
        height=800,
        config={
            'modeBarButtons': [[]],
            'scrollZoom': True,
            'displaylogo': False
        }
    )
    st.markdown(
        """
        <style>
        body {
            margin: 0;
            overflow: hidden;
        }
        .stAppHeader {
            display: none;
            height: 0%;
        }
        .st-emotion-cache-0 {
            width: 100%;
        }
        .st-emotion-cache-1ibsh2c {
            padding: 0;
        }
        .mapboxgl-canvas {
            height: 100vh !important;
        }
        [data-testid="stPlotlyChart"] > div {
            height: 100vh !important;
        }
        .mapboxgl-map {
            position: absolute;
            top: 0 !important;
            height: 100vh !important;
        }
        .modebar-container {
            top: auto !important;
            bottom: 41px !important;
            right: 40px !important;
            padding: 20px;
            z-index: 1001 !important;
        }
        .modebar-container, .modebar-container * {
            pointer-events: auto !important;
        }
        .modebar--hover.ease-bg {
            background-color: transparent !important;
            box-shadow: none !important;
        }
        .modebar--hover.ease-bg * {
            background-color: transparent !important;
            box-shadow: none !important;
        }
        .modebar-btn svg path {
            fill: #0b7d26!important;
        }
        [data-testid="stExpander"] {
            position: fixed !important;
            top: 5px;
            left: 5px;
            z-index: 1000;
            width: auto;
            background: transparent !important;
        }
        [data-testid="stExpander"] details {
            background: #0b7d26!important;
        }
        [data-testid="stExpanderToggleIcon"] {
            display: none !important;
        }
        [data-testid="stExpander"]:hover,
        [data-testid="stExpander"]:hover * {
            color: #ffffff !important;
        }
        [data-testid="stButton"],
        [data-testid="stBaseButton-secondary"] {
            width: 100% !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Settings", expanded=False):
        directory = st.text_input(
            "GeoTiff Directory:",
            help="Path to the directory containing your GeoTIFF files",
        )
        country_options = {}
        for code in countries_to_tiles_map.keys():
            try:
                country = pycountry.countries.get(alpha_2=code)
                country_options[country.name if country else code] = code
            except Exception:
                country_options[code] = code
        selected_country_name = st.selectbox(
            "Select Country",
            options=list(country_options.keys())
        )
        selected_country_code = country_options[selected_country_name]
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month_year_options = [(m, y) for y in range(2015, 2025) for m in range(1, 13)]
        default_option = (1, 2023)
        default_index = month_year_options.index(default_option)
        selected_month_year = st.selectbox(
            "Select Month and Year",
            options=month_year_options,
            format_func=lambda x: f"{month_names[x[0] - 1].lower()} {x[1]}",
            index=default_index
        )
        st.write("Selected:", f"{month_names[selected_month_year[0] - 1].lower()} {selected_month_year[1]}")
        if st.button("Generate Map"):
            country_tiles = countries_to_tiles_map[selected_country_code]
            generate_map(directory, selected_month_year[1], selected_month_year[0], country_tiles)


if __name__ == "__main__":
    main()
