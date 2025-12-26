import streamlit as st
import pandas as pd

st.title("Discrepancy Checker")

uploaded_file = st.file_uploader(
    "## Upload a FVR",
    type=["xlsx"]
)

# 🔒 Main guard
if uploaded_file and uploaded_file.name.endswith(".xlsx"):
    excel_file = pd.ExcelFile(uploaded_file)

    selected_sheets = st.multiselect(
        "Select sheets to check discrepancy",
        options=excel_file.sheet_names,
        key="sheets_to_display"
    )

    # 🔒 Only when user selects sheets
    if selected_sheets:
        sheet_tables = {}

        for sheet in selected_sheets:
            sheet_tables[sheet] = pd.read_excel(
                uploaded_file,
                sheet_name=sheet
            )

        st.success("Selected sheets loaded successfully")


        st.subheader("⚖️ Overall Percentage Discrepancy Among Selected Sheets")

        base_sheet = selected_sheets[0]  # first sheet as base
        discrepancy_summary = {"Metric": [], "Compared Sheet": [], "Discrepancy (%)": []}

        metrics = ["Occupancy On Books This Year", "Booked Room Revenue This Year"]

        for metric in metrics:
          base_total = sheet_tables[base_sheet][metric].sum()
         
          for sheet_name in selected_sheets[1:]:
             comp_total = sheet_tables[sheet_name][metric].sum()
             perc_diff = ((comp_total - base_total) / base_total) * 100
            
            # <-- append must be here, inside the inner loop
             discrepancy_summary["Metric"].append(metric)
             discrepancy_summary["Compared Sheet"].append(sheet_name)
             discrepancy_summary["Discrepancy (%)"].append(round(perc_diff, 2))


# Convert to DataFrame for display
        discrepancy_df = pd.DataFrame(discrepancy_summary)
        st.dataframe(discrepancy_df, use_container_width=True)



        # -----------------------------
        # 📊 VIEW TABLES (OPTIONAL)
        # -----------------------------
        st.subheader("📊 View Selected Tables")

        sheet_to_view = st.selectbox(
            "Choose a sheet to view",
            options=selected_sheets
        )

        st.dataframe(
            sheet_tables[sheet_to_view],
            use_container_width=True
        )

        # =====================================================
        # 📈 GRAPH 1: OCCUPANCY ON BOOKS vs OCCUPANCY DATE
        # =====================================================
        st.subheader("📈 Occupancy On Books This Year vs Occupancy Date")

        occupancy_frames = []

        for sheet_name, df in sheet_tables.items():
            if {
                "Occupancy Date",
                "Occupancy On Books This Year"
            }.issubset(df.columns):

                temp = df[
                    ["Occupancy Date", "Occupancy On Books This Year"]
                ].copy()

                temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
                temp["Category"] = sheet_name

                occupancy_frames.append(temp)

        if occupancy_frames:
            occupancy_df = pd.concat(occupancy_frames)

            occupancy_pivot = occupancy_df.pivot_table(
            index="Occupancy Date",
                columns="Category",
                values="Occupancy On Books This Year",
                aggfunc="sum"  # or "mean" if you prefer
            ).sort_index()
            st.line_chart(occupancy_pivot, use_container_width=True)

        # =====================================================
        # 📉 GRAPH 2: REVENUE vs OCCUPANCY DATE
        # =====================================================
        st.subheader("📉 Booked Room Revenue This Year vs Occupancy Date")

        revenue_frames = []

        for sheet_name, df in sheet_tables.items():
            if {
                "Occupancy Date",
                "Booked Room Revenue This Year"
            }.issubset(df.columns):

                temp = df[
                    ["Occupancy Date", "Booked Room Revenue This Year"]
                ].copy()

                temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
                temp["Category"] = sheet_name

                revenue_frames.append(temp)

        if revenue_frames:
            revenue_df = pd.concat(revenue_frames)

            revenue_pivot = revenue_df.pivot_table(
                index="Occupancy Date",
                columns="Category",
                values="Booked Room Revenue This Year",
                aggfunc="sum"  # or "mean" if you prefer
            ).sort_index()

            st.line_chart(revenue_pivot, use_container_width=True)

else:
    st.info("Please upload a valid Excel file.")





# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.title("Discrepancy Checker")

# uploaded_file = st.file_uploader("## Upload a FVR", type=["xlsx"])

# if uploaded_file and uploaded_file.name.endswith(".xlsx"):
#     excel_file = pd.ExcelFile(uploaded_file)

#     selected_sheets = st.multiselect(
#         "Select sheets to check discrepancy",
#         options=excel_file.sheet_names,
#         key="sheets_to_display"
#     )

#     if selected_sheets:
#         sheet_tables = {}

#         for sheet in selected_sheets:
#             sheet_tables[sheet] = pd.read_excel(
#                 uploaded_file,
#                 sheet_name=sheet
#             )

