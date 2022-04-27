import csv
import io

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from getPlaceIDs import getPLaceID

def fillPlaceIDs(names, lat, lon, radius):
    new_df = pd.DataFrame(columns=['Name', 'Place ID'])

    for name in names:
        place_id = getPLaceID(name, lat, lon, radius)
        if not place_id:
            continue

        new_df = new_df.append({'Name': name, 'Place ID': place_id}, ignore_index=True)

    return new_df


def main():
    st.set_page_config(layout="wide")

    places_df = None

    st.title('Map')

    input_col, map_col = st.columns([1,3])

    with input_col:
        st.header('Choose Places to Search From')

        latitude = st.number_input('Latitude', min_value=-90.0, max_value=90.0,
                                   value=0.0, format='%.7f')
        longitude = st.number_input('Longitude', min_value=-180.0, max_value=180.0,
                                    value=0.0, format='%.7f')
        radius = st.number_input('Radius (miles)', min_value=0.0, max_value=1000.0,
                                 value=25.0)
        csv_file = st.file_uploader('Choose a CSV file', type=['csv', 'txt'],
                                    accept_multiple_files=False)

        if csv_file is not None:
            places_df = pd.read_csv(csv_file, header=0)
            places_df = places_df.iloc[:, 0]
            places_df.name = 'Name'
            places_list = places_df.tolist()

            if st.button('Find Place IDs', key='get_places'):
                places_df = fillPlaceIDs(places_df.tolist(), latitude, longitude, radius)

        else:
            st.button('Find Place IDs', key='get_places', disabled=True)

    with map_col:
        st.header('Insert Map Here')

        if places_df is not None:
            st.table(places_df)





    # if csv_file is not None:
    #     places_df = pd.read_csv(csv_file, header=0)
    #     places_df = places_df.iloc[:, 0]
    #     places_df.name = 'Name'
    #
    #
    #     if st.button('Find Place IDs', key='get_places'):
    #         places_df = fillPlaceIDs(places_df.tolist(), latitude, longitude, radius)
    #         st.table(places_df)
    #
    #     else:
    #         st.text(type(places_df.tolist()))
    #         st.text(places_df.tolist())
    #         # st.table(places_df)
    #
    #
    # else:
    #     st.button('Find Place IDs', key='get_places', disabled=True)





if __name__ == '__main__':
    main()
