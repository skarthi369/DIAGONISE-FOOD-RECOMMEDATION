# # # import pandas as pd
# # import streamlit as st
# # from io import BytesIO

# # # Load the datasets using the provided file paths
# # file_paths = [
# #     "checkfinal/diabetes_food_100.csv",
# #     "checkfinal/diabetes_food_gdm_100_with_images.csv",
# #     "checkfinal/diabetes_food_type2_100.csv"
# # ]

# # # Loading the datasets
# # datasets = [pd.read_csv(file) for file in file_paths]

# # # Combine datasets for easier management
# # food_data = pd.concat(datasets, ignore_index=True)

# # # Data Preprocessing: cleaning column names and relevant information
# # food_data.columns = food_data.columns.str.strip().str.lower().str.replace(' ', '_')
# # food_data.dropna(subset=['food_item'], inplace=True)

# # # App Title
# # st.title("Diabetic Patient Food Recommendation System")

# # # User Input Form
# # with st.sidebar:
# #     st.header("User Information")
# #     age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)
# #     weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, value=70.0, step=0.1)
    
# #     diabetes_type = st.selectbox(
# #         "Select Diabetes Type:",
# #         ["Type 1", "Type 2", "Gestational Diabetes"]
# #     )
    
# #     diet_preference = st.selectbox(
# #         "Dietary Preference:",
# #         ["Vegetarian", "Non-Vegetarian"]
# #     )
    
# #     meal_time = st.selectbox(
# #         "Select Meal Type:",
# #         ["Breakfast", "Lunch", "Dinner", "Snacks"]
# #     )
    
# #     meal_plan_days = st.selectbox("Number of Meal Plan Days:", [3, 7])

# # # Food Recommendation Logic
# # def recommend_foods(diabetes_type, diet_preference, meal_time, days):
# #     # Example filter based on user inputs – modify to match your dataset's filtering logic
# #     filters = (food_data['meal_type'] == meal_time)
    
# #     if diabetes_type == "Type 1":
# #         filters &= (food_data['diabetes_type'].str.contains("1", case=False))
# #     elif diabetes_type == "Type 2":
# #         filters &= (food_data['diabetes_type'].str.contains("2", case=False))
# #     else:
# #         filters &= food_data['diabetes_type'].str.contains("gestational", case=False)
    
# #     if diet_preference == "Vegetarian":
# #         filters &= food_data['dietary_type'] == "Vegetarian"
    
# #     recommended_foods = food_data[filters].sample(n=days, random_state=1)
    
# #     return recommended_foods

# # if st.button("Get Recommendations"):
# #     recommendations = recommend_foods(diabetes_type, diet_preference, meal_time, meal_plan_days)
    
# #     if not recommendations.empty:
# #         st.subheader("Recommended Foods:")
# #         for _, row in recommendations.iterrows():
# #             st.image(row['image_url'], width=150)  # Ensure your dataset has an 'image_url' column
# #             st.write(f"*Food Item:* {row['food_item']}")
# #             st.write(f"*Calories:* {row['calories']}")
# #             st.write(f"*Glycemic Index:* {row['glycemic_index']}")
# #             st.write(f"*Nutrient Breakdown:* Carbs: {row['carbs']}, Protein: {row['protein']}, Fats: {row['fats']}, Fiber: {row['fiber']}")
# #             st.write("---")
# #     else:
# #         st.write("No recommendations available for the selected criteria.")

# # # Function to convert recommendations into a downloadable format
# # def create_downloadable_file(recommendations):
# #     buffer = BytesIO()
# #     recommendations.to_csv(buffer, index=False)
# #     buffer.seek(0)
# #     return buffer

# # if st.button("Download Meal Plan"):
# #     recommendations = recommend_foods(diabetes_type, diet_preference, meal_time, meal_plan_days)
# #     if not recommendations.empty:
# #         buffer = create_downloadable_file(recommendations)
# #         st.download_button(
# #             label="Download Meal Plan",
# #             data=buffer,
# #             file_name="meal_plan.csv",
# #             mime="text/csv"
# #         )
# #     else:
# #         st.error("No recommendations available to download.")

