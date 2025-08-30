#Package import:
import streamlit as st
import mysql.connector as db
import pandas as pd 
from Traffic_data import Traffic_details as TD
data = TD()

connection = db.connect(
    host ='localhost',
    user ='gowtham',
    password ='Gautisql',
    database ='police_secure_check'
)
curr = connection.cursor()


#Streamlit:

st.sidebar.title("📑 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "👮🚦 Traffic Reports", "👨🏻‍💻 Advanced Insights"])
st.balloons()
st.snow()

# 🏠 HOME PAGE
if page == "🏠 Home":
    st.title("Welcome to Police Traffic Dashboard 🚔")
    st.warning("🚫🍺🍷 Don't drink and drive! 🚗 Stay safe and responsible. 🚓🚨⚠️")
    st.success("🪖 Wear Helmet, Go slow! 👮🚦Follow Traffic Rules! ⚠️")
    st.markdown("""
    This app allows you to explore police traffic stop records easily. 
    Use the sidebar to navigate between different pages. 
    **Below, you can watch an awareness video about important traffic rules:**
    """)
    st.video("https://www.youtube.com/watch?v=aT61nwd5U-s")
    
    
# 👮🚦 TRAFFIC REPORTS PAGE
elif page == "👮🚦 Traffic Reports":
    st.title("Police Traffic Reports")

    st.markdown("""
    Hello, this record is based on traffic violation details.  
    Here you can find your police log & predict outcome and violation.  
    **Fields marked with * are mandatory.**
    """)

    # Dropdowns & inputs
    Vechile_num = st.selectbox('Vehicle Number*', data['vehicle_number'].unique()) 
    Gender = st.selectbox('Select Gender*', data['driver_gender'].unique())
    Age = st.selectbox('Select Age*', data['driver_age'].unique())
    Date = st.date_input('Select date here')
    Time = st.time_input('Select the time of stop')
    #Stop_Duration = st.selectbox('Stop Duration', data['stop_duration'].unique())

    if st.button('Check here'):
        Verify= data[
            (data['vehicle_number']== Vechile_num) &
            (data['driver_gender']==Gender) &
            (data['driver_age']==Age)
            #(data['stop_duration']== Stop_Duration)
        ]
        if not Verify.empty:
            row = Verify.iloc[0]
            def pronounce(gender):
                return "he" if gender.lower() == "male" else "she"
            
            st.success("✅ Operation completed successfully! Here are your details.")
            summary = f"""
            🚗 A **{row['driver_age']}-year-old** **{row['driver_gender']} driver**  
            was stopped for **{row['violation']}** at **{row['stop_time']}**.  
            **{row['search_conducted']}**, and {pronounce(row['driver_gender'])} received a **{row['stop_outcome']}**.  
            The stop lasted **{row['stop_duration']}** and it was **{row['drugs_related_stop']}**.
            """
            st.markdown(summary)

# 👨🏻‍💻 ADVANCED INSIGHTS PAGE:


elif page == "👨🏻‍💻 Advanced Insights":
    st.title("📊 Advanced Insights")
    st.markdown("Here You Can Search Advanced Traffic Related Data Insights.")

    selected_query = st.selectbox(
        "Select a Query to Run",
        [
            "top 10 drug-related vehicle_Number",
            "most frequently searched Vehicle",
            "Highest arrest rate driver Age group",
            "Gender distribution of drivers stopped in each country",
            "race and gender combination has the highest search rate",
            "time of day sees the most traffic stops",
            "average stop duration for different violations",
            "stops during the night more likely to lead to arrests",
            "violations are most associated with searches or arrests",
            "violations are most common among younger drivers (<25)",
            "a violation that rarely results in search or arrest",
            "countries report the highest rate of drug-related stops",
            "arrest rate by country and violation",
            "country has the most stops with search conducted",
            "Yearly Breakdown of Stops and Arrests by Country",
            "Driver Violation Trends Based on Age and Race",
            "Time Period Analysis of Stops, Number of Stops by Year,Month, Hour of the Day",
            "Violations with High Search and Arrest Rates",
            "Driver Demographics by Country (Age, Gender, and Race)",
            "Top 5 Violations with Highest Arrest Rates"
        ]
    )

    if st.button("Run"):
        # Map query
        if selected_query == "top 10 drug-related vehicle_Number":
            sql = "SELECT vehicle_number, COUNT(*) as cnt FROM Police_traffic_details1 WHERE drugs_related_stop='1' GROUP BY vehicle_number ORDER BY cnt DESC LIMIT 10;"
        
        elif selected_query == "most frequently searched Vehicle":
            sql = "SELECT vehicle_number, COUNT(*) as searches FROM Police_traffic_details1 WHERE search_conducted='1' GROUP BY vehicle_number ORDER BY searches DESC LIMIT 1;"

        elif selected_query == "Highest arrest rate driver Age group":
            sql = "SELECT driver_age, COUNT(*) as arrests FROM Police_traffic_details1 WHERE stop_outcome='Arrest' GROUP BY driver_age ORDER BY arrests DESC LIMIT 1;"
        elif selected_query =="Gender distribution of drivers stopped in each country":
            sql = "SELECT country_name, driver_gender, COUNT(*) as driver_count FROM Police_traffic_details1 GROUP BY country_name, driver_gender;"
        elif selected_query =="race and gender combination has the highest search rate":
            sql ="SELECT driver_race, driver_gender, AVG(search_conducted) as search_rate FROM Police_traffic_details1 GROUP BY driver_race, driver_gender ORDER BY search_rate DESC LIMIT 1;"
        elif selected_query =="time of day sees the most traffic stops":
            sql ="SELECT stop_time, COUNT(*) as stop_count FROM Police_traffic_details1 GROUP BY stop_time ORDER BY stop_count DESC LIMIT 1;"
        elif selected_query =="average stop duration for different violations":
            sql ="SELECT violation, AVG(CASE stop_duration WHEN '0-15 Min' THEN 7.5 WHEN '16-30 Min' THEN 23 WHEN '30+ Min' THEN 40 END) as avg_stop_duration_min FROM Police_traffic_details1 GROUP BY violation;"
        elif selected_query =="stops during the night more likely to lead to arrests":
            sql ="SELECT SUM(CASE WHEN stop_time BETWEEN '20:00:00' AND '23:59:59' OR stop_time BETWEEN '00:00:00' AND '05:59:59' THEN is_arrested ELSE 0 END) * 1.0 /NULLIF(SUM(CASE WHEN stop_time BETWEEN '20:00:00' AND '23:59:59' OR stop_time BETWEEN '00:00:00' AND '05:59:59' THEN 1 ELSE 0 END),0) as night_arrest_rateFROM Police_traffic_details1;"
        elif selected_query =="violations are most associated with searches or arrests":
            sql ="SELECT violation,AVG(search_conducted) as search_rate,AVG(is_arrested) as arrest_rate FROM Police_traffic_details1 GROUP BY violation ORDER BY search_rate DESC, arrest_rate DESC;"
        elif selected_query =="a violation that rarely results in search or arrest":
            sql ="SELECT violation, COUNT(*) as count FROM Police_traffic_details1 WHERE driver_age < 25 GROUP BY violation ORDER BY count DESC;"
        elif selected_query =="countries report the highest rate of drug-related stops":
            sql ="SELECT country_name, AVG(drugs_related_stop) as drug_stop_rate FROM Police_traffic_details1 GROUP BY country_name ORDER BY drug_stop_rate DESC;"
        elif selected_query =="arrest rate by country and violation":
            sql = "SELECT country_name, violation, AVG(is_arrested) as arrest_rate FROM Police_traffic_details1 GROUP BY country_name, violation;"
        elif selected_query =="country has the most stops with search conducted":
            sql = "SELECT country_name, SUM(search_conducted) as searches FROM Police_traffic_details1 GROUP BY country_name ORDER BY searches DESC LIMIT 1;"
        elif selected_query == "Yearly Breakdown of Stops and Arrests by Country":
            sql ="SELECT EXTRACT(YEAR FROM stop_date) as year,country_name,COUNT(*) as total_stops,SUM(is_arrested) as total_arrests FROM Police_traffic_details1 GROUP BY year, country_name;"
        elif selected_query =="Driver Violation Trends Based on Age and Race":
            sql = "SELECT age_bracket, driver_race, violation, COUNT(*) as count FROM (SELECT CASE WHEN driver_age < 25 THEN '<25' WHEN driver_age BETWEEN 25 AND 40 THEN '25-40' ELSE '40+' END as age_bracket, driver_race, violation FROM Police_traffic_details1) sub GROUP BY age_bracket, driver_race, violation;"
        elif selected_query =="Time Period Analysis of Stops, Number of Stops by Year,Month, Hour of the Day":
            sql = "SELECT EXTRACT(YEAR FROM stop_date) as year,EXTRACT(MONTH FROM stop_date) as month, EXTRACT(HOUR FROM stop_time) as hour, COUNT(*) as stop_count FROM Police_traffic_details1 GROUP BY year, month, hour;"
        elif selected_query == "Violations with High Search and Arrest Rates":
            sql = "SELECT violation, AVG(search_conducted) OVER(PARTITION BY violation) as violation_search_rate,AVG(is_arrested) OVER(PARTITION BY violation) as violation_arrest_rate FROM Police_traffic_details1;"
        elif selected_query == "Driver Demographics by Country (Age, Gender, and Race)":
            sql = "SELECT country_name, AVG(driver_age) as avg_age, driver_gender, driver_race, COUNT(*) as count FROM Police_traffic_details1 GROUP BY country_name, driver_gender, driver_race;"
        elif selected_query == "Top 5 Violations with Highest Arrest Rates":
            sql = "SELECT violation, AVG(is_arrested) as arrest_rate FROM Police_traffic_details1 GROUP BY violation ORDER BY arrest_rate DESC LIMIT 5;"

        st.write(f"🔍 You selected: **{selected_query}**")
        st.code(sql, language="sql")   
        st.success('Query executed successfully', icon="✅")

        # Execute the SQL and show result
        curr.execute(sql)
        result = curr.fetchall()
        col_names = [desc[0] for desc in curr.description] 
    
    # Convert to DataFrame
        df = pd.DataFrame(result, columns=col_names)

    # Show in Streamlit
        st.dataframe(df)
