import streamlit as st
import pandas as pd
from streamlit_folium import st_folium, folium_static
import folium
from streamlit_extras.grid import grid
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.figure_factory as ff


df = pd.read_csv('Airbnb_1.csv')  # Replace 'your_data.csv' with your actual data file path

df['country'] = df['country'].replace('中国', 'China')
chinese_to_english = {
    '香港 Hong Kong': 'Hong Kong',
    '香港島 Hong Kong Island': 'Hong Kong Island',
    '新界 New Territories': 'New Territories'
}

df['city'] = df['city'].replace(chinese_to_english)
df['rating'] = df['rating'].astype(int)
df['bedrooms'] = df['bedrooms'].astype(int)
df['price'] = df['price'].astype(int)


# Create a Streamlit app
def set_page_config():
# Display the image in your Streamlit app
    
    st.set_page_config(
        page_title="Airbnb Data Analysis",
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
    title_style = """
    color: black;
    text-align: center;
    padding: 10px;
    background-color: white;
    border-radius: 15px; /* Adjust the value to control the curvature */
    """

    # Apply the custom style to the title
    st.markdown(f'<h1 style="{title_style}">Interactive Airbnb Listings Insights</h1>', unsafe_allow_html=True)
    st.markdown("")
    
def navigation_menu():
    selected = option_menu(None, ["Map", "Price Analysis", "Charts","Trends"],  
    menu_icon="", default_index=0, orientation="horizontal",styles={
            "container": {"margin": "1", "padding": "0", "background-color": "black",},           
            "nav-link": {"font-size": "14px", "text-align": "center", "margin": "7px", "--hover-color": "#808080","border-radius": "10px"},
            "nav-link-selected": {"background-color": "#CCCCCC","border-radius": "10px"}
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
            (df["city"] == selected_city) if selected_city else True]


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

        col1, col2, col3= st.columns(3)
        with col1:
            st.write(" Property Type : ",filtered_df['property_type'].values[0])
            st.write("Room Type : ",filtered_df['room_type'].values[0])
            st.write("Host Name : ",filtered_df['host_name'].values[0])
            st.write("Neighbourhood : ",filtered_df['neighbourhood'].values[0])
            st.write("Amenities : ",filtered_df['amenities'].values[0])
            
        with col3:
            st.write("No of Bedtooms : ",filtered_df['bedrooms'].values[0])
            st.write("No of Accommodates : ",filtered_df['accommodates'].values[0])
            st.write("Host id : ",filtered_df['host_id'].values[0])
            st.write("Access : ",filtered_df['access'].values[0])
        
        fig = px.scatter(
                    df.sort_values(by='start_date'),
                    x="price",
                    y="number_of_reviews",
                    size="price",
                    color='country',
                    log_x=True,
                    size_max=60,
                )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    if selected=="Price Analysis":
        selected_country = st.selectbox("Select Country", df["country"].unique())
        
        my_grid = grid([3, 5], vertical_align="bottom")
        
        with my_grid.expander("Show Filters", expanded=True):
            min_price, max_price = st.slider("Select Price Range", min(df['price']), max(df['price']), (min(df['price']), max(df['price'])))
            min_rating = st.number_input("Select Rating Range", min_value=5, max_value=100, value=5, step=5,)
            max_rating = st.number_input("Select Rating Range", min_value=5, max_value=100, value=100, step=5,)
           
            min_bedrooms, max_bedrooms = st.slider("Select Bedrooms Range", min(df['bedrooms']), max(df['bedrooms']), (min(df['bedrooms']), max(df['bedrooms'])))

            # Filter the DataFrame based on the selected country, price range, rating range, and bedrooms range
            filtered_df = df[
                (df["country"] == selected_country) & 
                (df['price'] >= min_price) & (df['price'] <= max_price) &
                (df['rating'] >= min_rating) & (df['rating'] <= max_rating) &
                (df['bedrooms'] >= min_bedrooms) & (df['bedrooms'] <= max_bedrooms)
                ]
            st.write("No of Properties available",filtered_df['name'].count())

        fig = px.bar(
        filtered_df.groupby(['city'])['name'].count().reset_index(),
        x='city',
        y='name',
        title='Property Count by City',
        labels={'name': 'Property Count'},
            )
        fig.update_xaxes(title='City')
        fig.update_yaxes(title='Property Count')
        fig.update_traces(text=filtered_df.groupby(['city'])['name'].count().reset_index()['name'], textposition='outside')
        

        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')


        # Display the bar chart using Streamlit
        my_grid.plotly_chart(fig, use_container_width=True)
       
        
        selected_city_options = df[df["country"] == selected_country]["city"].unique()
        selected_city = st.selectbox("Select City", selected_city_options) if len(selected_city_options) > 0 else None
        #selected_name = st.selectbox("Select Property Name", filtered_df["name"].unique()) if not filtered_df.empty else None
        filtered_df =filtered_df[filtered_df["city"] == selected_city]

        acend_col, decend_col=st.columns(2)
        with acend_col:

            top_ascending_df = filtered_df.sort_values(by='price').tail(10)
            fig_ascending = px.bar(
                    top_ascending_df,
                x='price',
                y='name',
                title='Top 10 Airbnb listings by Prices(High to Low) ',
                labels={'price': 'Price'},
                orientation='h',
                color='price',  # Set color based on 'price' column
                color_continuous_scale='Viridis',
            )
            fig_ascending.update_xaxes(title='')
            fig_ascending.update_yaxes(title='')
            fig_ascending.update_traces(text=top_ascending_df['price'], textfont=dict(size=20), textposition='outside')
            fig_ascending.update_layout(bargap=0.5)
            

            fig_ascending.update_xaxes(tickvals=[], showticklabels=False)

            st.plotly_chart(fig_ascending, use_container_width=True, height=500)
            st.write("Top 10 Properties by Price (Ascending):")

            top_descending_df = top_ascending_df.sort_values(by='price', ascending=False)

            # Display the table in descending order by 'price'
            st.table(top_descending_df[['name', 'rating', 'bedrooms', 'price']])
            

        # Create bar chart for descending order
        with decend_col:
            top_descending_df = filtered_df.sort_values(by='price', ascending=False).tail(10)
            fig_descending = px.bar(
                top_descending_df,
                x='price',  
                y='name',
                title='Top 10 Airbnb listings by Prices(Low to High)',
                labels={'price': 'Price'},
                orientation='h',
                color='price',  # Set color based on 'price' column
                color_continuous_scale='Viridis',
            )
            fig_descending.update_xaxes(title='')
            fig_descending.update_yaxes(title='')
            fig_descending.update_traces(text=top_descending_df['price'], textfont=dict(size=20), textposition='outside')
            fig_descending.update_layout(bargap=0.5)
            fig_descending.update_xaxes(tickvals=[], showticklabels=False)
            


            # Display the charts using Streamlit
            
            st.plotly_chart(fig_descending, use_container_width=True, height=500)

            # Display tables for both ascending and descending dataframes
            
            st.write("Top 10 Properties by Price (Descending):")
            top_descending_df = top_descending_df.sort_values(by='price', ascending=True)

            st.table(top_descending_df[['name', 'rating', 'bedrooms', 'price']])


    if selected=="Charts":
        my_grid = grid([4, 4], vertical_align="bottom")
        
        Criteria=my_grid.selectbox("Select the Criteria show Insights",['country','bedrooms','property_type','room_type'])
        
        tab1, tab2, tab3= st.tabs(["All Properties", "By Selected country","HeatMap"])
        with tab1:        
            title = f'Property Count | {Criteria}'            
            fig = px.bar(
            df.groupby([Criteria])['name'].count().reset_index(),
            x=Criteria,
            y='name',
            title=title,
            labels={'name': 'Property Count'},
                )
            fig.update_xaxes(title=Criteria)
            fig.update_yaxes(title='Property Count')
            fig.update_traces(text=df.groupby([Criteria])['name'].count().reset_index()['name'], textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        with tab2:    
            selected_country = st.selectbox("Select Country", df["country"].unique())
            filtered_df = df[df["country"] == selected_country]
            
            title = f'Property Count | Country/{Criteria}'
            fig = px.bar(
            filtered_df.groupby([Criteria])['name'].count().reset_index(),
            x=Criteria,
            y='name',
            title=title,
            labels={'name': 'Property Count'},
                )
            fig.update_xaxes(title=Criteria)
            fig.update_yaxes(title='Property Count')
            fig.update_traces(text=filtered_df.groupby([Criteria])['name'].count().reset_index()['name'], textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        with tab3:
            columns_to_remove = ['_id', 'host_id', 'latitude', 'longitude']
            filtered_df = filtered_df.drop(columns=columns_to_remove)
            numeric_columns = filtered_df.select_dtypes(include=['number'])
            correlation_matrix = numeric_columns.corr()

            fig = px.imshow(
                correlation_matrix,
                x=correlation_matrix.columns,
                y=correlation_matrix.columns,
                title=title,
                labels={'x': 'Property Name', 'y': 'Property Name'},
                color_continuous_scale='Inferno',
            )

            fig.update_xaxes(title='')
            fig.update_yaxes(title='')
            st.plotly_chart(fig, use_container_width=True)

                

    if selected=="Trends":
        my_grid = grid([4, 4], vertical_align="bottom")
        metric=my_grid.selectbox("select Metic",['price','rating','number_of_reviews']) 
        selected_country = my_grid.selectbox("Select Country", df["country"].unique())
        filtered_df = df[df["country"] == selected_country]
        filtered_df = filtered_df.sort_values(by='end_date')
        
        fig = px.line(
            filtered_df,
            x='end_date',  # Assuming 'date' is the column containing date values
            y=metric,  # Assuming 'price' is the column containing price values
            title=f'{metric} Over Time in {selected_country}',
            labels={'date': 'Date', 'price': 'Price'},            
            )

        # Specify the axis labels
        fig.update_xaxes(title='')
        fig.update_yaxes(title=metric)

        # Display the line chart
        st.plotly_chart(fig, use_container_width=True)
        
if __name__ == '__main__':
    set_page_config()
    main()