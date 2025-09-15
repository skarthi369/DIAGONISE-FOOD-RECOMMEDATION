import pandas as pd
import streamlit as st
from io import BytesIO
import os

# Function to load data from multiple CSV files
def load_data():
    base_dir = os.path.dirname(__file__)  # Current directory
    file_paths = {
        "Type 2": os.path.join(base_dir, "diabetes_food_type2_100.csv"),
        "Gestational": os.path.join(base_dir, "diabetes_food_gdm_100_with_images.csv"),
        "General (Type 1)": os.path.join(base_dir, "diabetes_food_100.csv")
    }
    
    dataframes = []
    for diabetes_type, file_path in file_paths.items():
        try:
            df = pd.read_csv(file_path)
            df['diabetes_type'] = diabetes_type  # Adding diabetes type for filtering
            dataframes.append(df)
            st.success(f"Loaded data for {diabetes_type}.")
        except FileNotFoundError:
            st.warning(f"Warning: {file_path} not found. Skipping this file.")
        except Exception as e:
            st.error(f"Error loading {file_path}: {e}")
    
    if not dataframes:
        st.error("No data files were loaded successfully. Please check file paths and try again.")
        st.stop()
    
    return pd.concat(dataframes, ignore_index=True)

# Load the data once
food_data = load_data()

# App Title and User Input Form
st.title("Diabetes Weekly Meal Planner")
st.header("Enter Your Preferences")

with st.form(key="user_form"):
    diabetes_type = st.selectbox("Diabetes Type", ["Type 1", "Type 2", "Gestational"])
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    diet_preference = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "No Preference"])
    submit_button = st.form_submit_button(label="Generate Meal Plan")

# Function to filter meals based on diabetes type and preferences
def filter_meals(df, diabetes_type, diet_pref):
    # Define filtering logic based on diabetes type
    filtered_df = df.copy()

    # Set conditions based on diabetes type
    if diabetes_type == "Type 1":
        filtered_df = filtered_df[(filtered_df["Glycemic Index"] <= 55) & 
                                  (filtered_df["Carbohydrates (g)"] >= 20) & 
                                  (filtered_df["Carbohydrates (g)"] <= 60)]
    elif diabetes_type == "Type 2":
        filtered_df = filtered_df[(filtered_df["Glycemic Index"] <= 55) & 
                                  (filtered_df["Carbohydrates (g)"] >= 20) & 
                                  (filtered_df["Carbohydrates (g)"] <= 40) & 
                                  (filtered_df["Calories"] <= 350) & 
                                  (filtered_df["Fiber (g)"] >= 5)]
    else:  # Gestational Diabetes
        filtered_df = filtered_df[(filtered_df["Glycemic Index"] <= 55) & 
                                  (filtered_df["Carbohydrates (g)"] >= 30) & 
                                  (filtered_df["Carbohydrates (g)"] <= 50) & 
                                  (filtered_df["Calories"] >= 300) & 
                                  (filtered_df["Calories"] <= 400) & 
                                  (filtered_df["Fiber (g)"] >= 5) & 
                                  (filtered_df["Proteins (g)"] >= 10)]

    # Filter by diet preference
    if diet_pref != "No Preference":
        filtered_df = filtered_df[filtered_df["Diet Type"] == diet_pref]
    
    return filtered_df

# Generate and display the meal plan
if submit_button:
    st.header(f"Your Weekly Meal Plan for {diabetes_type} Diabetes")
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meal_types = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    
    weekly_plan = {day: {} for day in days}
    
    for day in days:
        for meal_type in meal_types:
            available_meals = filter_meals(food_data, diabetes_type, diet_preference)
            if not available_meals.empty:
                meal = available_meals.sample(1).iloc[0]
                weekly_plan[day][meal_type] = meal
            else:
                weekly_plan[day][meal_type] = None
    
    # Display the plan
    for day in days:
        st.subheader(day)
        for meal_type in meal_types:
            meal = weekly_plan[day][meal_type]
            if meal is not None:
                st.image(meal['image_url'], caption=meal['Food Item'], use_column_width=True)
                st.write(f"{meal_type}: {meal['Food Item']} (GI: {meal['Glycemic Index']}, "
                         f"Carbs: {meal['Carbohydrates (g)']}g, Calories: {meal['Calories']}, "
                         f"Protein: {meal['Proteins (g)']}g, Fat: {meal['Fats (g)']}g, "
                         f"Fiber: {meal['Fiber (g)']}g)")
            else:
                st.write(f"{meal_type}: No suitable option available.")
        st.write("---")

    # Optionally download plan as CSV
    download_data = []
    for day in days:
        for meal_type in meal_types:
            meal = weekly_plan[day][meal_type]
            if meal is not None:
                download_data.append({
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
    
    if download_data:
        download_df = pd.DataFrame(download_data)
        csv = download_df.to_csv(index=False)
        st.download_button("Download Weekly Plan as CSV", csv, "weekly_meal_plan.csv", "text/csv")
    else:
        st.warning("No data available to download.")