#         st.success("Selected sheets loaded successfully")

#         # -------------------------
#         # Plot Occupancy
#         # -------------------------
#         occupancy_frames = []

#         for sheet_name, df in sheet_tables.items():
#             if {"Occupancy Date", "Occupancy On Books This Year"}.issubset(df.columns):
#                 temp = df[["Occupancy Date", "Occupancy On Books This Year"]].copy()
#                 temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#                 temp["Category"] = sheet_name
#                 occupancy_frames.append(temp)

#         if occupancy_frames:
#             occupancy_df = pd.concat(occupancy_frames)

#             fig_occ = px.line(
#                 occupancy_df,
#                 x="Occupancy Date",
#                 y="Occupancy On Books This Year",
#                 color="Category",
#                 title="Occupancy On Books This Year vs Occupancy Date"
#             )

#             st.plotly_chart(fig_occ, use_container_width=True)

#         # -------------------------
#         # Plot Revenue
#         # -------------------------
#         revenue_frames = []

#         for sheet_name, df in sheet_tables.items():
#             if {"Occupancy Date", "Booked Room Revenue This Year"}.issubset(df.columns):
#                 temp = df[["Occupancy Date", "Booked Room Revenue This Year"]].copy()
#                 temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#                 temp["Category"] = sheet_name
#                 revenue_frames.append(temp)

#         if revenue_frames:
#             revenue_df = pd.concat(revenue_frames)

#             fig_rev = px.line(
#                 revenue_df,
#                 x="Occupancy Date",
#                 y="Booked Room Revenue This Year",
#                 color="Category",
#                 title="Booked Room Revenue This Year vs Occupancy Date"
#             )

#             st.plotly_chart(fig_rev, use_container_width=True)

# else:
#     st.info("Please upload a valid Excel file.")




# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.title("Discrepancy Checker")

# uploaded_file = st.file_uploader("## Upload a FVR", type=["xlsx"])

# if uploaded_file and uploaded_file.name.endswith(".xlsx"):
#     excel_file = pd.ExcelFile(uploaded_file)

#     selected_sheets = st.multiselect(
#         "Select sheets to check discrepancy",
#         options=excel_file.sheet_names,
#         key="sheets_to_display"
#     )

#     if selected_sheets:
#         sheet_tables = {}

#         for sheet in selected_sheets:
#             sheet_tables[sheet] = pd.read_excel(
#                 uploaded_file,
#                 sheet_name=sheet
#             )

#         st.success("Selected sheets loaded successfully")

#         # -------------------------
#         # Optional Table View
#         # -------------------------
#         st.subheader("📊 View Selected Tables")
#         sheet_to_view = st.selectbox(
#             "Choose a sheet to view",
#             options=selected_sheets
#         )
#         st.dataframe(sheet_tables[sheet_to_view], use_container_width=True)

#         # -------------------------
#         # Line Chart: Occupancy
#         # -------------------------
#         st.subheader("📈 Occupancy On Books This Year vs Occupancy Date")

#         occupancy_frames = []

#         for sheet_name, df in sheet_tables.items():
#             if {"Occupancy Date", "Occupancy On Books This Year"}.issubset(df.columns):
#                 temp = df[["Occupancy Date", "Occupancy On Books This Year"]].copy()
#                 temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#                 temp["Category"] = sheet_name
#                 occupancy_frames.append(temp)

#         if occupancy_frames:
#             occupancy_df = pd.concat(occupancy_frames)
#             fig_occ = px.line(
#                 occupancy_df,
#                 x="Occupancy Date",
#                 y="Occupancy On Books This Year",
#                 color="Category",
#                 markers=False,   # classic smooth line
#                 title="Occupancy On Books This Year"
#             )
#             fig_occ.update_layout(legend_title_text="Sheet/Category")
#             st.plotly_chart(fig_occ, use_container_width=True)

#         # -------------------------
#         # Line Chart: Revenue
#         # -------------------------
#         st.subheader("📉 Booked Room Revenue This Year vs Occupancy Date")

#         revenue_frames = []

#         for sheet_name, df in sheet_tables.items():
#             if {"Occupancy Date", "Booked Room Revenue This Year"}.issubset(df.columns):
#                 temp = df[["Occupancy Date", "Booked Room Revenue This Year"]].copy()
#                 temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#                 temp["Category"] = sheet_name
#                 revenue_frames.append(temp)

#         if revenue_frames:
#             revenue_df = pd.concat(revenue_frames)
#             fig_rev = px.line(
#                 revenue_df,
#                 x="Occupancy Date",
#                 y="Booked Room Revenue This Year",
#                 color="Category",
#                 markers=False,   # smooth line
#                 title="Booked Room Revenue This Year"
#             )
#             fig_rev.update_layout(legend_title_text="Sheet/Category")
#             st.plotly_chart(fig_rev, use_container_width=True)

# else:
#     st.info("Please upload a valid Excel file.")
