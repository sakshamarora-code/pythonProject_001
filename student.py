import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Student Management System",
    layout="wide"
)

FILE = "students.csv"

# -------------------- DATA HANDLING --------------------
def load_data():
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=[
            "sl", "name", "class", "batch",
            "admit_date", "mobile", "parent_mobile"
        ])
        df.to_csv(FILE, index=False)
    return pd.read_csv(FILE)

def save_data(df):
    df.to_csv(FILE, index=False)

df = load_data()

# -------------------- UI HEADER --------------------
st.title("🎓 Student Management System")
st.caption("CSV-based UI application using Python & Streamlit")

# -------------------- ADD STUDENT (APPEND ONLY) --------------------
st.subheader("➕ Add Student")

with st.form("student_form"):
    c1, c2, c3 = st.columns(3)

    sl = c1.number_input("Serial No", min_value=1, step=1)
    name = c2.text_input("Student Name")
    class_ = c3.selectbox("Class", [f"Class {i}" for i in range(1, 11)])

    batch = c1.text_input("Batch")
    admit_date = c2.text_input("Admit Date")
    mobile = c3.text_input("Mobile")
    parent_mobile = c1.text_input("Parent Mobile")

    submit = st.form_submit_button("Add Student")

    if submit:
        if name.strip() == "":
            st.error("Student name is required")
        elif sl in df["sl"].values:
            st.error("Serial number already exists. Records cannot be updated.")
        else:
            new_row = pd.DataFrame([{
                "sl": sl,
                "name": name,
                "class": class_,
                "batch": batch,
                "admit_date": admit_date,
                "mobile": mobile,
                "parent_mobile": parent_mobile
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("Student record added successfully")

# -------------------- FILTER & SORT --------------------
st.subheader("🔍 Filter & Sort")

f1, f2, f3 = st.columns(3)

filter_class = f1.selectbox(
    "Filter by Class",
    ["All"] + sorted(df["class"].dropna().unique().tolist())
)

sort_by = f2.selectbox("Sort By", ["sl", "name", "class"])
sort_order = f3.radio("Order", ["Ascending", "Descending"])

filtered_df = df.copy()

if filter_class != "All":
    filtered_df = filtered_df[filtered_df["class"] == filter_class]

filtered_df = filtered_df.sort_values(
    by=sort_by,
    ascending=(sort_order == "Ascending")
)

# -------------------- DISPLAY TABLE --------------------
st.subheader("📋 Student Records")
st.dataframe(filtered_df, width="stretch")

# -------------------- CSV DOWNLOAD --------------------
st.subheader("⬇️ Download Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="students_export.csv",
    mime="text/csv"
)

# -------------------- DELETE --------------------
st.subheader("🗑️ Delete Student")

del_sl = st.number_input("Enter Serial No to Delete", min_value=1, step=1)

if st.button("Delete Record"):
    if del_sl not in df["sl"].values:
        st.error("Serial number not found")
    else:
        df = df[df["sl"] != del_sl]
        save_data(df)
        st.warning("Student record deleted")

# -------------------- CHARTS --------------------
st.subheader("📊 Analytics")

chart_col1, chart_col2 = st.columns(2)

class_counts = df["class"].value_counts()

with chart_col1:
    st.markdown("**Students per Class (Bar Chart)**")
    st.bar_chart(class_counts)

with chart_col2:
    st.markdown("**Class Distribution (Pie Chart)**")
    fig, ax = plt.subplots()
    ax.pie(
        class_counts.values,
        labels=class_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)
