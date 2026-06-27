import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Doctor Product Portfolio Dashboard",
    layout="wide"
)

st.title("🩺 Doctor Product Portfolio Dashboard")
st.write("Welcome to my Internship Project")

# Database Connection
conn = sqlite3.connect("doctor.db", check_same_thread=False)
cursor = conn.cursor()

# Sidebar
page = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Doctors", "Products", "Assignments"]
)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.header("📊 Dashboard")

    doctor_count = cursor.execute(
        "SELECT COUNT(*) FROM doctors"
    ).fetchone()[0]

    product_count = cursor.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    assignment_count = cursor.execute(
        "SELECT COUNT(*) FROM doctor_products"
    ).fetchone()[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👨‍⚕️ Doctors", doctor_count)

    with col2:
        st.metric("💊 Products", product_count)

    with col3:
        st.metric("🔗 Assignments", assignment_count)

    st.divider()

    st.subheader("Doctor - Product Mapping")

    dashboard = pd.read_sql(
        """
        SELECT
            d.doctor_name,
            p.product_name
        FROM doctor_products dp
        LEFT JOIN doctors d
            ON dp.doctor_id = d.id
        LEFT JOIN products p
            ON dp.product_id = p.id
        """,
        conn
    )

    st.dataframe(
        dashboard,
        use_container_width=True
    )

# ---------------- DOCTORS ----------------
elif page == "Doctors":

    st.header("👨‍⚕️ Doctor Management")

    tab1, tab2 = st.tabs(["➕ Add Doctor", "📋 View Doctors"])

    # ---------------- ADD DOCTOR ----------------

    with tab1:

        doctor_name = st.text_input("Doctor Name")
        hospital_name = st.text_input("Hospital Name")
        specialty = st.text_input("Specialty")
        whatsapp = st.text_input("WhatsApp Number")

        if st.button("Add Doctor"):

            if doctor_name == "":
                st.warning("Doctor name is required!")

            else:

                cursor.execute(
                    """
                    INSERT INTO doctors
                    (doctor_name,hospital_name,specialty,whatsapp_number)
                    VALUES(?,?,?,?)
                    """,
                    (
                        doctor_name,
                        hospital_name,
                        specialty,
                        whatsapp
                    )
                )

                conn.commit()

                st.success("Doctor Added Successfully!")

                st.rerun()

    # ---------------- VIEW DOCTORS ----------------

    with tab2:

        search = st.text_input("🔍 Search Doctor")

        doctors = pd.read_sql(
            "SELECT * FROM doctors",
            conn
        )

        if search:
            doctors = doctors[
                doctors["doctor_name"].str.contains(search, case=False, na=False)
            ]

        st.dataframe(
            doctors,
            use_container_width=True
        )

        st.subheader("🗑 Delete Doctor")

        doctor_list = pd.read_sql(
            "SELECT id, doctor_name FROM doctors",
            conn
        )

        if not doctor_list.empty:

            delete_doctor = st.selectbox(
                "Select Doctor",
                doctor_list["doctor_name"],
                key="delete_doctor"
            )

            if st.button("Delete Doctor"):

                doctor_id = int(
                    doctor_list.loc[
                        doctor_list["doctor_name"] == delete_doctor,
                        "id"
                    ].values[0]
                )

                cursor.execute(
                    "DELETE FROM doctors WHERE id=?",
                    (doctor_id,)
                )

                cursor.execute(
                    "DELETE FROM doctor_products WHERE doctor_id=?",
                    (doctor_id,)
                )

                conn.commit()

                st.success("Doctor Deleted Successfully!")

                st.rerun()

# ---------------- PRODUCTS ----------------
elif page == "Products":

    st.header("💊 Product Management")

    tab1, tab2 = st.tabs(["➕ Add Product", "📋 View Products"])

    # -------- Add Product --------

    with tab1:

        product_name = st.text_input("Product Name")
        company_name = st.text_input("Company Name")
        molecule = st.text_input("Molecule")
        specialty = st.text_input("Specialty")
        description = st.text_area("Description")

        if st.button("Add Product"):

            if product_name == "":
                st.warning("Product Name is required!")

            else:

                cursor.execute(
                    """
                    INSERT INTO products
                    (product_name, company_name, molecule, specialty, description)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        product_name,
                        company_name,
                        molecule,
                        specialty,
                        description
                    )
                )

                conn.commit()

                st.success("Product Added Successfully!")

                st.rerun()

    # -------- View Product --------

    with tab2:

        search_product = st.text_input("🔍 Search Product")

        products = pd.read_sql(
            "SELECT * FROM products",
            conn
        )

        if search_product:
            products = products[
                products["product_name"].str.contains(
                    search_product,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            products,
            use_container_width=True
        )

        st.subheader("🗑 Delete Product")

        product_list = pd.read_sql(
            "SELECT id, product_name FROM products",
            conn
        )

        if not product_list.empty:

            delete_product = st.selectbox(
                "Select Product",
                product_list["product_name"],
                key="delete_product"
            )

            if st.button("Delete Product"):

                product_id = int(
                    product_list.loc[
                        product_list["product_name"] == delete_product,
                        "id"
                    ].values[0]
                )

                cursor.execute(
                    "DELETE FROM products WHERE id=?",
                    (product_id,)
                )

                cursor.execute(
                    "DELETE FROM doctor_products WHERE product_id=?",
                    (product_id,)
                )

                conn.commit()

                st.success("Product Deleted Successfully!")

                st.rerun()
# ---------------- ASSIGNMENTS ----------------
elif page == "Assignments":

    st.header("🔗 Assign Products to Doctor")

    # Get doctors
    doctors = pd.read_sql(
        "SELECT id, doctor_name FROM doctors",
        conn
    )

    # Get products
    products = pd.read_sql(
        "SELECT id, product_name FROM products",
        conn
    )

    if doctors.empty:
        st.warning("Please add at least one doctor.")
    elif products.empty:
        st.warning("Please add at least one product.")
    else:

        doctor = st.selectbox(
            "Select Doctor",
            doctors["doctor_name"]
        )

        product = st.selectbox(
            "Select Product",
            products["product_name"]
        )

        if st.button("Assign Product"):

            doctor_id = int(doctors.loc[
                doctors["doctor_name"] == doctor,
                "id"
            ].values[0])

            product_id = int(products.loc[
                products["product_name"] == product,
                "id"
            ].values[0])

            cursor.execute(
                """
                INSERT INTO doctor_products
                (doctor_id, product_id)
                VALUES (?, ?)
                """,
                (doctor_id, product_id)
            )

            conn.commit()

            st.success("Product Assigned Successfully!")

        st.subheader("Assigned Products")

        assigned = pd.read_sql(
            """
            SELECT
                dp.id,
                d.doctor_name,
                p.product_name
            FROM doctor_products dp
            LEFT JOIN doctors d
                ON dp.doctor_id = d.id
            LEFT JOIN products p
                ON dp.product_id = p.id
            ORDER BY dp.id DESC
            """,
            conn
        )

        st.dataframe(
            assigned,
            use_container_width=True
        )