# # # User Guidance
# # st.sidebar.subheader("Helpful Tips")
# # st.sidebar.text("Consult a healthcare provider for meal planning specific to your needs.")

# if st.button("Get Recommendations"):
#     recommendations = recommend_foods(diabetes_type, diet_preference, meal_time, meal_plan_days)
    
#     if not recommendations.empty:
#         st.subheader("Recommended Foods:")
#         for _, row in recommendations.iterrows():
#             st.image(row['image_url'], width=150)  # Ensure your dataset has an 'image_url' column
#             st.write(f"*Food Item:* {row['food_item']}")
#             st.write(f"*Calories:* {row['calories']}")
#             st.write(f"*Glycemic Index:* {row['glycemic_index']}")
#             st.write(f"*Nutrient Breakdown:* Carbs: {row['carbs']}, Protein: {row['protein']}, Fats: {row['fats']}, Fiber: {row['fiber']}")
#             st.write("---")
#     else:
#         st.write("No recommendations available for the selected criteria.")

# # Function to convert recommendations into a downloadable format
# def create_downloadable_file(recommendations):
#     buffer = BytesIO()
#     recommendations.to_csv(buffer, index=False)
#     buffer.seek(0)
#     return buffer

# if st.button("Download Meal Plan"):
#     recommendations = recommend_foods(diabetes_type, diet_preference, meal_time, meal_plan_days)
#     if not recommendations.empty:
#         buffer = create_downloadable_file(recommendations)
#         st.download_button(
#             label="Download Meal Plan",
#             data=buffer,
#             file_name="meal_plan.csv",
#             mime="text/csv"
#         )
#     else:
#         st.error("No recommendations available to download.")

# # User Guidance
# st.sidebar.subheader("Helpful Tips")
# st.sidebar.text("Consult a healthcare provider for meal planning specific to your needs.")
# import streamlit as st
# import pandas as pd
# import random
# import os

# # Function to load data from multiple CSV files
# def load_data():
#     # Define file paths (update these paths as needed)
#     base_dir = os.path.dirname(_file_)  # Directory of the script
#     file_paths = {
#         "Type 2": os.path.join(base_dir, "diabetes_food_type2_100.csv"),
#         "Gestational": os.path.join(base_dir, "diabetes_food_gdm_100_with_images.csv"),
#         "General (Type 1)": os.path.join(base_dir, "diabetes_food_100.csv")
#     }
    
#     dataframes = []
#     for diabetes_type, file_path in file_paths.items():
#         try:
#             df = pd.read_csv(file_path)
#             dataframes.append(df)
#             st.success(f"Loaded {diabetes_type} data from {file_path}")
#         except FileNotFoundError:
#             st.warning(f"Warning: {file_path} not found. Skipping this file.")
#         except Exception as e:
#             st.error(f"Error loading {file_path}: {e}")
    
#     if not dataframes:
#         st.error("No data files were loaded successfully. Please check file paths and try again.")
#         st.stop()
    
#     # Concatenate all available DataFrames
#     return pd.concat(dataframes, ignore_index=True)

# # Load the data
# df = load_data()

# # Streamlit app
# st.title("Diabetes Weekly Meal Planner")

# # Form for user input
# st.header("Enter Your Preferences")
# with st.form(key="user_form"):
#     diabetes_type = st.selectbox("Diabetes Type", ["Type 1", "Type 2", "Gestational"])
#     gender = st.selectbox("Gender", ["Male", "Female", "Other"])
#     diet_preference = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "No Preference"])
#     submit_button = st.form_submit_button(label="Generate Meal Plan")

