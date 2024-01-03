# importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px


# Page configuration
st.set_page_config(
    page_title = "Kaduna State Tuberculosis",
    page_icon = "❤️",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

alt.themes.enable("dark")

st.title('Tuberculosis Analysis in Kaduna')

# Load the data
block1a_2021_df = pd.read_csv("C:/Uday/Uday Research/Uday Projects/Real-World Projects Omdena/Local Chapter - Tuberculosis/2021_block1a_dataset.csv")
block1a_2022_df = pd.read_csv("C:/Uday/Uday Research/Uday Projects/Real-World Projects Omdena/Local Chapter - Tuberculosis/2022_block1a_dataset.csv")
block1a_2023_df = pd.read_csv("C:/Uday/Uday Research/Uday Projects/Real-World Projects Omdena/Local Chapter - Tuberculosis/2023_block1a_dataset.csv")

gps_facility_df = pd.read_csv("C:/Uday/Uday Research/Uday Projects/Real-World Projects Omdena/Local Chapter - Tuberculosis/gps_facility_final.csv")


# Sidebar for Slected Year
with st.sidebar:
    st.sidebar.image("Kaduna chapter logo.jpg")
    st.title("❤️ Kaduna State Tuberculosis Dashboard")


# Combine unique Years and create labeled options for multiselect
all_years_with_labels = [year for year in pd.concat([df['Year'] for df in [block1a_2021_df, block1a_2022_df, block1a_2023_df]]).unique()]

# Combine unique Quarters and create labeled options for multiselect
all_quarters_with_labels = [("Quarter " + str(quarter), quarter) for quarter in pd.concat([df['Quarter'] for df in [block1a_2021_df, block1a_2022_df, block1a_2023_df]]).unique()]

with st.sidebar:
    # Create multiselect widgets for Years and Quarters
    selected_years = st.multiselect("Selected Years", options=all_years_with_labels, default=all_years_with_labels[:1])

    selected_quarters = st.multiselect("Selected Quarters", options=[option[0][8:] for option in all_quarters_with_labels], default=[option[0][8:] for option in all_quarters_with_labels][:1])

    # Extract only the Year and Quarter values from the selected options
    selected_years_values = [int(option) for option in selected_years]
    selected_quarters_values = [int(option) for option in selected_quarters]

# Filter and display the combined DataFrame based on selected Years and Quarters
combined_df = pd.concat([df[df['Year'].isin(selected_years_values) & df['Quarter'].isin(selected_quarters_values)] for df in [block1a_2021_df, block1a_2022_df, block1a_2023_df]]).reset_index(drop=True)

if selected_years and selected_quarters:

    # Sort selected Quarters in ascending order
    selected_quarters_values.sort()

    # Fill null values with 0
    combined_df.fillna(0, inplace=True)

    # Remove the index
    combined_df = combined_df.reset_index(drop=True)

     # Sort the DataFrame by the selected Quarters in ascending order
    combined_df['Quarter'] = pd.Categorical(combined_df['Quarter'], categories=selected_quarters_values, ordered=True)
    combined_df = combined_df.sort_values(by=['Quarter']).reset_index(drop=True)



    # Hide the first column (likely the Year column)
    st.dataframe(combined_df.iloc[:, 1:])
else:
    st.write("No data matches the selected criteria.")


# Plots

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

# Choropleth map
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="Kaduna",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(combined_df.Year)),
                               scope="kaduna",
                               labels={'Year':'Year'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth


# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='medium')


with col[1]:

    # Sample Data for the choropleth map
    data_map = {
        'State': ['Kaduna', 'Lagos', 'Abuja'], 
        'Year': [2021, 2022, 2023], 
        }
    
    combined_df_map = pd.DataFrame(data_map)

    # GeoJSON data for Nigerian states
    geojson_url = "https://raw.githubusercontent.com/UdashFramework/plotly-dash/master/dash_geojson/test/assets/nigeria.geojson"
    


    
    # Create choropleth map
    fig_map = px.choropleth(
        combined_df_map,
        geojson=geojson_url,
        featureidkey="properties.NAME_1",
        locations="State",
        color="Year",
        color_continuous_scale="Viridis",
        title="Tuberculosis Analysis in Kaduna",
    )
    
    # Customize map layout
    fig_map.update_geos(fitbounds="locations", visible=False)

    # Display choropleth map
    st.plotly_chart(fig_map, use_container_width=True)



with col[2]:
    st.markdown("#### Top LGA's")

    # Sort the DataFrame by "Total number of presumptives" in ascending order
    combined_df_sorted = combined_df.sort_values(by="Total number of presumptives", ascending=False)

    # Ensure unique LGA values
    combined_df_sorted = combined_df_sorted.drop_duplicates(subset=["LGA"])


    # Check for empty DataFrame and handle accordingly
    if not combined_df_sorted.empty:
        max_value = max(combined_df_sorted.Year)
    else:
        max_value = 100 


    # Select and display the desired columns with progress bar configuration
    st.dataframe(combined_df_sorted[['LGA', 'Total number of presumptives']],
                 column_order=("LGA", "Total number of presumptives"),
                 hide_index=True,
                 width=None,
                 column_config={
                     "LGA": st.column_config.TextColumn("LGA"),
                     "Total number of presumptives": st.column_config.ProgressColumn(
                         "Total number of presumptives",
                         format="%f",
                         min_value=0,
                         max_value=max_value,  
                     )
                 }
                 )





