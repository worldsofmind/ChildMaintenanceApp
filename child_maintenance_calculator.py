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

# Train the Gradient Boosting model with hyperparameter tuning
gb_model = GradientBoostingRegressor(
    n_estimators=300,  # Increase the number of trees
    learning_rate=0.05,  # Reduce learning rate for smoother convergence
    max_depth=5,  # Increase depth for better capturing relationships
    subsample=0.8,  # Use a fraction of the data for training each tree
    min_samples_split=10,  # Minimum samples required to split a node
    min_samples_leaf=5,  # Minimum samples in leaf nodes
    random_state=42
)
gb_model.fit(X_train, y_train)

# Evaluate the model
y_pred = gb_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# Function for calculating child maintenance using Gradient Boosting
def calculate_child_maintenance(father_income, mother_income, children_ages):
    if father_income < 0 or mother_income < 0:
        raise ValueError("Income values cannot be negative.")
    if not children_ages:
        raise ValueError("No valid children ages provided.")

    total_income = father_income + mother_income

    # Feature engineering
    num_children = len(children_ages)
    weighted_child_age = np.mean([1.2 if age < 10 else 1.0 if age < 18 else 0.8 for age in children_ages])

    # Prepare input for prediction
    input_data = pd.DataFrame({
        "Father's income (Processed)": [father_income],
        "Mother's income (Processed)": [mother_income],
        "No. of children of the marriage": [num_children],
        "Weighted Child Age": [weighted_child_age]
    })

    # Normalize inputs using scaler
    input_data_scaled = scaler.transform(input_data)

    # Predict maintenance using Gradient Boosting
    base_maintenance = gb_model.predict(input_data_scaled)[0]

    # Apply scaling and limits to predictions
    base_maintenance = max(100, min(base_maintenance, 1000))  # Limit predictions to realistic range
    min_maintenance = base_maintenance * 0.9
    max_maintenance = base_maintenance * 1.1

    return round(min_maintenance), round(max_maintenance), round(total_income)

# Streamlit UI
st.title("Child Maintenance Calculator")

st.sidebar.header("Input Parameters")
father_income = st.sidebar.number_input("Father's Monthly Income ($)", min_value=0, step=100, format="%d", help="Enter the father's monthly income.")
mother_income = st.sidebar.number_input("Mother's Monthly Income ($)", min_value=0, step=100, format="%d", help="Enter the mother's monthly income.")
num_children = st.sidebar.number_input("Number of Eligible Children", min_value=1, step=1, help="Enter the number of children eligible for maintenance.")

# Intuitive input for children's ages with validation
children_ages = []
st.sidebar.write("Enter the ages of each child:")
for i in range(int(num_children)):
    age = st.sidebar.number_input(f"Age of Child {i + 1}", min_value=0, max_value=21, step=1, help=f"Enter the age of child {i + 1}.")
    if age <= 21:  # Only include eligible children
        children_ages.append(age)

if st.sidebar.button("Calculate"):
    try:
        # Exclude ineligible ages
        valid_children_ages = [age for age in children_ages if age <= 21]

        if not valid_children_ages:
            st.error("No eligible children provided. Please check the ages entered.")
        else:
            min_maintenance, max_maintenance, total_income = calculate_child_maintenance(
                father_income, mother_income, valid_children_ages
            )

            st.write("### Predicted Maintenance Range:")
            st.write(f"**Minimum Monthly Maintenance:** ${min_maintenance}")
            st.write(f"**Maximum Monthly Maintenance:** ${max_maintenance}")
            st.write(f"**Total Income:** ${total_income}")

            st.markdown("**Disclaimer:** The predicted maintenance range is an estimate based on provided inputs and should not be considered as legal or financial advice. Consult a professional for accurate guidance.")

            # Add a download button for results
            download_data = f"Minimum Monthly Maintenance: ${min_maintenance}\nMaximum Monthly Maintenance: ${max_maintenance}\nTotal Income: ${total_income}\nDisclaimer: The predicted maintenance range is an estimate based on provided inputs and should not be considered as legal or financial advice. Consult a professional for accurate guidance."

            st.download_button(
                label="Download Results",
                data=download_data,
                file_name="child_maintenance_results.txt",
                mime="text/plain"
            )
    except ValueError as e:
        st.error(f"Input Error: {e}")

# Additional styling for the download button
st.markdown(
    """
    <style>
        .stDownloadButton > button {
            background-color: #4CAF50; /* Green */
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