# # Function to filter meals based on diabetes type and preferences
# def filter_meals(diabetes_type, diet_pref, meal_type):
#     if diabetes_type == "Type 1":
#         # Type 1: GI ≤ 55, Carbs 20-60g
#         filtered_df = df[(df["Glycemic Index"] <= 55) & 
#                          (df["Carbohydrates (g)"] >= 20) & 
#                          (df["Carbohydrates (g)"] <= 60)]
#     elif diabetes_type == "Type 2":
#         # Type 2: GI ≤ 55, Carbs 20-40g, Calories ≤ 350, Fiber ≥ 5g
#         filtered_df = df[(df["Glycemic Index"] <= 55) & 
#                          (df["Carbohydrates (g)"] >= 20) & 
#                          (df["Carbohydrates (g)"] <= 40) & 
#                          (df["Calories"] <= 350) & 
#                          (df["Fiber (g)"] >= 5)]
#     else:  # Gestational Diabetes
#         # Gestational: GI ≤ 55, Carbs 30-50g, Calories 300-400, Fiber ≥ 5g, Protein ≥ 10g
#         filtered_df = df[(df["Glycemic Index"] <= 55) & 
#                          (df["Carbohydrates (g)"] >= 30) & 
#                          (df["Carbohydrates (g)"] <= 50) & 
#                          (df["Calories"] >= 300) & 
#                          (df["Calories"] <= 400) & 
#                          (df["Fiber (g)"] >= 5) & 
#                          (df["Proteins (g)"] >= 10)]
#     # Apply diet preference
#     if diet_pref == "Vegetarian":
#         filtered_df = filtered_df[filtered_df["Diet Type"] == "Vegetarian"]
#     elif diet_pref == "Non-Vegetarian":
#         filtered_df = filtered_df[filtered_df["Diet Type"] == "Non-Vegetarian"]
    
#     # Filter by meal type
#     filtered_df = filtered_df[filtered_df["Meal Type"] == meal_type]
#     return filtered_df

# # Generate weekly meal plan only after form submission
# if submit_button:
#     st.header(f"Your Weekly Meal Plan for {diabetes_type} Diabetes")
#     days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#     meal_types = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    
#     # Dictionary to store the plan
#     weekly_plan = {day: {} for day in days}
    
#     # Populate the plan
#     for day in days:
#         for meal_type in meal_types:
#             available_meals = filter_meals(diabetes_type, diet_preference, meal_type)
#             if not available_meals.empty:
#                 # Randomly select one meal for variety
#                 meal = available_meals.sample(1).iloc[0]
#                 weekly_plan[day][meal_type] = meal
#             else:
#                 weekly_plan[day][meal_type] = None
    
#     # Display the plan
#     for day in days:
#         st.subheader(day)
#         for meal_type in meal_types:
#             meal = weekly_plan[day][meal_type]
#             if meal is not None:
#                 st.write(f"{meal_type}: {meal['Food Item']}** (GI: {meal['Glycemic Index']}, "
#                          f"Carbs: {meal['Carbohydrates (g)']}g, Calories: {meal['Calories']}, "
#                          f"Protein: {meal['Proteins (g)']}g, Fat: {meal['Fats (g)']}g, "
#                          f"Fiber: {meal['Fiber (g)']}g)")
#             else:
#                 st.write(f"{meal_type}:** No suitable option available.")
#         st.write("---")
    
#     # Tailored advice
#     if diabetes_type == "Type 1":
#         st.write("*Note:* Adjust portion sizes and insulin doses as per your doctor's advice.")
#     elif diabetes_type == "Type 2":
#         st.write("*Note:* Focus on portion control and consult your doctor for weight management goals.")
#     else:  # Gestational
#         st.write("*Note:* Ensure balanced nutrition for you and your baby. Consult your doctor or dietitian.")
    
