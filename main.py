import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")


st.title("Phonepe Data Visualization and Exploration")
st.text('This is a web app allow exploration of Phonepe Data')

st.sidebar.title("Navigation")
side_bar_object = st.sidebar.radio("Pages", options=["About", "Aggregated Data", "District Data", "Geography Data"])

if side_bar_object == "About":
    st.subheader("About:")
    st.markdown("Fintech, Data visualization and exploration with Plotly library and built interactive dashboard using "
             "Streamlit.  \n🌟 Data upto  Q2(April, May, June) of 2023 has been added.")

# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------Aggregated Data Page --------------------------------------------------

if side_bar_object == "Aggregated Data":
    tab1, tab2 = st.tabs(["Transaction Data", "User Data"])

    # ------------------------------------------------------tab1----------------------------------------------

    with tab1:
        conn = sqlite3.connect("Phonepe.db")
        df1 = pd.read_sql("SELECT SUM(Transaction_amount) AS Transaction_amount , SUM(Transaction_count) AS"
                          " Transaction_count, Year, Quarter FROM agg_trans GROUP BY Year, Quarter", conn)
        df2 = pd.read_sql("SELECT SUM(Transaction_amount) AS Transaction_amount , SUM(Transaction_count) AS"
                          " Transaction_count, State FROM agg_trans GROUP BY State ORDER BY Transaction_amount ASC", conn)
        df3 = pd.read_sql("SELECT SUM(Transaction_amount) AS Transaction_amount , SUM(Transaction_count) AS "
                          "Transaction_count, Transaction_type, Year FROM agg_trans GROUP BY Transaction_type, Year", conn)
        st.header("Aggregated Transaction Data")
        st.write("")
        st.write("")
        st.write("")
        # st.dataframe(df1)
        fig1 = px.bar(df1, x="Year", y="Transaction_amount", color="Transaction_count", animation_frame="Quarter", range_y=[0, 25000000000000])
        fig1.update_layout(margin=dict(l=20, r=20, t=30, b=200), paper_bgcolor="Black")
        fig2 = px.scatter(df2, x="State", y="Transaction_amount", color="Transaction_count")
        fig2.update_layout(margin=dict(l=50, r=20, t=30, b=200), paper_bgcolor="Black")
        fig3 = px.bar(df3, x="Transaction_type", y="Transaction_amount", color="Transaction_count", animation_frame="Year", range_y=[0, 52000000000000])
        fig3.update_layout(margin=dict(l=50, r=20, t=30, b=200), paper_bgcolor="Black")
        fig3['layout']['updatemenus'][0]['pad'] = dict(r=10, t=100)
        fig3['layout']['sliders'][0]['pad'] = dict(r=10, t=100, )
        st.subheader("1. Year vs Transaction Amount:", divider='gray')
        st.plotly_chart(fig1, theme=None)
        st.subheader("2. Transaction Type vs Transaction Amount:", divider='gray')
        st.plotly_chart(fig3, theme=None)
        st.subheader("3. State vs Transaction Amount:", divider='gray')
        st.plotly_chart(fig2, theme=None)

    # ------------------------------------------------------tab2----------------------------------------------

    with tab2:
        conn = sqlite3.connect("Phonepe.db")
        st.header("Aggregated User Data")
        st.write("")
        st.write("")
        st.write("")
        df1 = pd.read_sql("SELECT SUM(Count) AS No_of_registered_users, Brands, Year FROM agg_user GROUP "
                          "BY Brands, Year", conn)
        df2 = pd.read_sql("SELECT SUM(Count) AS No_of_registered_users, Year FROM agg_user "
                          "GROUP BY Year", conn)
        # df3 = pd.read_sql("SELECT * FROM agg_user", conn)
        # st.dataframe(df3)
        # st.dataframe(df2)
        fig1 = px.bar(df1, x="Brands", y="No_of_registered_users", animation_frame="Year", range_y=[0, 320000000])
        fig1.update_layout(margin=dict(l=60, r=20, t=30, b=200), paper_bgcolor="Black")
        fig2 = px.bar(df2, x="Year", y="No_of_registered_users")
        fig2.update_layout(margin=dict(l=60, r=20, t=30, b=125), paper_bgcolor="Black")
        st.subheader("1. Year vs No of users:", divider='gray')
        st.plotly_chart(fig2, theme=None)
        st.subheader("2. Brands vs No of users:", divider='gray')
        st.plotly_chart(fig1, theme=None)

# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------District Data Page --------------------------------------------------
if side_bar_object == "District Data":
    tab1, tab2 = st.tabs(["Transaction Data", "User Data"])
    conn = sqlite3.connect("Phonepe.db")

    # ------------------------------------------------------tab1----------------------------------------------
    with tab1:
        st.header("District Transaction Data")
        st.write("")
        st.write("")
        st.write("")

        def state_selection(selected_state, conn):
            query = ("SELECT SUM(Count) AS Transaction_Count, SUM(Amount) AS Transaction_Amount, Year, District FROM"
                     " map_trans WHERE State = ? GROUP BY Year, District")
            sdf = pd.read_sql_query(query, conn, params=[selected_state])

            figg1 = px.scatter(sdf, x="District", y="Transaction_Amount", color="Transaction_Count", animation_frame="Year")
            initial_y_range = [0, sdf["Transaction_Amount"].max()]
            figg1.update_yaxes(range=initial_y_range)
            figg1.update_layout(margin=dict(l=20, r=20, t=30, b=200), paper_bgcolor="Black")
            figg1['layout']['updatemenus'][0]['pad'] = dict(r=10, t=150)
            figg1['layout']['sliders'][0]['pad'] = dict(r=10, t=150, )

            st.plotly_chart(figg1, theme=None)


        def quarter(state, year):
            query = ("SELECT SUM(Count) AS Transaction_Count, SUM(Amount) AS Transaction_Amount, District, Quarter FROM"
                     " map_trans WHERE State = ? AND Year = ? GROUP BY Quarter, District")
            dff = pd.read_sql_query(query, conn, params=[state, year])
            figggg = px.scatter(dff, x="District", y="Transaction_Amount", color="Transaction_Count", animation_frame="Quarter")
            initial_y_range = [0, dff["Transaction_Amount"].max()]
            figggg.update_yaxes(range=initial_y_range)
            figggg.update_layout(margin=dict(l=20, r=20, t=30, b=200), paper_bgcolor="Black")
            figggg['layout']['updatemenus'][0]['pad'] = dict(r=10, t=150)
            figggg['layout']['sliders'][0]['pad'] = dict(r=10, t=150, )
            st.plotly_chart(figggg, theme=None)



        df = pd.read_sql("SELECT * FROM map_trans", conn)
        list_of_states = df["State"].unique()
        st.subheader("1. District vs Transaction Amount", divider='gray')
        selected_state = st.selectbox("Select any State to get there respective district view", list_of_states)

        if selected_state:
            state_selection(selected_state=selected_state, conn=conn)

        st.subheader("2. District vs Quarter", divider='gray')
        state = st.selectbox("Select any State", list_of_states)
        year = st.selectbox("Select any Year", ['2018', '2019', '2020', '2021', '2022', '2023'])

        if state and year:
            quarter(state=state, year=year)

    # ------------------------------------------------------tab2----------------------------------------------

    with tab2:
        # st.dataframe(pd.read_sql("SELECT * FROM map_user", conn))
        st.header("District Registered User")
        st.write("")
        st.write("")
        st.write("")


        def state_selections(selected_state, conn):
            query = ("SELECT SUM(RegisteredUser) AS Registered_User, SUM(AppOpens) AS App_Opens, Year, District FROM"
                     " map_user WHERE State = ? GROUP BY Year, District")
            sdf = pd.read_sql_query(query, conn, params=[selected_state])

            figg1 = px.scatter(sdf, x="District", y="Registered_User", color="App_Opens",
                               animation_frame="Year")
            initial_y_range = [0, sdf["Registered_User"].max()]
            figg1.update_yaxes(range=initial_y_range)
            figg1.update_layout(margin=dict(l=50, r=20, t=30, b=200), paper_bgcolor="Black")
            figg1['layout']['updatemenus'][0]['pad'] = dict(r=10, t=150)
            figg1['layout']['sliders'][0]['pad'] = dict(r=10, t=150, )

            st.plotly_chart(figg1, theme=None)


        def quarters(state, year):
            query = ("SELECT SUM(RegisteredUser) AS Registered_User, SUM(AppOpens) AS App_Opens, Quarter, District FROM"
                     " map_user WHERE State = ? AND Year = ? GROUP BY Quarter, District")
            dff = pd.read_sql_query(query, conn, params=[state, year])
            figggg = px.scatter(dff, x="District", y="Registered_User", color="App_Opens",
                                animation_frame="Quarter")
            initial_y_range = [0, dff["Registered_User"].max()]
            figggg.update_yaxes(range=initial_y_range)
            figggg.update_layout(margin=dict(l=20, r=20, t=30, b=200), paper_bgcolor="Black")
            figggg['layout']['updatemenus'][0]['pad'] = dict(r=10, t=150)
            figggg['layout']['sliders'][0]['pad'] = dict(r=10, t=150, )
            st.plotly_chart(figggg, theme=None)



        df = pd.read_sql("SELECT * FROM map_user", conn)
        list_of_states = df["State"].unique()
        st.subheader("District vs Registered User", divider='gray')
        selected_states = st.selectbox("Select any State to get there respective district", list_of_states)
        if selected_states:
            state_selections(selected_state=selected_states, conn=conn)

        st.subheader("2. Registered User vs Quarter", divider='gray')
        state1 = st.selectbox("Select any States", list_of_states)
        year1 = st.selectbox("Select any Years", ['2018', '2019', '2020', '2021', '2022', '2023'])

        if state1 and year1:
            quarters(state=state1, year=year1)

# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------ Top Data Page ------------------------------------------------------------------
if side_bar_object == "Geography Data":
    st.header("Geography user and Transaction Data")
    conn = sqlite3.connect("Phonepe.db")


    def map(year):
            query = ("SELECT SUM(Transaction_amount) AS Transaction_Amount, State FROM top_trans WHERE Year = ? GROUP"
                     " BY State")
            df = pd.read_sql_query(query, conn, params=[year])
            df2 = pd.read_csv('statename.csv')
            df["State"] = df2

            fig54 = px.choropleth(df, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/"
                                            "raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Transaction_Amount',
                                color_continuous_scale='oranges',
                                width=900,
                                height=600)

            # Update map layout
            fig54.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig54, use_container_width=True)

            query = ("SELECT SUM(RegisteredUsers) AS Registered_Users, State FROM top_user WHERE Year = ? GROUP"
                     " BY State")
            d = pd.read_sql_query(query, conn, params=[year])
            df = pd.read_csv('statename.csv')
            d["State"] = df

            ffig = px.choropleth(d, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/"
                                        "raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Registered_Users',
                                color_continuous_scale='oranges',
                                width=900,
                                height=600)

            # Update map layout
            ffig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(ffig, use_container_width=True)


    year1 = st.selectbox("Select any Years", ['2018', '2019', '2020', '2021', '2022', '2023'])

    if year1:
        map(year=year1)
