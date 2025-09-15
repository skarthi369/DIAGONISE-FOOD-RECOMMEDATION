import streamlit as st
import pandas as pd
from datetime import datetime
import requests  # Added for checking image URLs
import random
import os

# Set page configuration
st.set_page_config(page_title="Diabetes Meal Planner", layout="wide")

# Function to validate image URL
def is_valid_image_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    try:
        response = requests.get(url, headers=headers, timeout=5, stream=True, verify=False)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').lower()
            return 'image' in content_type or url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))
        return False
    except:
        return False

# Function to load data from multiple CSV files with caching
@st.cache_data
def load_data():
    file_paths = [
        "diabetes_food_100_with_imagesnew.csv",
        "diabetesnew.csv",
        "gestational diabeticnew.csv"
    ]
    
    dataframes = []
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            dataframes.append(df)
        except Exception as e:
            st.warning(f"Warning: {file_path} could not be loaded. Error: {str(e)}")
            continue
    
    if not dataframes:
        st.error("No data files were loaded successfully. Please check file paths and try again.")
        st.stop()
    
    # Concatenate all available DataFrames
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # Ensure required columns exist and convert data types
    required_columns = {
        "Food Item": str,
        "Glycemic Index": float,
        "Calories": float,
        "Carbohydrates (g)": float,
        "Proteins (g)": float,
        "Fats (g)": float,
        "Fiber (g)": float,
        "Diet Type": str,
        "Meal Type": str
    }
    
    # Check for missing columns
    missing_columns = [col for col in required_columns.keys() if col not in combined_df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        st.stop()
    
    # Convert data types and handle missing values
    for col, dtype in required_columns.items():
        if col in ["Food Item", "Diet Type", "Meal Type"]:
            combined_df[col] = combined_df[col].astype(str)
        else:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce').fillna(0).astype(float)
    
    return combined_df

# Load the data
df = load_data()

# Streamlit app
st.title("Diabetes Weekly Meal Planner")
st.markdown("Generate a personalized weekly meal plan based on your diabetes type and preferences.")

# Sidebar for additional options
st.sidebar.header("Settings")
show_nutrients = st.sidebar.checkbox("Show Nutritional Details", value=True)
show_images = st.sidebar.checkbox("Show Food Images", value=True)

# Form for user input
with st.form(key="meal_planner"):
    col1, col2 = st.columns(2)
    
    with col1:
        diabetes_type = st.selectbox(
            "Diabetes Type",
            ["Type 1", "Type 2", "Gestational"],
            help="Select your type of diabetes"
        )
        
        diet_preference = st.selectbox(
            "Diet Preference",
            ["No Preference", "Vegetarian", "Non-Vegetarian"],
            help="Select your dietary preference"
        )
    
    with col2:
        activity_level = st.select_slider(
            "Activity Level",
            options=["Low", "Moderate", "High"],
            value="Moderate",
            help="Select your typical activity level"
        )
        
        num_days = st.slider("Number of Days", 1, 7, 7, help="Select how many days for your meal plan.")
    
    submit_button = st.form_submit_button(label="Generate Meal Plan")

# Function to filter meals based on diabetes type and preferences
def filter_meals(diabetes_type, diet_pref, meal_type):
    if diabetes_type == "Type 1":
        # Type 1: More flexible criteria for all meal types
        filtered_df = df[(df["Glycemic Index"] <= 55) & 
                        (df["Carbohydrates (g)"] >= 15) &  # Lowered minimum carbs
                        (df["Carbohydrates (g)"] <= 60)]
    elif diabetes_type == "Type 2":
        # Type 2: Adjusted criteria based on meal type
        if meal_type in ["Breakfast", "Lunch", "Dinner"]:
            filtered_df = df[(df["Glycemic Index"] <= 55) & 
                           (df["Carbohydrates (g)"] >= 20) & 
                           (df["Carbohydrates (g)"] <= 45) &  # Increased max carbs
                           (df["Calories"] <= 400) &  # Increased max calories
                           (df["Fiber (g)"] >= 3)]   # Lowered min fiber
        else:  # Snacks
            filtered_df = df[(df["Glycemic Index"] <= 55) & 
                           (df["Carbohydrates (g)"] >= 10) &  # Lower carbs for snacks
                           (df["Carbohydrates (g)"] <= 30) & 
                           (df["Calories"] <= 250) & 
                           (df["Fiber (g)"] >= 2)]
    else:  # Gestational Diabetes
        # Gestational: Adjusted criteria based on meal type
        if meal_type in ["Breakfast", "Lunch", "Dinner"]:
            filtered_df = df[(df["Glycemic Index"] <= 55) & 
                           (df["Carbohydrates (g)"] >= 25) & 
                           (df["Carbohydrates (g)"] <= 50) & 
                           (df["Calories"] >= 250) & 
                           (df["Calories"] <= 450) & 
                           (df["Fiber (g)"] >= 3) & 
                           (df["Proteins (g)"] >= 8)]
        else:  # Snacks
            filtered_df = df[(df["Glycemic Index"] <= 55) & 
                           (df["Carbohydrates (g)"] >= 15) & 
                           (df["Carbohydrates (g)"] <= 30) & 
                           (df["Calories"] >= 150) & 
                           (df["Calories"] <= 300) & 
                           (df["Fiber (g)"] >= 2) & 
                           (df["Proteins (g)"] >= 5)]
    
    # Apply diet preference if specified
    if diet_pref != "No Preference":
        filtered_df = filtered_df[filtered_df["Diet Type"] == diet_pref]
    
    # Apply meal type filter
    filtered_df = filtered_df[filtered_df["Meal Type"] == meal_type]
    
    return filtered_df

# Generate and display meal plan
if submit_button:
    st.header(f"Your Weekly Meal Plan for {diabetes_type} Diabetes")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][:num_days]
    meal_types = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    
    # Dictionary to store the plan
    weekly_plan = {day: {} for day in days}
    used_meals = set()  # Track used meals to avoid repetition
    
    # Populate the plan
    for day in days:
        for meal_type in meal_types:
            available_meals = filter_meals(diabetes_type, diet_preference, meal_type)
            # Remove already used meals
            available_meals = available_meals[~available_meals["Food Item"].isin(used_meals)]
            if not available_meals.empty:
                meal = available_meals.sample(1).iloc[0]
                weekly_plan[day][meal_type] = meal
                used_meals.add(meal["Food Item"])
            else:
                # If no unique meals left, allow reuse
                available_meals = filter_meals(diabetes_type, diet_preference, meal_type)
                if not available_meals.empty:
                    meal = available_meals.sample(1).iloc[0]
                    weekly_plan[day][meal_type] = meal
                else:
                    weekly_plan[day][meal_type] = None
    
    # Display the meal plan with expanders and images
    for day in days:
        with st.expander(day, expanded=True):
            for meal_type in meal_types:
                meal = weekly_plan[day][meal_type]
                if meal is not None:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{meal_type}: {meal['Food Item']}**")
                        if show_nutrients:
                            st.write(f"GI: {meal['Glycemic Index']}, Carbs: {meal['Carbohydrates (g)']}g, "
                                   f"Calories: {meal['Calories']}, Protein: {meal['Proteins (g)']}g, "
                                   f"Fat: {meal['Fats (g)']}g, Fiber: {meal['Fiber (g)']}g")
                    
                    with col2:
                        if show_images and 'Image_URL' in meal and meal['Image_URL']:
                            if is_valid_image_url(meal['Image_URL']):
                                st.image(meal['Image_URL'], caption=meal['Food Item'], width=200)
                            else:
                                st.info("Image not available")
                else:
                    st.write(f"**{meal_type}:** No suitable option available.")
    
    # Nutritional summary and health tips
    total_calories = sum(meal["Calories"] for day in weekly_plan.values() 
                        for meal in day.values() if meal is not None)
    
    st.write(f"**Total Calories for the Week:** {total_calories:.0f}")
    
    with st.expander("Health Tips"):
        tips = {
            "Type 1": "Adjust portion sizes and insulin doses as per your doctor's advice. Monitor blood sugar regularly.",
            "Type 2": "Focus on portion control and consult your doctor for weight management goals. Include regular physical activity.",
            "Gestational": "Ensure balanced nutrition for you and your baby. Consult your doctor or dietitian for prenatal care."
        }
        st.write(tips[diabetes_type])
    
    # Download options
    plan_data = []
    for day in days:
        for meal_type in meal_types:
            meal = weekly_plan[day][meal_type]
            if meal is not None:
                plan_data.append({
                    "Day": day,
                    "Meal Type": meal_type,
                    "Food Item": meal["Food Item"],
                    "Glycemic Index": meal["Glycemic Index"],
                    "Calories": meal["Calories"],
                    "Carbohydrates (g)": meal["Carbohydrates (g)"],
                    "Proteins (g)": meal["Proteins (g)"],
                    "Fats (g)": meal["Fats (g)"],
                    "Fiber (g)": meal["Fiber (g)"]
                })
    
    if plan_data:
        plan_df = pd.DataFrame(plan_data)
        csv = plan_df.to_csv(index=False)
        st.download_button(
            "Download Weekly Plan as CSV",
            csv,
            f"meal_plan_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
else:
    st.info("Fill in your preferences above and click 'Generate Meal Plan' to get started!")