#     # Optional: Download the plan as CSV
#     plan_data = []
#     for day in days:
#         for meal_type in meal_types:
#             meal = weekly_plan[day][meal_type]
#             if meal is not None:
#                 plan_data.append({
#                     "Day": day,
#                     "Meal Type": meal_type,
#                     "Food Item": meal["Food Item"],
#                     "Glycemic Index": meal["Glycemic Index"],
#                     "Calories": meal["Calories"],
#                     "Carbohydrates (g)": meal["Carbohydrates (g)"],
#                     "Proteins (g)": meal["Proteins (g)"],
#                     "Fats (g)": meal["Fats (g)"],
#                     "Fiber (g)": meal["Fiber (g)"]
#                 })
#     if plan_data:
#         plan_df = pd.DataFrame(plan_data)
#         csv = plan_df.to_csv(index=False)
#         st.download_button("Download Weekly Plan as CSV", csv, "weekly_meal_plan.csv", "text/csv")
# else:
#     st.write("Please fill in your preferences and submit to see your weekly meal plan.")
import streamlit as st
import pandas as pd

# CSV data
data = {
    "Diet Type": ["Vegetarian", "Vegetarian", "Vegetarian"],
    "Meal Type": ["Breakfast", "Breakfast", "Breakfast"],
    "Food Item": ["Oats Pongal", "Ragi Idiyappam", "Vegetable Poha"],
    "Glycemic Index": [44, 46, 41],
    "Calories": [389, 272, 301],
    "Carbohydrates (g)": [48, 22, 22],
    "Proteins (g)": [19, 5, 8],
    "Fats (g)": [7, 6, 6],
    "Fiber (g)": [4, 3, 9],
    "Image_URL": [
        "https://premasculinary.com/wp-content/uploads/2021/07/Oats-Pongal.jpg",
        "https://i0.wp.com/cookingfromheart.com/wp-content/uploads/2020/03/Ragi-Idiyappam-2.jpg?resize=683,1024&ssl=1",
        "http://slurrp.club/wp-content/uploads/2019/05/DSC_0935.jpg"
    ]
}

# Load CSV data into a DataFrame
df = pd.DataFrame(data)

# Filter meals by diet type and meal type
def filter_meals(diet_type, meal_type):
    return df[(df["Diet Type"] == diet_type) & (df["Meal Type"] == meal_type)]

# Create a meal plan
def create_meal_plan(diet_type, meal_types, days):
    meal_plan = {}
    for day in days:
        meal_plan[day] = {}
        for meal_type in meal_types:
            meals = filter_meals(diet_type, meal_type)
            if not meals.empty:
                meal_plan[day][meal_type] = meals.sample(1).iloc[0]
            else:
                meal_plan[day][meal_type] = None
    return meal_plan

# Main app
def main():
    st.title("Meal Plan App")

    # User input
    diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
    meal_types = ["Breakfast", "Lunch", "Dinner"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    show_nutrients = st.checkbox("Show Nutrients")

    # Create meal plan
    weekly_plan = create_meal_plan(diet_type, meal_types, days)

    # Display meal plan
    for day in days:
        with st.expander(day, expanded=True):
            for meal_type in meal_types:
                meal = weekly_plan[day][meal_type]
                col1, col2 = st.columns([3, 1])
                with col1:
                    if meal is not None:
                        st.write(f"{meal_type}: {meal['Food Item']}")
                        if show_nutrients:
                            st.write(f"GI: {meal['Glycemic Index']}, Carbs: {meal['Carbohydrates (g)']}g, "
                                     f"Calories: {meal['Calories']}, Protein: {meal['Proteins (g)']}g, "
                                     f"Fat: {meal['Fats (g)']}g, Fiber: {meal['Fiber (g)']}g")
                        if meal['Image_URL'] is not None and meal['Image_URL'] != '':
                            try:
                                st.image(meal['Image_URL'], width=200)
                            except Exception as e:
                                st.warning(f"Failed to load image for {meal['Food Item']}: {e}")
                    else:
                        st.write(f"{meal_type}:** No suitable option available.")
                with col2:
                    if meal is not None and st.button("Swap", key=f"{day}_{meal_type}"):
                        available_meals = filter_meals(diet_type, meal_type)
                        if not available_meals.empty:
                            new_meal = available_meals.sample(1).iloc[0]
                            weekly_plan[day][meal_type] = new_meal
                            st.experimental_rerun()

if __name__ == "__main__":
    main()