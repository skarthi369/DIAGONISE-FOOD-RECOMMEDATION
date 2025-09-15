# Diabetes Meal Planner

A Streamlit web application that generates personalized meal plans for people with different types of diabetes (Type 1, Type 2, and Gestational).

## Features

- Personalized meal planning based on:
  - Diabetes Type (Type 1, Type 2, Gestational)
  - Diet Preference (Vegetarian/Non-Vegetarian)
  - Number of days (1-7)
- Nutritional information for each meal
- Weekly nutritional summary
- Meal swapping functionality
- Export meal plans to CSV
- Health tips specific to diabetes type

## Installation

1. Install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)

2. Clone or download this repository

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Make sure all CSV files are in the same directory as `app.py`:
   - diabetes_food_100.csv
   - diabetes_food_gdm_100_with_images.csv
   - diabetes_food_type2_100.csv

2. Run the application:
   ```bash
   streamlit run app.py
   ```

3. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Data Files

The application requires three CSV files with the following columns:
- Food Item
- Glycemic Index
- Calories
- Carbohydrates (g)
- Proteins (g)
- Fats (g)
- Fiber (g)
- Meal Type
- Diet Type

## Error Handling

The application includes:
- Data validation for CSV files
- Nutritional value range checking
- Error handling for missing data
- Image URL validation and caching

## Disclaimer

This meal planner is for informational purposes only. Always consult with healthcare professionals for personalized medical advice.
