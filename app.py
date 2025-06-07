import streamlit as st
import pandas as pd

# Sample car dataset
data = [
    {"Brand": "Toyota", "Model": "Corolla", "Type": "Sedan", "Fuel": "Petrol", "Price": 20000},
    {"Brand": "Honda", "Model": "Civic", "Type": "Sedan", "Fuel": "Petrol", "Price": 22000},
    {"Brand": "Tesla", "Model": "Model 3", "Type": "Sedan", "Fuel": "Electric", "Price": 35000},
    {"Brand": "Ford", "Model": "F-150", "Type": "Truck", "Fuel": "Diesel", "Price": 30000},
    {"Brand": "Chevrolet", "Model": "Bolt", "Type": "Hatchback", "Fuel": "Electric", "Price": 32000},
    {"Brand": "Hyundai", "Model": "Tucson", "Type": "SUV", "Fuel": "Petrol", "Price": 27000},
    {"Brand": "Kia", "Model": "Sorento", "Type": "SUV", "Fuel": "Diesel", "Price": 29000},
]
df = pd.DataFrame(data)

st.title("🚗 Car Suggestion App")
st.write("Find the best car for you based on your preferences!")

# User inputs
budget = st.slider("Select your budget ($)", min_value=15000, max_value=40000, value=25000, step=1000)
car_type = st.selectbox("Select car type", ["Any"] + sorted(df["Type"].unique()))
fuel_type = st.selectbox("Select fuel type", ["Any"] + sorted(df["Fuel"].unique()))

# Filter logic
filtered = df[df["Price"] <= budget]
if car_type != "Any":
    filtered = filtered[filtered["Type"] == car_type]
if fuel_type != "Any":
    filtered = filtered[filtered["Fuel"] == fuel_type]

st.subheader("Suggested Cars:")
if not filtered.empty:
    for _, row in filtered.iterrows():
        st.markdown(f"**{row['Brand']} {row['Model']}**")
        st.write(f"Type: {row['Type']}, Fuel: {row['Fuel']}, Price: ${row['Price']}")
        st.markdown("---")
else:
    st.write("No cars match your preferences. Try adjusting your filters.") 