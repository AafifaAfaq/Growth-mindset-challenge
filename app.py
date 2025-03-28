import streamlit as st
import pandas as pd
from io import BytesIO

# Page Configurations
st.set_page_config(page_title="Data Cleaner", layout="wide")

# Custom CSS for Styling
st.markdown("""
   <style>
    .title { 
        font-size: 3.5rem; 
        font-weight: bold; 
        color: #2C3E50; 
        text-align: center; 
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    
    .subheader { 
        font-size: 1.8rem; 
        color: #34495E; pip show streamlit

        font-weight: 600; 
        margin-top: 25px;
        text-align: left;
        border-bottom: 3px solid #3498DB;
        padding-bottom: 5px;
    }
    
    .divider { 
        border-bottom: 3px solid #BDC3C7; 
        margin: 25px 0; 
    }
    
    .success-msg { 
        font-size: 1.2rem; 
        color: #27AE60; 
        font-weight: bold; 
        background-color: #EAF7EC; 
        padding: 10px; 
        border-radius: 5px;
        text-align: center;
        box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.1);
    }
</style>

""", unsafe_allow_html=True)

# Title Section
st.markdown('<p class="title">🧹 Data Cleaner</p>', unsafe_allow_html=True)
st.write("📂 Upload CSV or Excel files, clean the data, and convert formats.")

# File Upload Section
files = st.file_uploader("Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        # Display File Name
        st.markdown(f'<p class="subheader">📄 {file.name} - Preview</p>', unsafe_allow_html=True)
        st.dataframe(df.head())

        # Remove Duplicates
        if st.checkbox(f"🗑️ Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.markdown('<p class="success-msg">✅ Duplicates removed successfully!</p>', unsafe_allow_html=True)
            st.dataframe(df.head())

        # Fill Missing Values
        if st.checkbox(f"🛠️ Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)
            st.markdown('<p class="success-msg">✅ Missing values filled!</p>', unsafe_allow_html=True)
            st.dataframe(df.head())

        # Column Selection
        selected_columns = st.multiselect(f"📌 Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show Chart
        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include='number').empty:
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Format Conversion
        format_choice = st.radio(f"📥 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"📤 Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button("📥 Download File", data=output, file_name=new_name, mime=mime)
            output.close()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


    st.markdown('<p class="success-msg" style="text-align: center;">🎉 All files processed successfully!</p>', unsafe_allow_html=True)

else:
    st.write("No files uploaded yet.")