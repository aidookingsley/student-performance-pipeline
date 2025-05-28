import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import warnings
from pathlib import Path
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from s3_utils import upload_file_to_s3
from azure_sb import upload_file_to_azure
import subprocess
sys.path.append('scripts')
import visualize
# Streamlit config
st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="📊",
    layout="wide",
)

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Set project root
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

# Title
st.title("📚 Student Performance Analysis")
st.sidebar.title("Navigation")

# Load transformed data
df_path = "output/transformed_students.csv"
if not os.path.exists(df_path):
    st.error("The dataset file does not exist.")
    st.stop()

df = pd.read_csv(df_path)

# Sidebar filters
st.sidebar.header("Filter Students")
gender_options = ["All"] + sorted(df['sex'].unique().tolist())
gender = st.sidebar.selectbox("Select Gender:", options=gender_options)
age = st.sidebar.slider(
    "Select Age Range:",
    min_value=int(df['age'].min()),
    max_value=int(df['age'].max()),
    value=(int(df['age'].min()), int(df['age'].max()))
)

# Filtered DataFrame
filtered_df = df[
    ((df['sex'] == gender) if gender != "All" else True) &
    (df['age'] >= age[0]) &
    (df['age'] <= age[1])
]

st.write(f"🎯 Filtered Students: {len(filtered_df)}")
st.dataframe(filtered_df)

# Sidebar Option Selection
options = ["Visualize Data", "Predict Final Grade"]
selected_option = st.sidebar.selectbox("Choose an option:", options)

# --- Visualization Section ---
if selected_option == "Visualize Data":
    st.header("📊 Visualizations")

    import subprocess
    from datetime import datetime
    import humanize  # Import humanize library

    # Regenerate Button
    if st.button("🔄 Regenerate Visualizations"):
        try:
            result = subprocess.run(
                [sys.executable, "visualize.py"],
                capture_output=True,
                text=True,
                check=True
            )
            st.success("Visualizations regenerated successfully!")
        except subprocess.CalledProcessError as e:
            st.error("Failed to regenerate visualizations.")
            st.text(e.stderr)

    # Directory and file check
    image_dir = Path("output")
    image_files = sorted(image_dir.glob("*.png"))

    if not image_files:
        st.warning("No visualizations found. Please run visualize.py first.")

        try:
            result = subprocess.run(
                [sys.executable, "visualize.py"],
                capture_output=True,
                text=True,
                check=True
            )
            st.success("Visualizations generated successfully!")
        except subprocess.CalledProcessError as e:
            st.error("Failed to generate visualizations.")
            st.text(e.stderr)
        st.stop()
    else:
        # Get latest modification time
        latest_file = max(image_files, key=lambda f: f.stat().st_mtime)
        last_updated_timestamp = latest_file.stat().st_mtime
        last_updated = datetime.fromtimestamp(last_updated_timestamp)
        time_since_update = humanize.naturaltime(last_updated)

        # Set badge color based on time since last update
        if (datetime.now() - last_updated).days >= 1:
            badge_color = "red"
        elif (datetime.now() - last_updated).days < 1:
            badge_color = "green"
        else:
            badge_color = "yellow"

        st.markdown(f"🕒 Visuals last updated: **{time_since_update}**", unsafe_allow_html=True)

        # Display the last updated badge
        st.markdown(
            f'<p style="background-color:{badge_color}; color:white; font-size: 16px; padding: 5px; border-radius: 5px; text-align: center;">'
            f'Visuals are up-to-date: {time_since_update}</p>', unsafe_allow_html=True)

        # Display all visualizations
        for image_file in image_files:
            title = image_file.stem.replace("_", " ").title()
            st.subheader(title)
            st.image(str(image_file), use_container_width=True)


