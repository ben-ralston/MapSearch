import csv
import io

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import folium
from streamlit_folium import st_folium

from getPlaceIDs import getPLaceID


def fillPlaceIDs(names, lat, lon, radius, progress_bar):
    new_df = pd.DataFrame(columns=['Name', 'Place ID', 'Latitude', 'Longitude'])

    progress_inc = 1 / len(names)
    progress_amount = 0.0

    for name in names:
        place_dict = getPLaceID(name, lat, lon, radius)
        if not place_dict:
            continue

        new_df = new_df.append(place_dict, ignore_index=True)

        progress_amount += progress_inc
        if progress_amount > 1:
            progress_amount = 1
        progress_bar.progress(progress_amount)

    return new_df


def sidebar():
    with st.sidebar:
        if st.button('Choose Places'):
            st.session_state.setup = True
        if st.button('Search Your Places'):
            st.session_state.setup = False

        if st.session_state.setup:
            st.title('Choose Places')

            if st.button('Use Recommended Places'):
                st.session_state.places = pd.read_pickle('JunkosPlaces.pkl')

            st.session_state.latitude = st.number_input('Latitude', min_value=-90.0, max_value=90.0,
                                       value=37.541290, format='%.7f')
            st.session_state.longitude = st.number_input('Longitude', min_value=-180.0, max_value=180.0,
                                        value=-77.434769, format='%.7f')
            radius = st.number_input('Radius (miles)', min_value=0.0, max_value=1000.0,
                                     value=75.0)
            csv_file = st.file_uploader('Choose a CSV file', type=['csv', 'txt'],
                                        accept_multiple_files=False)

            if csv_file is not None:
                places_df = pd.read_csv(csv_file, header=0)
                places_df = places_df.iloc[:, 0]
                places_df.name = 'Name'
                st.session_state.place_names = places_df

                if st.button('Find Place IDs', key='get_places'):
                    progress_bar = st.progress(0.0)

                    st.session_state.places = fillPlaceIDs(
                        st.session_state.place_names.tolist(),
                        st.session_state.latitude,
                        st.session_state.longitude,
                        radius,
                        progress_bar
                    )

            else:
                st.button('Find Place IDs', key='get_places', disabled=True)

        else:
            st.title('Search Places')

            name = st.text_input('Name')
            only_open = st.checkbox('Open Now')
            price = st.multiselect('Price', options=['$', '$$', '$$$', '$$$$'])


def body():
    st.title('Junko\'s Map App')

    # st.header('Insert Map Here')

    if st.session_state.places is not None:
        m = folium.Map(location=[st.session_state.latitude, st.session_state.longitude],
                       zoom_start=12)

        for index, row in st.session_state.places.iterrows():
            name = row['Name']
            folium.Marker(
                [row['Latitude'], row['Longitude']], popup=name, tooltip=name
            ).add_to(m)

        st_folium(m)

        st.table(st.session_state.places)

    elif st.session_state.place_names is not None:
        st.table(st.session_state.place_names)


def main():
    if 'setup' not in st.session_state:
        st.session_state.setup = True
    if 'places' not in st.session_state:
        st.session_state.places = None
    if 'place_names' not in st.session_state:
        st.session_state.place_names = None
    if 'latitude' not in st.session_state:
        st.session_state.latitude = 0
    if 'longitude' not in st.session_state:
        st.session_state.longitude = 0

    st.set_page_config(layout='wide')

    sidebar()

    body()


if __name__ == '__main__':
    main()
