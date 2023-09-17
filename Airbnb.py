import streamlit as st
import pandas as pd
from streamlit_folium import st_folium, folium_static
import folium
from streamlit_extras.grid import grid
from streamlit_option_menu import option_menu



df = pd.read_csv('Airbnb_1.csv')  # Replace 'your_data.csv' with your actual data file path

# Create a Streamlit app
def set_page_config():
# Display the image in your Streamlit app
    
    st.set_page_config(
        page_title="Extracting Business Card Data with OCR",
        layout="wide",
    )

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1579547621113-e4bb2a19bdd6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1878&q=80");
            background-attachment: scroll;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Intractive Property Locations Insights")
    
def navigation_menu():
    selected = option_menu(None, ["Map", "Charts", 'Price Analysis',"About"],  
    menu_icon="cast", default_index=0, orientation="horizontal",styles={
            "container": {"margin": "0", "padding": "0!important", "background-color": "#0c7ded"},
            "icon": {"color": "black", "font-size": "17px"},
            "nav-link": {"font-size": "17px", "text-align": "center", "margin": "2px", "--hover-color": "#1e0ead"},
            "nav-link-selected": {"background-color": "#1e0ead"}
    }
            )
    return selected


def main():
    selected=navigation_menu()
    if selected=="Map":
        
        col1, col2, col3= st.columns(3)
        # Sidebar filters
        with col1:
            selected_country = st.selectbox("Select Country", df["country"].unique())
            selected_city_options = df[df["country"] == selected_country]["city"].unique()
        with col2:
            selected_city = st.selectbox("Select City", selected_city_options) if len(selected_city_options) > 0 else None

        # Filter the DataFrame based on selected filters
        filtered_df = df[
            (df["country"] == selected_country) &
            (df["city"] == selected_city) if selected_city else True   
        ]


        with col3:
            selected_name = st.selectbox("Select Property Name", filtered_df["name"].unique()) if not filtered_df.empty else None
        filtered_df = filtered_df[filtered_df["name"] == selected_name] if selected_name else filtered_df

        if not filtered_df.empty:
            # Get coordinates for the selected property name
            selected_coords = filtered_df["coordinates"].iloc[0].split(", ")
            latitude = float(selected_coords[1])
            longitude = float(selected_coords[0])

            # Center the map on the selected property
            m = folium.Map(location=[latitude, longitude], zoom_start=30)

            # Add a marker for the selected property
            folium.Marker([latitude, longitude], tooltip=selected_name).add_to(m)
        else:
        # Create a default map if no property is selected
            m = folium.Map(location=[0, 0], zoom_start=2)

        st.markdown(f'<h2 style="text-align: center;">{filtered_df["name"].values[0]}</h2>', unsafe_allow_html=True)
        col_1, col_2, col_3=st.columns(3)
        with col_1:
            st.metric(label="Price", value=filtered_df['price'].values[0])
        with col_2:
            st.metric(label="Rating", value=filtered_df['rating'].values[0])
        with col_3:
            st.metric(label="Number of Reviews", value=filtered_df['number_of_reviews'].values[0]) 


        # Display the Folium map using st.write
        folium_static(m)

        col1, col2= st.columns(2)
        with col1:
            st.write(" Property Type : ",filtered_df['property_type'].values[0])
            st.write("Room Type : ",filtered_df['room_type'].values[0])
            st.write("Neighbourhood : ",filtered_df['neighbourhood'].values[0])
        with col2:
            st.write("No of Bedtooms : ",filtered_df['bedrooms'].values[0])
            st.write("No of Accommodates : ",filtered_df['accommodates'].values[0])
        
if __name__ == '__main__':
    set_page_config()
    main()
