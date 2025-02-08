import streamlit as st
import joblib
import pandas as pd

# User authentication
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username", "")
    password = st.sidebar.text_input("Password", "", type="password")
    if st.sidebar.button("Login"):
        if username == "admin" and password == "password":  # Simple authentication
            st.session_state["logged_in"] = True
        else:
            st.sidebar.error("Invalid username or password")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    # Load saved model
    model = joblib.load("D:\Solar Power Prediction\solar_power_model.pkl")

    # Feature names (from your dataset)
    features = [
        'temperature_2_m_above_gnd', 'relative_humidity_2_m_above_gnd',
        'mean_sea_level_pressure_MSL', 'total_precipitation_sfc',
        'snowfall_amount_sfc', 'total_cloud_cover_sfc',
        'high_cloud_cover_high_cld_lay', 'medium_cloud_cover_mid_cld_lay',
        'low_cloud_cover_low_cld_lay', 'shortwave_radiation_backwards_sfc',
        'wind_speed_10_m_above_gnd', 'wind_direction_10_m_above_gnd',
        'wind_speed_80_m_above_gnd', 'wind_direction_80_m_above_gnd',
        'wind_speed_900_mb', 'wind_direction_900_mb',
        'wind_gust_10_m_above_gnd', 'angle_of_incidence', 'zenith', 'azimuth'
    ]

    st.title('☀️ Solar Power Prediction')
    st.header('Input Parameters')

    # Create input widgets
    inputs = {}

    col1, col2 = st.columns(2)
    with col1:
        inputs['temperature_2_m_above_gnd'] = st.slider('Temperature (°C)', -10.0, 50.0, 25.0)
        inputs['relative_humidity_2_m_above_gnd'] = st.slider('Humidity (%)', 0, 100, 50)
        inputs['mean_sea_level_pressure_MSL'] = st.slider('Pressure (hPa)', 900.0, 1100.0, 1013.25)
        inputs['total_precipitation_sfc'] = st.slider('Precipitation (mm)', 0.0, 50.0, 0.0)
        inputs['snowfall_amount_sfc'] = st.slider('Snowfall (mm)', 0.0, 100.0, 0.0)
        inputs['total_cloud_cover_sfc'] = st.slider('Total Cloud Cover (%)', 0, 100, 50)
        inputs['high_cloud_cover_high_cld_lay'] = st.slider('High Cloud Cover (%)', 0, 100, 30)
        inputs['medium_cloud_cover_mid_cld_lay'] = st.slider('Medium Cloud Cover (%)', 0, 100, 40)
        inputs['low_cloud_cover_low_cld_lay'] = st.slider('Low Cloud Cover (%)', 0, 100, 50)

    with col2:
        inputs['shortwave_radiation_backwards_sfc'] = st.slider('Radiation (W/m²)', 0.0, 1500.0, 500.0)
        inputs['wind_speed_10_m_above_gnd'] = st.slider('Wind Speed 10m (m/s)', 0.0, 50.0, 5.0)
        inputs['wind_direction_10_m_above_gnd'] = st.slider('Wind Direction 10m (°)', 0, 360, 180)
        inputs['wind_speed_80_m_above_gnd'] = st.slider('Wind Speed 80m (m/s)', 0.0, 50.0, 5.0)
        inputs['wind_direction_80_m_above_gnd'] = st.slider('Wind Direction 80m (°)', 0, 360, 180)
        inputs['wind_speed_900_mb'] = st.slider('Wind Speed 900mb (m/s)', 0.0, 50.0, 5.0)
        inputs['wind_direction_900_mb'] = st.slider('Wind Direction 900mb (°)', 0, 360, 180)
        inputs['wind_gust_10_m_above_gnd'] = st.slider('Wind Gust 10m (m/s)', 0.0, 50.0, 10.0)
        inputs['angle_of_incidence'] = st.slider('Angle of Incidence (°)', 0, 90, 45)
        inputs['zenith'] = st.slider('Zenith Angle (°)', 0, 180, 90)
        inputs['azimuth'] = st.slider('Azimuth Angle (°)', 0, 360, 180)

    # Convert to DataFrame
    input_df = pd.DataFrame([[inputs[feature] for feature in features]], columns=features)

    # Make prediction
    if st.button('Predict'):
        prediction = model.predict(input_df)
        st.success(f'Predicted Power Generation: {prediction[0]:.2f} kW')
        
        # Show input summary
        st.subheader('Input Summary')
        st.write(input_df)