# --- Prediction Section ---
if selected_option == "Predict Final Grade":
    st.header("🧠 Predict Final Grade Using ML")

    # Features and target
    try:
        features = filtered_df[['studytime', 'G_avg', 'absences']]
        target = filtered_df['G3']

        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.2, random_state=42
        )

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)

        st.write(f"✅ Mean Squared Error: {mse:.2f}")

        st.subheader("🔍 Feature Importance")
        importances = pd.Series(model.feature_importances_, index=features.columns)
        st.bar_chart(importances.sort_values(ascending=False))

        if st.checkbox("Save Predictions"):
            pred_df = pd.DataFrame(predictions, columns=['Predicted Final Grade'])
            pred_df.to_csv("output/predictions.csv", index=False)
            st.success("Predictions saved to `output/predictions.csv`")

        if os.path.exists("output/predictions.csv"):
            with open("output/predictions.csv", "rb") as f:
                st.download_button(
                    label="⬇️ Download Predictions",
                    data=f,
                    file_name="predictions.csv",
                    mime="text/csv"
                )
    except Exception as e:
        st.error(f"Prediction error: {e}")

# --- Optional Visual Explorations ---
st.sidebar.markdown("---")
if st.sidebar.checkbox("More Visuals"):
    st.subheader("Gender vs Final Grade")
    fig, ax = plt.subplots()
    sns.boxplot(x='sex', y='G3', data=filtered_df, ax=ax)
    st.pyplot(fig)

    st.subheader("Class Failures vs Final Grade")
    fig, ax = plt.subplots()
    sns.boxplot(x='failures', y='G3', data=filtered_df, ax=ax)
    st.pyplot(fig)

    st.subheader("Study Time vs Final Grade")
    fig, ax = plt.subplots()
    sns.boxplot(x='studytime', y='G3', data=filtered_df, ax=ax)
    st.pyplot(fig)

    st.subheader("Absences vs Final Grade")
    fig, ax = plt.subplots()
    sns.boxplot(x='absences', y='G3', data=filtered_df, ax=ax)
    st.pyplot(fig)

    st.subheader("Mother’s Education vs Final Grade")
    fig, ax = plt.subplots()
    sns.boxplot(x='Medu', y='G3', data=filtered_df, ax=ax)
    st.pyplot(fig)

    st.subheader("Parental Cohabitation vs Final Grade")
    fig, ax = plt.subplots()
    sns.boxplot(x='Pstatus', y='G3', data=filtered_df, ax=ax)
    st.pyplot(fig)

# --- Downloads ---
st.sidebar.markdown("---")
st.sidebar.header("📁 Downloads")

# Download transformed data
transformed_data_path = "output/transformed_students.csv"
if os.path.exists(transformed_data_path):
    with open(transformed_data_path, "rb") as f:
        st.sidebar.download_button(
            label="⬇️ Download Transformed Data",
            data=f,
            file_name="transformed_students.csv",
            mime="text/csv"
        )
else:
    st.sidebar.warning("Transformed data file not found.")

# Download raw data
raw_data_path = "data/student.txt"
if os.path.exists(raw_data_path):       
    with open(raw_data_path, "rb") as f:  
        st.sidebar.download_button("   Download Raw Data", data=f, file_name="data/student.txt", mime="text/txt")
else:
    st.sidebar.warning("Raw data file not found.")

# --- Upload to S3 ---
st.sidebar.markdown("---")
st.sidebar.header("☁️ Upload to S3")
if st.sidebar.button("Upload Transformed Data to S3"):
    bucket_name = os.getenv("S3_BUCKET_NAME")
    object_name = "transformed_students.csv"
    if upload_file_to_s3(df_path, bucket_name, object_name):
        st.success(f"Uploaded {df_path} to S3 bucket {bucket_name}/{object_name}")
    else:
        st.error("Failed to upload to S3")

# Upload predictions to S3
if st.sidebar.button("Upload Predictions to S3"):
    bucket_name = os.getenv("S3_BUCKET_NAME")
    object_name = "predictions.csv"
    if os.path.exists("output/predictions.csv"):
        if upload_file_to_s3("output/predictions.csv", bucket_name, object_name):
            st.success(f"Uploaded predictions to S3 bucket {bucket_name}/{object_name}")
        else:
            st.error("Failed to upload predictions to S3")
    else:
        st.error("Predictions file does not exist.")


# --- Upload transto Azure Blob Storage ---
if st.sidebar.button("Upload Transformed Data to Azure Blob Storage"):
    container_name = os.getenv("AZURE_CONTAINER_NAME")
    blob_name = "output/transformed_students.csv"
    if upload_file_to_azure(df_path, container_name, blob_name):
        st.success(f"Uploaded {df_path} to Azure Blob Storage {container_name}/{blob_name}")
    else:
        st.error("Failed to upload to Azure Blob Storage")