import streamlit as st

# Function for calculating child maintenance
def calculate_child_maintenance(father_income, mother_income, children_ages):
    father_income = father_income or 0
    mother_income = mother_income or 0

    # Validate input values
    if father_income < 0 or mother_income < 0:
        raise ValueError("Income values cannot be negative.")

    total_income = father_income + mother_income

    low_total = total_income * 0.06  # 6% of total income for all children
    high_total = total_income * 0.08  # 8% of total income for all children

    # Calculate per-child maintenance with age weights
    age_weights = [1.2 if age < 10 else 1.0 if age < 18 else 0.8 for age in children_ages]
    low_amounts = [(low_total * weight) / len(children_ages) for weight in age_weights]
    high_amounts = [(high_total * weight) / len(children_ages) for weight in age_weights]

    # Calculate total maintenance
    min_maintenance = sum(low_amounts)
    max_maintenance = sum(high_amounts)

    return round(min_maintenance, 2), round(max_maintenance, 2), total_income

# Streamlit UI
st.title("Child Maintenance Calculator")

st.sidebar.header("Input Parameters")
father_income = st.sidebar.number_input("Father's Monthly Income ($)", min_value=0.0, step=100.0, help="Enter the father's monthly income.")
mother_income = st.sidebar.number_input("Mother's Monthly Income ($)", min_value=0.0, step=100.0, help="Enter the mother's monthly income.")
num_children = st.sidebar.number_input("Number of Eligible Children", min_value=1, step=1, help="Enter the number of children eligible for maintenance.")

# Intuitive input for children's ages with validation
children_ages = []
st.sidebar.write("Enter the ages of each child:")
for i in range(int(num_children)):
    age = st.sidebar.number_input(f"Age of Child {i + 1}", min_value=0, max_value=21, step=1, help=f"Enter the age of child {i + 1}.")
    if age > 21:
        st.sidebar.warning(f"Child {i + 1}'s age exceeds the eligibility limit of 21 years. This child will be excluded.")
    else:
        children_ages.append(age)

if st.sidebar.button("Calculate"):
    try:
        if not children_ages:
            st.error("No eligible children provided. Please check the ages entered.")
        else:
            min_maintenance, max_maintenance, total_income = calculate_child_maintenance(
                father_income, mother_income, children_ages
            )

            st.write(f"### Monthly Maintenance Range:")
            st.write(f"**Minimum Monthly Maintenance:** ${min_maintenance}")
            st.write(f"**Maximum Monthly Maintenance:** ${max_maintenance}")
            st.write(f"**Total Income:** ${total_income}")
            
            st.markdown("**Disclaimer:** The calculated maintenance range is an estimate and should not be considered as legal or financial advice. Consult a professional for accurate guidance.")

            # Optional: Add a download button for results
            download_data = f"Minimum Monthly Maintenance: ${min_maintenance}\nMaximum Monthly Maintenance: ${max_maintenance}\nTotal Income: ${total_income}\nDisclaimer: The calculated maintenance range is an estimate and should not be considered as legal or financial advice. Consult a professional for accurate guidance."

            st.download_button(
                label="Download Results",
                data=download_data,
                file_name="child_maintenance_results.txt",
                mime="text/plain"
            )
    except ValueError as e:
        st.error(f"Input Error: {e}")

# Additional styling for the download button
st.markdown("""
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
""", unsafe_allow_html=True)
