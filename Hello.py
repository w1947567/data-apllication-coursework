import pandas as pd
import streamlit as st
import pip as pip
from PIL import Image
import plotly.express as px 


# Title of the Dashboard
st.title("Wastewater Discharges Per Year and Per Country")

# File uploader
uploaded_file = st.file_uploader("Upload your file", type="xlsx")

if uploaded_file is not None:
    try:
        
        df = pd.read_excel(uploaded_file)
        
        # If statement to check if Data frame is not empty
        if not df.empty:
            # Present the entire DataFrame
            st.write("Uploaded DataFrame:")
            st.write(df)
            
            # Display specific columns
            st.write("Selected Columns:")
            selected_columns = st.multiselect("Select columns to display", df.columns)
            if selected_columns:
                st.write(df[selected_columns])
            
            # Columns for display
            export_columns = st.multiselect("Select columns to export", df.columns)
            if st.button("Export Selected Columns"):
                selected_df = df[export_columns]
                st.write(selected_df)
        else:
            st.write("The uploaded file is empty.")
            
        # Sidebar widgets for country
        st.sidebar.header("Select filter:")
        selected_countries=[]
        if "Country" in df.columns:
            selected_countries= st.sidebar.multiselect(
                "Select the country",
                options=df["Country"].unique(),
                default=df["Country"].unique().tolist()
            )
        else:
            st.sidebar.write("Country column not found.")
            
        
        #Sidebar widegts for year:
        st.sidebar.header("Select filter:")
        selected_years=[]
        if "Year" in df.columns:
            selected_years= st.sidebar.multiselect(
                "Select the year",
                options=df["Year"].unique(),
                default=df["Year"].unique().tolist()
            )
        else:
             st.sidebar.write("Year column not found.")
             
        
        # DataFrame based on selected countries and years
        filtered_df = df[df["Country"].isin(selected_countries) & df["Year"].isin(selected_years)]

        # MAP for volume of discharges to inland waters
        if not filtered_df.empty:
            figure = px.choropleth(filtered_df, 
                        locations="Country",
                        locationmode="country names",
                        color="Total discharges to Inland waters(million m3)",  # Remove extra space
                        hover_name="Country",
                        animation_frame="Year",
                        title="Wastewater Discharges Per Year and Per Country to inland waters (million m3)",
                        labels={"Total discharges to Inland waters(million m3)": "Total Discharges (million m3)"}
                        )
            figure.update_layout(geo=dict(showcoastlines=True))
            st.plotly_chart(figure)
        else:
            st.write("No data available for the selected filters.")

        # MAP for volume of discharges to sea 
        if not filtered_df.empty:
            figure = px.choropleth(filtered_df, 
                        locations="Country",
                        locationmode="country names",
                        color="Total discharges to the sea(million m3)",  # Remove extra space
                        hover_name="Country",
                        animation_frame="Year",
                        title="Wastewater Discharges Per Year and Per Country to the sea (million m3)",
                        labels={"Total discharges to the sea(million m3)": "Total Discharges (million m3)"}
                       )
            figure.update_layout(geo=dict(showcoastlines=True))
            st.plotly_chart(figure)
        else:
            st.write("No data available for the selected filters.")
    
        # Define sidebar widget for selecting category
        selected_category = st.multiselect("Select category", 
                                    ["Agricultural wastewater", "Urban wastewater", "Industrial wastewater"])

        # Plot bar charts based on selected categories
        for category in selected_category:
            if category == "Agricultural wastewater":
                figure = px.bar(df, x='Year', y='Agricultural (incl. forestry + fisheries) wastewater, all sources, direct discharges(million m3)',
                     title="Agricultural Wastewater Discharges Over the Years",
                     labels={"Agricultural (incl. forestry + fisheries) wastewater, all sources, direct discharges(million m3)": "Volume (million m3)"})
                st.plotly_chart(figure)
            elif category == "Urban wastewater":
                figure = px.bar(df, x='Year', y='Urban wastewater, all sources, discharged without treatment(million m3)',
                     title="Urban Wastewater Discharges Over the Years",
                     labels={"Urban wastewater, all sources, discharged without treatment(million m3)": "Volume (million m3)"})
                st.plotly_chart(figure)
            elif category == "Industrial wastewater":
                figure = px.bar(df, x='Year', y='Industrial wastewater, all sources, discharged without treatment(million m3)',
                     title="Industrial Wastewater Discharges Over the Years",
                     labels={"Industrial wastewater, all sources, discharged without treatment(million m3)": "Volume (million m3)"})
                st.plotly_chart(figure)
    except Exception as e:
        st.error(f"An error occurred: {e}")

