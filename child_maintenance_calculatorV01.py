
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define the Calculation Function
def calculate_child_maintenance(father_income, mother_income, child_ages, age_weights, base_per_child, max_per_child):
    """
    Calculates child maintenance based on parent incomes, child ages, and adjustable parameters.

    Args:
        father_income (float): Father's monthly income.
        mother_income (float): Mother's monthly income.
        child_ages (list): List of child ages as integers.
        age_weights (dict): Custom age weights provided by the user.
        base_per_child (float): Base maintenance amount per child.
        max_per_child (float): Maximum maintenance amount per child.

    Returns:
        tuple: 
            - Minimum maintenance amount.
            - Maximum maintenance amount.
            - Total income of both parents.
            - Per-child maintenance amounts.
            - Lower percentage for maintenance calculation.
            - Higher percentage for maintenance calculation.
    """
    father_income = float(father_income) if father_income else 0.0
    mother_income = float(mother_income) if mother_income else 0.0
    total_income = father_income + mother_income

    low_percentage = 0.06
    high_percentage = 0.08
    low_total = total_income * low_percentage
    high_total = total_income * high_percentage

    # Ensure there is at least one child
    child_count = len(child_ages)
    if child_count == 0:
        raise ValueError("Please enter at least one child's age.")
    diminishing_factor = 0.95 ** (child_count - 1)

    # Minimum maintenance floor
    min_maintenance_floor = base_per_child - 50
    max_maintenance_floor = max_per_child - 50

    # Calculate maintenance per child
    per_child_maintenance = []
    for age in child_ages:
        weight = age_weights.get(str(age), 1.0)  # Default weight is 1.0 if age is not in age_weights
        low_amount = max(base_per_child * weight, low_total * diminishing_factor / child_count)
        high_amount = max(max_per_child * weight, high_total * diminishing_factor / child_count)
        low_amount = max(low_amount, min_maintenance_floor)
        high_amount = max(high_amount, max_maintenance_floor)
        per_child_maintenance.append((age, round(low_amount, 2), round(high_amount, 2)))

    min_maintenance = sum([x[1] for x in per_child_maintenance])
    max_maintenance = sum([x[2] for x in per_child_maintenance])

    return (
        round(min_maintenance, 2),
        round(max_maintenance, 2),
        total_income,
        per_child_maintenance,
        low_percentage,
        high_percentage,
    )


# Streamlit UI
st.title("Enhanced Child Maintenance Calculator")
st.sidebar.header("Input Parameters")

# Sidebar Inputs
father_income = st.sidebar.number_input(
    "Father's Monthly Income ($)",
    min_value=0.0,
    step=100.0,
    help="Enter the father's monthly income.",
)
mother_income = st.sidebar.number_input(
    "Mother's Monthly Income ($)",
    min_value=0.0,
    step=100.0,
    help="Enter the mother's monthly income.",
)
child_ages_input = st.sidebar.text_input(
    "Ages of Children (comma-separated)",
    help="Enter the ages of the children, separated by commas (e.g., 4, 8, 15).",
)

# Custom Age Weight Configurations
st.sidebar.subheader("Age Weighting (Optional)")
default_weights = {"0-5": 1.2, "6-12": 1.0, "13-18": 0.8, "19+": 0.6}
age_weights = {
    str(age): st.sidebar.number_input(
        f"Weight for Age {age}:", min_value=0.5, max_value=2.0, value=default_weights.get(f"{age}", 1.0), step=0.1
    )
    for age in range(1, 20)
}

# Parameterized Maintenance Values
st.sidebar.subheader("Maintenance Values")
base_per_child = st.sidebar.number_input(
    "Base Maintenance Amount per Child ($)",
    min_value=100.0,
    max_value=1000.0,
    value=350.0,
    step=50.0,
    help="Adjust the base maintenance amount per child.",
)
max_per_child = st.sidebar.number_input(
    "Maximum Maintenance Amount per Child ($)",
    min_value=200.0,
    max_value=1500.0,
    value=450.0,
    step=50.0,
    help="Adjust the maximum maintenance amount per child.",
)

try:
    child_ages = [
        int(age.strip()) for age in child_ages_input.split(",") if age.strip().isdigit()
    ]
    invalid_ages = [age for age in child_ages if age < 0]
    if invalid_ages:
        st.error(f"Invalid ages detected: {invalid_ages}. Please enter non-negative integers.")
        child_ages = []
except ValueError:
    st.error("Please enter valid child ages (integers only).")
    child_ages = []

if st.sidebar.button("Calculate"):
    if not child_ages:
        st.error("Please enter the ages of the children.")
    else:
        try:
            (
                min_maintenance,
                max_maintenance,
                total_income,
                per_child_maintenance,
                low_percentage,
                high_percentage,
            ) = calculate_child_maintenance(
                father_income, mother_income, child_ages, age_weights, base_per_child, max_per_child
            )

            # Display Results
            st.write(f"### Maintenance Range:")
            st.write(f"**Minimum Maintenance:** ${min_maintenance}")
            st.write(f"**Maximum Maintenance:** ${max_maintenance}")
            st.write(f"**Total Income:** ${total_income}")
            st.write(
                f"**Percentage Range for Maintenance:** {low_percentage * 100}% - {high_percentage * 100}%"
            )

            # Per-Child Maintenance Table
            df = pd.DataFrame(per_child_maintenance, columns=["Age", "Min Maintenance", "Max Maintenance"])
            st.write("### Per-Child Maintenance Breakdown:")
            st.dataframe(df)

            # Visualization
            st.write("### Maintenance Allocation Per Child:")
            fig, ax = plt.subplots()
            df.plot(kind="bar", x="Age", y=["Min Maintenance", "Max Maintenance"], ax=ax)
            plt.title("Maintenance Allocation by Age")
            plt.xlabel("Child Age")
            plt.ylabel("Maintenance Amount ($)")
            st.pyplot(fig)

            # Download Button
            download_data = f"""
            Minimum Maintenance: ${min_maintenance}
            Maximum Maintenance: ${max_maintenance}
            Total Income: ${total_income}
            Percentage Range for Maintenance: {low_percentage * 100}% - {high_percentage * 100}%
            """
            st.download_button(
                label="Download Results",
                data=download_data,
                file_name="child_maintenance_results.txt",
                mime="text/plain",
            )

            # Disclaimer
            st.write(
                """
                **Disclaimer:** 
                This tool is for informational purposes only and should not be considered legal or financial advice. 
                Child maintenance laws and regulations vary significantly by jurisdiction. 
                Please consult with a qualified legal or financial professional for guidance specific to your situation.
                """
            )
        except ValueError as e:
            st.error(f"Error: {e}")
