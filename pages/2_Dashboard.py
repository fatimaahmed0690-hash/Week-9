# pages/2_Dashboard.py
import streamlit as st
from database_manager import DatabaseManager
import pandas as pd
import matplotlib.pyplot as plt

db = DatabaseManager(user="week9user", password="MyPassword123", database="week9_db")

def _sidebar_filters(df):
    st.sidebar.header("Filters")
    categories = ["All"] + sorted(df['category'].dropna().unique().tolist())
    severities = ["All"] + sorted(df['severity'].dropna().unique().tolist())
    statuses = ["All"] + sorted(df['status'].dropna().unique().tolist())
    sel_cat = st.sidebar.selectbox("Category", categories)
    sel_sev = st.sidebar.selectbox("Severity", severities)
    sel_status = st.sidebar.selectbox("Status", statuses)
    return sel_cat, sel_sev, sel_status

def dashboard_page():
    st.title("Cybersecurity Dashboard (Week 9)")

    df = pd.read_sql("SELECT * FROM cyber_incidents", con=db.conn)
    if df.empty:
        st.warning("No incidents in database.")
    else:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    sel_cat, sel_sev, sel_status = _sidebar_filters(df if not df.empty else pd.DataFrame(columns=['category','severity','status']))

    filtered = df.copy()
    if sel_cat != "All":
        filtered = filtered[filtered['category'] == sel_cat]
    if sel_sev != "All":
        filtered = filtered[filtered['severity'] == sel_sev]
    if sel_status != "All":
        filtered = filtered[filtered['status'] == sel_status]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Incidents", len(filtered))
    col2.metric("Open Incidents", int((filtered['status'] == "Open").sum()) if not filtered.empty else 0)
    col3.metric("Avg Resolution (hrs)", round(filtered['resolution_time_hours'].dropna().mean() or 0, 2) if not filtered.empty else 0)

    st.subheader("Incident Records")
    st.dataframe(filtered.sort_values(by="date", ascending=False).reset_index(drop=True))

    with st.expander("Add New Incident"):
        with st.form("add_incident_form"):
            incident_id = st.text_input("Incident ID (unique)")
            date = st.date_input("Date")
            category = st.text_input("Category", value="Phishing")
            subcategory = st.text_input("Subcategory", value="")
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
            assigned_to = st.text_input("Assigned To")
            resolution_time_hours = st.number_input("Resolution time (hrs)", min_value=0.0, step=0.1)
            description = st.text_area("Description")
            submitted = st.form_submit_button("Add Incident")
            if submitted:
                incident = {
                    "incident_id": incident_id or f"INC-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}",
                    "date": date.isoformat(),
                    "category": category,
                    "subcategory": subcategory,
                    "severity": severity,
                    "status": status,
                    "assigned_to": assigned_to,
                    "resolution_time_hours": resolution_time_hours,
                    "description": description
                }
                try:
                    db.insert_incident(incident)
                    st.success("Incident added successfully.")
                    st.experimental_rerun()
                except:
                    st.error("Error: Incident ID already exists.")

    st.markdown("---")
    st.subheader("Edit / Delete Incident")
    all_incidents = db.get_all_incidents()
    if all_incidents:
        choices = {f"{r['id']} - {r['incident_id']} - {r['category']} - {r['status']}": r['id'] for r in all_incidents}
        sel = st.selectbox("Select incident to edit", list(choices.keys()))
        inc_id = choices[sel]
        inc = db.get_incident_by_id(inc_id)
        if inc:
            with st.form("edit_incident_form"):
                ed_incident_id = st.text_input("Incident ID", value=inc["incident_id"])
                ed_date = st.date_input("Date", value=pd.to_datetime(inc["date"]).date() if inc["date"] else None)
                ed_category = st.text_input("Category", value=inc["category"])
                ed_subcategory = st.text_input("Subcategory", value=inc["subcategory"])
                ed_severity = st.selectbox("Severity", ["Low","Medium","High","Critical"], index=["Low","Medium","High","Critical"].index(inc["severity"]) if inc["severity"] in ["Low","Medium","High","Critical"] else 0)
                ed_status = st.selectbox("Status", ["Open","In Progress","Resolved"], index=["Open","In Progress","Resolved"].index(inc["status"]) if inc["status"] in ["Open","In Progress","Resolved"] else 0)
                ed_assigned = st.text_input("Assigned To", value=inc["assigned_to"])
                ed_resolution = st.number_input("Resolution time (hours)", value=float(inc["resolution_time_hours"] or 0.0))
                ed_description = st.text_area("Description", value=inc["description"])
                btn_update = st.form_submit_button("Update")
                btn_delete = st.form_submit_button("Delete")
                if btn_update:
                    db.update_incident(inc_id, {
                        "incident_id": ed_incident_id,
                        "date": ed_date.isoformat(),
                        "category": ed_category,
                        "subcategory": ed_subcategory,
                        "severity": ed_severity,
                        "status": ed_status,
                        "assigned_to": ed_assigned,
                        "resolution_time_hours": ed_resolution,
                        "description": ed_description
                    })
                    st.success("Updated successfully.")
                    st.experimental_rerun()
                if btn_delete:
                    db.delete_incident(inc_id)
                    st.success("Deleted successfully.")
                    st.experimental_rerun()
    else:
        st.info("No incidents to edit or delete.")

    st.markdown("---")
    st.subheader("Visualizations with Matplotlib")

    viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Trend", "Severity Distribution", "Assigned Staff"])

    with viz_tab1:
        st.write("Incidents over time")
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            time_df = df.groupby(pd.Grouper(key='date', freq='W')).size().reset_index(name='count')
            fig, ax = plt.subplots()
            ax.plot(time_df['date'].to_numpy(), time_df['count'].to_numpy(), marker='o', color='blue')
            ax.set_xlabel("Week")
            ax.set_ylabel("Number of Incidents")
            ax.set_title("Incidents per Week")
            ax.grid(True)
            st.pyplot(fig)

        else:
            st.info("No data to display.")

    with viz_tab2:
        st.write("Severity distribution")
        if not filtered.empty:
            sev = filtered['severity'].value_counts()
            fig, ax = plt.subplots()
            ax.bar(sev.index, sev.values, color=['green','yellow','orange','red'])
            ax.set_xlabel("Severity")
            ax.set_ylabel("Number of Incidents")
            ax.set_title("Severity Distribution")
            st.pyplot(fig)
        else:
            st.info("No data to display.")

    with viz_tab3:
        st.write("Incidents per Staff")
        if not filtered.empty:
            staff = filtered['assigned_to'].fillna("Unassigned").value_counts()
            fig, ax = plt.subplots()
            ax.bar(staff.index, staff.values, color='skyblue')
            ax.set_xlabel("Staff")
            ax.set_ylabel("Number of Incidents")
            ax.set_title("Incidents Assigned")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.info("No data to display.")


if __name__ == "__main__":
    dashboard_page()
