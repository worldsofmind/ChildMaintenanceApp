import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Sample data for training (replace this with actual dataset)
data = {
    "Father's income (Processed)": [4000, 5000, 6000, 7000, 8000],
    "Mother's income (Processed)": [3000, 4000, 5000, 6000, 7000],
    "No. of children of the marriage": [1, 2, 3, 4, 2],
    "Weighted Child Age": [8.5, 10.2, 12.3, 14.5, 9.8],
    "Actual Maintenance": [600, 800, 1000, 1200, 900]
}
df = pd.DataFrame(data)

# Features and target
X = df[["Father's income (Processed)", "Mother's income (Processed)", "No. of children of the marriage", "Weighted Child Age"]]
y = df["Actual Maintenance"]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train the Gradient Boosting model
gb_model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)
gb_model.fit(X_train, y_train)

# Evaluate the model
y_pred = gb_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# Function for calculating child maintenance
def calculate_child_maintenance(father_income, mother_income, children_ages):
    if father_income < 0 or mother_income < 0:
        raise ValueError("Income values cannot be negative.")
    if not children_ages:
        raise ValueError("No valid children ages provided.")

    total_income = father_income + mother_income

    num_children = len(children_ages)
    weighted_child_age = np.mean([1.2 if age < 10 else 1.0 if age < 18 else 0.8 for age in children_ages])

    input_data = pd.DataFrame({
        "Father's income (Processed)": [father_income],
        "Mother's income (Processed)": [mother_income],
        "No. of children of the marriage": [num_children],
        "Weighted Child Age": [weighted_child_age]
    })

    input_data_scaled = scaler.transform(input_data)

    base_maintenance = gb_model.predict(input_data_scaled)[0]

    income_proportion = total_income * 0.1
    base_maintenance = max(100, min(base_maintenance, income_proportion))

    min_maintenance = base_maintenance * 0.75
    max_maintenance = base_maintenance * 1.25

    return round(min_maintenance), round(max_maintenance)

# Streamlit UI
st.title("Child Maintenance Calculator")

st.sidebar.header("Input Parameters")
father_income = st.sidebar.number_input("Father's Monthly Income ($)", min_value=0, step=100, format="%d", help="Enter the father's monthly income.")
mother_income = st.sidebar.number_input("Mother's Monthly Income ($)", min_value=0, step=100, format="%d", help="Enter the mother's monthly income.")
num_children = st.sidebar.number_input("Number of Eligible Children", min_value=1, step=1, help="Enter the number of children eligible for maintenance.")

st.sidebar.markdown("**Definition of Eligible Children:**")
st.sidebar.write("Eligible children include:")
st.sidebar.write("- Biological children")
st.sidebar.write("- Adopted children")
st.sidebar.write("- Non-biological children accepted as part of the family, such as stepchildren. Evidence of acceptance may include:")
st.sidebar.write("  - Changing the child’s surname")
st.sidebar.write("  - The child calling the non-parent 'dad' or 'mum'")
st.sidebar.write("  - Paying for the child’s expenses")

children_ages = []
st.sidebar.write("Enter the ages of each child:")
for i in range(int(num_children)):
    age = st.sidebar.number_input(f"Age of Child {i + 1}", min_value=0, max_value=21, step=1, help=f"Enter the age of child {i + 1}.")
    if age <= 21:
        children_ages.append(age)

if "results" not in st.session_state:
    st.session_state["results"] = None
if "feedback" not in st.session_state:
    st.session_state["feedback"] = None

if st.sidebar.button("Calculate"):
    try:
        valid_children_ages = [age for age in children_ages if age <= 21]

        if not valid_children_ages:
            st.error("No eligible children provided. Please check the ages entered.")
        else:
            min_maintenance, max_maintenance = calculate_child_maintenance(
                father_income, mother_income, valid_children_ages
            )
            st.session_state["results"] = {
                "min_maintenance": min_maintenance,
                "max_maintenance": max_maintenance
            }
            st.session_state["feedback"] = None
    except ValueError as e:
        st.error(f"Input Error: {e}")

if st.session_state["results"]:
    results = st.session_state["results"]
    st.write("### Predicted Maintenance Range:")
    st.write(f"**Minimum Monthly Maintenance (for all children combined):** ${results['min_maintenance']}")
    st.write(f"**Maximum Monthly Maintenance (for all children combined):** ${results['max_maintenance']}")

    st.markdown("**Disclaimer:** The predicted maintenance range is an estimate based on provided inputs and should not be considered as legal or financial advice. Consult a professional for accurate guidance.")

    st.write("### Is the Predicted Maintenance Acceptable?")

    feedback_reason = ""
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state["feedback"] == "👍":
            st.success("Thank you for your feedback! We're glad the prediction met your expectations.")
        elif st.button("👍 Yes", key="yes_button"):
            st.session_state["feedback"] = "👍"

    with col2:
        if st.session_state["feedback"] == "👎":
            st.warning("Thank you for your feedback! We'll use this to improve our predictions.")
        elif st.button("👎 No", key="no_button"):
            st.session_state["feedback"] = "👎"

    if st.session_state["feedback"] is not None:
        feedback_reason = st.text_area("Please share why you found the result acceptable or not:")

    if feedback_reason:
        st.write("Your feedback has been recorded and will be reviewed.")

# Add link to legal clinics
st.markdown("For legal advice, please visit the [List of Legal Clinics](https://example.com/legal-clinics).")

# Additional styling for the feedback buttons
st.markdown(
    """
    <style>
        .stButton > button {
            margin: 10px;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
