### Import Libraries
```python
import streamlit as st
```
- **Purpose**: Imports the Streamlit library to build an interactive web application.

---

### Define the Calculation Function
```python
def calculate_child_maintenance(father_income, mother_income, num_children):
```
- **Purpose**: Defines a function to calculate the child maintenance amount based on parental income and the number of children.

```python
    father_income = father_income or 0
    mother_income = mother_income or 0
```
- **Purpose**: Ensures that income values are treated as `0` if no input is provided (handling missing values).

```python
    total_income = father_income + mother_income
    low_percentage = 0.06
    high_percentage = 0.08
```
- **Purpose**: Calculates the total combined income of the parents and sets the percentage range (6%–8%) for maintenance allocation.

```python
    base_per_child = 350
    max_per_child = 450
```
- **Purpose**: Defines the minimum and maximum base maintenance amount per child.

```python
    low_total = total_income * low_percentage
    high_total = total_income * high_percentage
```
- **Purpose**: Calculates the total maintenance allocation for the family based on the percentage range.

```python
    diminishing_factor = 0.95 ** (num_children - 1)
    low_amount = max(base_per_child, low_total * diminishing_factor / num_children)
    high_amount = max(max_per_child, high_total * diminishing_factor / num_children)
```
- **Purpose**: Applies a diminishing factor for additional children (e.g., second, third child receives slightly less) and calculates per-child maintenance within the base range.

```python
    min_maintenance = low_amount * num_children
    max_maintenance = high_amount * num_children
```
- **Purpose**: Computes the total minimum and maximum maintenance amounts for all eligible children.

```python
    return round(min_maintenance, 2), round(max_maintenance, 2), total_income, low_percentage, high_percentage, base_per_child, max_per_child
```
- **Purpose**: Returns the calculated maintenance range along with other relevant details for display.

---

### Streamlit UI - Title and Sidebar Input
```python
st.title("Child Maintenance Calculator")
```
- **Purpose**: Displays the app title at the top of the page.

```python
st.sidebar.header("Input Parameters")
```
- **Purpose**: Adds a header in the sidebar for input fields.

```python
father_income = st.sidebar.number_input("Father's Monthly Income ($)", min_value=0.0, step=100.0, help="Enter the father's monthly income.")
```
- **Purpose**: Provides an input field in the sidebar for the father's income, with a minimum value of $0 and step increments of $100.

```python
mother_income = st.sidebar.number_input("Mother's Monthly Income ($)", min_value=0.0, step=100.0, help="Enter the mother's monthly income.")
```
- **Purpose**: Provides an input field in the sidebar for the mother's income, similar to the father's income.

```python
num_children = st.sidebar.number_input("Number of Eligible Children", min_value=1, step=1, help="Enter the number of children eligible for maintenance.")
```
- **Purpose**: Provides an input field for the number of eligible children, with a minimum value of 1 and step increments of 1.

---

### Calculation and Output Display
```python
if st.sidebar.button("Calculate"):
```
- **Purpose**: Adds a "Calculate" button in the sidebar. When clicked, the script triggers the calculation and displays the results.

```python
    min_maintenance, max_maintenance, total_income, low_percentage, high_percentage, base_per_child, max_per_child = calculate_child_maintenance(father_income, mother_income, num_children)
```
- **Purpose**: Calls the calculation function with user-provided inputs and stores the returned values.

```python
    st.write(f"### Maintenance Range:")
```
- **Purpose**: Adds a subheading to display the maintenance range.

```python
    st.write(f"**Minimum Maintenance:** ${min_maintenance}")
    st.write(f"**Maximum Maintenance:** ${max_maintenance}")
```
- **Purpose**: Displays the calculated minimum and maximum maintenance amounts.

```python
    st.write(f"**Total Income:** ${total_income}")
    st.write(f"**Percentage Range for Maintenance:** {low_percentage * 100}% - {high_percentage * 100}%")
    st.write(f"**Base Maintenance per Child:** ${base_per_child} - ${max_per_child}")
```
- **Purpose**: Displays additional details about the calculation, such as total income and maintenance percentages.

---

### Add Download Button for Results
```python
    download_data = f"Minimum Maintenance: ${min_maintenance}\\nMaximum Maintenance: ${max_maintenance}\\nTotal Income: ${total_income}\\nPercentage Range for Maintenance: {low_percentage * 100}% - {high_percentage * 100}%"
```
- **Purpose**: Prepares the calculation results as a downloadable text file.

```python
    st.download_button(
        label="Download Results",
        data=download_data,
        file_name="child_maintenance_results.txt",
        mime="text/plain"
    )
```
- **Purpose**: Adds a download button that allows users to save the calculation results as a `.txt` file.

---

### Styling
```python
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
```
- **Purpose**: Adds custom CSS styling to enhance the appearance of the download button (green background, rounded corners, etc.).

---
