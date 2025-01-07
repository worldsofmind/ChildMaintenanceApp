
import streamlit as st

# Function for calculating child maintenance
def calculate_child_maintenance(father_income, mother_income, num_children):
    father_income = father_income or 0
    mother_income = mother_income or 0

    total_income = father_income + mother_income
    low_percentage = 0.06
    high_percentage = 0.08

    base_per_child = 350
    max_per_child = 450

    low_total = total_income * low_percentage
    high_total = total_income * high_percentage

    # Diminishing returns for additional children
    diminishing_factor = 0.95 ** (num_children - 1)
    low_amount = max(base_per_child, low_total * diminishing_factor / num_children)
    high_amount = max(max_per_child, high_total * diminishing_factor / num_children)

    min_maintenance = low_amount * num_children
    max_maintenance = high_amount * num_children

    return round(min_maintenance, 2), round(max_maintenance, 2), total_income, low_percentage, high_percentage, base_per_child, max_per_child

# Streamlit UI
st.title("Child Maintenance Calculator")

st.sidebar.header("Input Parameters")
father_income = st.sidebar.number_input("Father's Monthly Income ($)", min_value=0.0, step=100.0, help="Enter the father's monthly income.")
mother_income = st.sidebar.number_input("Mother's Monthly Income ($)", min_value=0.0, step=100.0, help="Enter the mother's monthly income.")
num_children = st.sidebar.number_input("Number of Eligible Children", min_value=1, step=1, help="Enter the number of children eligible for maintenance.")

if st.sidebar.button("Calculate"):
    # No need for additional validation since number_input restricts input
    min_maintenance, max_maintenance, total_income, low_percentage, high_percentage, base_per_child, max_per_child = calculate_child_maintenance(father_income, mother_income, num_children)
    
    st.write(f"### Maintenance Range:")
    st.write(f"**Minimum Maintenance:** ${min_maintenance}")
    st.write(f"**Maximum Maintenance:** ${max_maintenance}")
    st.write(f"**Total Income:** ${total_income}")
    st.write(f"**Percentage Range for Maintenance:** {low_percentage * 100}% - {high_percentage * 100}%")
    st.write(f"**Base Maintenance per Child:** ${base_per_child} - ${max_per_child}")

    # Optional: Add a download button for results
    download_data = f"Minimum Maintenance: ${min_maintenance}\nMaximum Maintenance: ${max_maintenance}\nTotal Income: ${total_income}\nPercentage Range for Maintenance: {low_percentage * 100}% - {high_percentage * 100}%"
    
    st.download_button(
        label="Download Results",
        data=download_data,
        file_name="child_maintenance_results.txt",
        mime="text/plain"
    )

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
