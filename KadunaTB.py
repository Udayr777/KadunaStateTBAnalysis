# importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt
from views.blocks.block1 import vis1A
from views.blocks.block2a import block2aTBCases, block2aDiagQtr, block2aDistLGA, block2aReleationship
from views.blocks.visualsblock1 import plot_lga_presumptive_cases_trend, plot_lga_diagnosed_tb_cases_trend, show_choropleth_for_number_of_diagnosed, show_gender_age_tb_bar, kaduna_lgas, create_tb_cases_plot, create_tb_scatter_plot
from views.blocks.block2d import block2dTBHIV, create_age_group_distribution_chart

from views.blocks.block2b import vis2B

from scripts.spatiotemporal_cluster import get_hiv_cluster_plot, get_tb_cluster_plot

# Page configuration
st.set_page_config(
    page_title = "Kaduna State Tuberculosis",
    page_icon = "❤️",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

alt.themes.enable("dark")

st.title('Tuberculosis Analysis in Kaduna')

dataType = ["Breakdown of activities of all presumptive PTB cases on the clinic during the register", "Quarterly breakdown of all TB cases registered during the quarter by category and type of diagnosis", "Number of cases broken down by gender and age","Block 2d"]

gps_facility_df = pd.read_csv("Datasets/Misc/gps_facility_final.csv")

# Sidebar for Slected Year
with st.sidebar:
    st.sidebar.image("images/Kaduna chapter logo.jpg")
    st.title("❤️ Kaduna State Tuberculosis Dashboard")

    #which block the user want to see
    block = st.selectbox("Dataset", options = dataType )

    #block 1a
    if block == "Breakdown of activities of all presumptive PTB cases on the clinic during the register":
        blockCombined = pd.read_csv("Datasets/block1a/block1a_2019_to_2023_processed.csv")

    #block 2b and block 2c combined in block2b folder
    elif block == "Number of cases broken down by gender and age":
        blockCombined = pd.read_csv("Datasets/block2b/block2b_19_to_23.csv")

    elif block == "Quarterly breakdown of all TB cases registered during the quarter by category and type of diagnosis":
        blockCombined = pd.read_csv("Datasets/block2a/block2a_full_data_q.csv")
    else:
        # blockCombined = pd.read_csv("Datasets/block2d/block2d_all_years_processed.csv")
        blockCombined = pd.read_csv("Datasets/block2d/combined_data.csv")




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
    #st.dataframe(combined_df.iloc[:, 1:])
else:
    st.write("No data matches the selected criteria.")


if block == "Breakdown of activities of all presumptive PTB cases on the clinic during the register":
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
        
#if the user picks block 2a
elif block == "Number of cases broken down by gender and age":
    vis2B(combined_df.iloc[:, 1:])
    
elif block == "Quarterly breakdown of all TB cases registered during the quarter by category and type of diagnosis":
    #if the user picks block 2a
    ## TODO: Put the models in the code ##
    st.write("Block2a")

    c3_, c4_ = st.columns(2)
    c5_, c6_ = st.columns(2)
    fig1 = block2aTBCases(combined_df)
    fig2 = block2aDiagQtr(combined_df)
    fig3 = block2aDistLGA(combined_df)
    # fig4 = block2aTotalTBCasesOverTime(combined_df)
    fig5 = block2aReleationship(combined_df)
    
    # fig3 = block2aDiagQtrSum(combined_df)
    c3_.plotly_chart(fig1, use_container_width=True)
    c4_.plotly_chart(fig2, use_container_width=True)
    c5_.plotly_chart(fig3, use_container_width=True)
    # c6_.plotly_chart(fig4, use_container_width=True)
    c6_.plotly_chart(fig5, use_container_width=True)

else:
    fig = block2dTBHIV(combined_df)
    st.plotly_chart(fig, use_container_width=True)

    data = {
    'Year_Quarter': ['2022Q1', '2022Q1', '2022Q2', '2022Q2'],
    'LGA': ['LGA1', 'LGA2', 'LGA1', 'LGA2'],
    'Sex': ['Male', 'Female', 'Male', 'Female'],
    '0 to 4': [10, 15, 8, 12],
    '5 to 14': [20, 25, 18, 22],
    '15 to 24': [15, 30, 25, 20],
    '25 to 34': [12, 18, 10, 15],
    '35 to 44': [8, 12, 6, 10],
    '45 to 54': [5, 10, 8, 12],
    '55 to 64': [3, 5, 4, 7],
    '> 65': [1, 2, 2, 3],
}
    
    # year_quarter_options = sorted(data['Year_Quarter'].unique())
    st.title("TB-HIV Cases Visualization")
    selected_year_quarter = st.selectbox("Select Year and Quarter", sorted(set(data['Year_Quarter'])))

    # Create and display the chart
    fig = create_age_group_distribution_chart(pd.DataFrame(data), selected_year_quarter)
    st.plotly_chart(fig)


    
    
    
    







if selected_years and selected_quarters:
    st.write("raw data")
    st.dataframe(combined_df.iloc[:, 1:])
else:
    st.write("No data matches the selected criteria.")


# st.subheader("Spatiotemporal Clustering using ST-DBSCAN")
# st.write("These maps show spatiotemporal clusters of high volume of TB cases (left) and high volume of HIV and TB co-infections (right) within Kaduna")
# st.markdown("* LGA regions are color coded per legend")
# st.markdown("* Points represent healthcare facilities and are color coded by the spatiotemporal cluster designation")
# st.markdown("* Point sizes are indicative of disease burden - number of TB cases (left) and HIV co-infection rate (right)")
# st.markdown("* A st_dbscan_label of -1 indicates these facilities do not fall within a cluster")

# c1_stdb, c2_stdb = st.columns(2)
#c1_stdb.plotly_chart(get_tb_cluster_plot(), use_container_width=True)
#c2_stdb.plotly_chart(get_hiv_cluster_plot(), use_container_width=True)