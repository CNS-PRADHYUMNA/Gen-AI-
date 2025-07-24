import streamlit as st
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf

# Load model and encoders
model = tf.keras.models.load_model('ann_model.h5')
label_encoder = joblib.load('label_encoder.pkl')
one_hot_encoder = joblib.load('one_hot_encoder.pkl')
scaler = joblib.load('scaler.pkl')

# Title
st.set_page_config(page_title="Churn Prediction", layout="centered")
st.title("🔍 Bank Customer Churn Prediction")
st.markdown("Enter customer details below to predict if they are likely to **exit** the bank.")

# Input form
with st.form("churn_form"):
    col1, col2 = st.columns(2)

    with col1:
        credit_score = st.number_input("Credit Score", min_value=300, max_value=900, value=600)
        geography = st.selectbox("Geography", options=['France', 'Germany', 'Spain'])
        age = st.number_input("Age", min_value=18, max_value=100, value=40)
        tenure = st.slider("Tenure", min_value=0, max_value=10, value=5)
        balance = st.number_input("Balance", min_value=0.0, max_value=300000.0, value=50000.0)

    with col2:
        gender = st.selectbox("Gender", options=["Male", "Female"])
        num_products = st.selectbox("Number of Products", options=[1, 2, 3, 4])
        has_cr_card = st.selectbox("Has Credit Card?", options=[0, 1])
        is_active_member = st.selectbox("Is Active Member?", options=[0, 1])
        estimated_salary = st.number_input("Estimated Salary", min_value=0.0, max_value=200000.0, value=50000.0)

    submitted = st.form_submit_button("Predict")

# Prediction logic
if submitted:
    # Build input DataFrame
    input_data = pd.DataFrame([{
        'CreditScore': credit_score,
        'Geography': geography,
        'Gender': gender,
        'Age': age,
        'Tenure': tenure,
        'Balance': balance,
        'NumOfProducts': num_products,
        'HasCrCard': has_cr_card,
        'IsActiveMember': is_active_member,
        'EstimatedSalary': estimated_salary
    }])

    # Transform gender
    input_data['Gender'] = label_encoder.transform(input_data['Gender'])

    # Transform geography
    geo_encoded = one_hot_encoder.transform(input_data[['Geography']]).toarray()
    geo_df = pd.DataFrame(geo_encoded, columns=one_hot_encoder.get_feature_names_out(['Geography']))
    input_data = pd.concat([input_data.drop(['Geography'], axis=1).reset_index(drop=True), geo_df], axis=1)

    # Scale features
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)
    prob = prediction[0][0]
    result = "🚪 Exited" if prob > 0.5 else "✅ Not Exited"

    # Display result
    st.markdown("### 📊 Prediction Result")
    st.success(f"**{result}** with probability of `{prob:.2f}`")
