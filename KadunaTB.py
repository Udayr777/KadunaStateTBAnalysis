# importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt
from block1 import vis1A
from visualsblock1 import plot_lga_presumptive_cases_trend, plot_lga_diagnosed_tb_cases_trend, show_choropleth_for_number_of_diagnosed, show_gender_age_tb_bar, kaduna_lgas, create_tb_cases_plot, create_tb_scatter_plot

from block2b import vis2B

# Page configuration
st.set_page_config(
    page_title = "Kaduna State Tuberculosis",
    page_icon = "❤️",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

alt.themes.enable("dark")

st.title('Tuberculosis Analysis in Kaduna')

dataType = ["Breakdown of activities of all presumptive PTB cases on the clinic during the register", "Quarterly breakdown of all TB cases registered during the quarter by category and type of diagnosis", "Number of cases broken down by gender and age"]

gps_facility_df = pd.read_csv("Dataset/gps_facility_final.csv")

# Sidebar for Slected Year
with st.sidebar:
    st.sidebar.image("Kaduna chapter logo.jpg")
    st.title("❤️ Kaduna State Tuberculosis Dashboard")

    #which block the user want to see
    block = st.selectbox("Dataset", options = dataType )

    #block 1a
    if block == "Breakdown of activities of all presumptive PTB cases on the clinic during the register":
        blockCombined = pd.read_csv("Dataset/block1a/block1a_2019_to_2023_processed.csv")

    #block 2b
    elif block == "Number of cases broken down by gender and age":
        blockCombined = pd.read_csv("Dataset/block2b/block2b_19_to_23.csv")

    else:

        blockCombined = pd.read_csv("Dataset/block2a/block2a_full_data_q.csv")




# Combine unique Years and create labeled options for multiselect
all_years_with_labels = [year for year in blockCombined['Year'].unique()]

# Combine unique Quarters and create labeled options for multiselect
all_quarters_with_labels = [("Quarter " + str(quarter), quarter) for quarter in blockCombined['Quarter'].unique()]

with st.sidebar:
    # Create multiselect widgets for Years and Quarters
    selected_years = st.multiselect("Selected Years", options=all_years_with_labels, default=all_years_with_labels[:1])

    selected_quarters = st.multiselect("Selected Quarters", options=[option[0][8:] for option in all_quarters_with_labels], default=[option[0][8:] for option in all_quarters_with_labels][:1])

    # Extract only the Year and Quarter values from the selected options
    selected_years_values = [int(option) for option in selected_years]
    selected_quarters_values = [int(option) for option in selected_quarters]

    lga_choice = st.selectbox(
    'Select a Kaduna LGA',
    kaduna_lgas)


    if st.button("Contact Us"):
        st.write("""
                 **Contact:**
                * Jamaludeen Madaki
                * Omdena Kaduna Chapter Lead
                * omdenakdnachapter@gmail.com
                * +234 7010412114
                """)



    

# Filter and display the combined DataFrame based on selected Years and Quarters
combined_df = blockCombined[blockCombined['Year'].isin(selected_years_values) & blockCombined['Quarter'].isin(selected_quarters_values)].reset_index(drop=True)


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


# Display the selected year and quarter
year_quarter_options = [
    '2019 Q1', '2019 Q2', '2019 Q3', '2019 Q4', '2020 Q1', '2020 Q2',
    '2020 Q3', '2020 Q4', '2021 Q1', '2021 Q2', '2021 Q3', '2021 Q4',
    '2022 Q1', '2022 Q2', '2022 Q3', '2022 Q4', '2023 Q1', '2023 Q2'
]

year_quarter = st.select_slider('Year and Quarter', options=year_quarter_options)

c1, c2 = st.columns(2)
c1.plotly_chart(show_choropleth_for_number_of_diagnosed(year_quarter), use_container_width=True)
c2.plotly_chart(show_gender_age_tb_bar(year_quarter), use_container_width=True)

st.plotly_chart(create_tb_scatter_plot(year_quarter), use_container_width=True)

c1_, c2_ = st.columns(2)
c1_.plotly_chart(plot_lga_presumptive_cases_trend(lga_choice), use_container_width=True)
c2_.plotly_chart(plot_lga_diagnosed_tb_cases_trend(lga_choice), use_container_width=True)





# Dashboard Main Panel
col = st.columns((5, 2), gap='medium')


with col[0]:
    if block == "Breakdown of activities of all presumptive PTB cases on the clinic during the register":
        
        #if the user picks block 1a
        #this method is from block1.py. It displays all the models needed for block 1.
        #if you want to add more models add them in block1.py
        st.write("Dynamic data")
        vis1A(combined_df, len(selected_years), len(selected_quarters))
        st.write("Static data")

    elif block == "Number of cases broken down by gender and age":
        vis2B(combined_df.iloc[:, 1:])
    else:
        
        #if the user picks block 2a
        st.write("User has picked block 2a")
        ## TODO: Put the models in the code ##
        st.write("Block2a")

## TODO: This does not work if the user picks block 2A ##
# with col[1]:
#     st.markdown("#### Top LGA's")

#     # Sort the DataFrame by "Total number of presumptives" in ascending order
#     combined_df_sorted = combined_df.sort_values(by="Total number of presumptives", ascending=False)

#     # Ensure unique LGA values
#     combined_df_sorted = combined_df_sorted.drop_duplicates(subset=["LGA"])


#     # Check for empty DataFrame and handle accordingly
#     if not combined_df_sorted.empty:
#         max_value = max(combined_df_sorted.Year)
#     else:
#         max_value = 100 


#     # Select and display the desired columns with progress bar configuration
#     st.dataframe(combined_df_sorted[['LGA', 'Total number of presumptives']],
#                  column_order=("LGA", "Total number of presumptives"),
#                  hide_index=True,
#                  width=None
#                  ,column_config={
#                      "LGA": st.column_config.TextColumn("LGA"),
#                      "Total number of presumptives": st.column_config.ProgressColumn(
#                          "Total number of presumptives",
#                          format="%f",
#                          min_value=0,
#                          max_value=max_value,  
#                      )
#                  }
#     )







