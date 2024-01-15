import matplotlib.pyplot as plt
import streamlit as st
def vis1A(combined_df, numYears, numQuarters):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
    

    # Total number of presumptives
    axes[0, 0].hist(combined_df['Total number of presumptives'], bins=20, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Total number of presumptives')
    axes[0, 0].set_xlabel('Number of presumptives')
    axes[0, 0].set_ylabel('Frequency')

    # Total examined with Xpert
    axes[0, 1].hist(combined_df['Total examined with Xpert'], bins=20, color='lightgreen', edgecolor='black')
    axes[0, 1].set_title('Total examined with Xpert')
    axes[0, 1].set_xlabel('Number examined with Xpert')
    axes[0, 1].set_ylabel('Frequency')

    # MTB detected
    axes[1, 0].hist(combined_df['MTB detected'], bins=20, color='lightcoral', edgecolor='black')
    axes[1, 0].set_title('MTB detected')
    axes[1, 0].set_xlabel('Number of MTB detected cases')
    axes[1, 0].set_ylabel('Frequency')

    # Total diagnosed
    axes[1, 1].hist(combined_df['Total diagnosed'], bins=20, color='gold', edgecolor='black')
    axes[1, 1].set_title('Total diagnosed')
    axes[1, 1].set_xlabel('Number of diagnosed cases')
    axes[1, 1].set_ylabel('Frequency')
    

    st.pyplot(fig)

    if(numYears + numQuarters > 2):
        st.write("Graph time")
   