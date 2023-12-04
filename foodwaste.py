# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:54:13 2023

@author: HP
"""

import numpy as np
import pickle
import streamlit as st
from PIL import Image

# Load the trained model
model = pickle.load(open("trained_model2.sav", "rb"))

# Function to map categorical variables to numeric values
def map_categorical_to_numeric(user_input):
    # Example mappings (adjust based on how the model was trained)
    gender_map = {'Male': 0, 'Female': 1, 'Other': 2}
    age_map = {'18-25': 1, '26-35': 2, '36-45': 3, '46-55': 4, '56-65': 5, 'Older than 65': 6}
    education_map = {'No formal education': 0, 'Completed Primary Education': 1, 'Completed Secondary Education': 2, 'Completed Community College': 3, 'Completed Undergraduate': 4, 'Completed Postgraduate': 5}
    income_source_map = {'Farm work (own or others’ farm)': 0, 'Salaried employment': 1, 'Casual non-farm work': 2, 'Own enterprise': 3}
    income_map = {'Less than Ksh 10,000': 0, '10,001- 20,000': 1, '20,001- 30,000': 2, '30,001- 40,000': 3, 'More than 40,000': 4}
    lvap_map = {'Strongly disagree': 0, 'Disagree': 1, 'Neutral': 2, 'Agree': 3, 'Strongly agree': 4}

    # Apply mappings
    user_input[0] = gender_map[user_input[0]]
    user_input[1] = age_map[user_input[1]]
    user_input[2] = education_map[user_input[2]]
    user_input[3] = income_source_map[user_input[3]]
    user_input[4] = income_map[user_input[4]]
    user_input[6:] = [lvap_map[response] for response in user_input[6:]]  # Apply lvap_map to LVAP responses

    return user_input

def predict_package_selection(input_data):
    input_data = map_categorical_to_numeric(input_data)
    input_data_as_numpy_array = np.asarray(input_data, dtype=float)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = model.predict(input_data_reshaped)
    return "Package A" if prediction[0] == 0 else "Package B"

def main():
    st.title("🍏 Food Waste Prediction Web App 🌿")
    st.write("""
        The experiment aimed to capture the effect of sharing information about less visually appealing produce (LVAP) on the actual behavior of consumers, namely their selection of produce at the end of the experiment. Essentially, the app is able to run on already existing data, trying to make predictions of the selection based on knowledge and attitude perception. It can predict their selection of the package.
    """)

    # User Inputs
    st.write("### Demographic Questions")
    gender = st.radio("What is your Gender?", ('Male', 'Female'))
    age = st.selectbox("What is your age?", ['18-25', '26-35', '36-45', '46-55', '56-65', 'Older than 65'])
    education = st.selectbox("Highest level of education completed", ['No formal education', 'Completed Primary Education', 'Completed Secondary Education', 'Completed Community College', 'Completed Undergraduate', 'Completed Postgraduate'])
    income_source = st.selectbox("People earn money in different ways. In which of these ways do you get the majority of your money?", ['Farm work (own or others’ farm)', 'Salaried employment', 'Casual non-farm work', 'Own enterprise'])
    income = st.selectbox("How much was your income last month?", ['Less than Ksh 10,000', '10,001- 20,000', '20,001- 30,000', '30,001- 40,000', 'More than 40,000'])
    size_household = st.number_input("Including yourself, how many people have you lived with in your household in the past 6 months?", min_value=1, max_value=20)

    # LVAP Knowledge Questions
    st.write("### Level of Knowledge about LVAP")
    lvap_knowledge_responses = {
        "Fruits and vegetables that are smelly and slimy are still safe to consume": st.selectbox("Fruits and vegetables that are smelly and slimy are still safe to consume:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']),
        "Less visually appealing produce has the same nutritional value as good looking produce": st.selectbox("Less visually appealing produce has the same nutritional value as good looking produce:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']),
        "Less visually appealing produce tastes just as good as good looking produce": st.selectbox("Less visually appealing produce tastes just as good as good looking produce:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']),
        "Less visually appealing produce is not safe to consume": st.selectbox("Less visually appealing produce is not safe to consume:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']),
        "Less visually appealing produce cannot be repurposed to be used elsewhere": st.selectbox("Less visually appealing produce cannot be repurposed to be used elsewhere:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']),
        "Blemishes and scars on produce mean the produce cannot be consumed": st.selectbox("Blemishes and scars on produce mean the produce cannot be consumed:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']),
        "Throwing away less visually appealing produce has no effect on food waste in the markets and the environment": st.selectbox("Throwing away less visually appealing produce has no effect on food waste in the markets and the environment:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree'])
    }

    # LVAP Attitude Questions
    st.write("### What is your attitude towards LVAP?")
    lvap_attitude_responses = {
        "Unsold less visually appealing produce contributes to food waste in the markets": st.selectbox("Unsold less visually appealing produce contributes to food waste in the markets:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']),
        "I believe less visually appealing produce is just as valuable to my health": st.selectbox("I believe less visually appealing produce is just as valuable to my health:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']),
        "Only visually appealing fresh produce should be sold in markets": st.selectbox("Only visually appealing fresh produce should be sold in markets:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']),
        "I care about the amount of food wasted due to unsold less visually appealing produce": st.selectbox("I care about the amount of food wasted due to unsold less visually appealing produce:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']),
        "I am willing to enrich my knowledge on less visually appealing produce": st.selectbox("I am willing to enrich my knowledge on less visually appealing produce:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']),
        "I feel guilty whenever I exclude less visually appealing or funny looking produce when buying my groceries": st.selectbox("I feel guilty whenever I exclude less visually appealing or funny looking produce when buying my groceries:", ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree'])
    }

    if st.button("Predict Package Selection"):
        user_input = [gender, age, education, income_source, income, size_household]
        user_input.extend(lvap_knowledge_responses.values())
        user_input.extend(lvap_attitude_responses.values())
        prediction = predict_package_selection(user_input)
        st.write(f"The predicted package selection is: {prediction}")
        
        if prediction == "Package A (which is perfect produce)":
            image = Image.open("package_A.PNG")  # Adjust the path as needed
            st.image(image, caption='Package A')
        elif prediction == "Package B (which is LVAP)":
            image = Image.open("package_B.PNG")  # Adjust the path as needed
            st.image(image, caption='Package B')

if __name__ == "__main__":
    main()  
    
# CODE TO RUN ON THE TERMINAL
#streamlit run "C:\Users\HP\Downloads\busara_posner_ML\foodwaste.py"
