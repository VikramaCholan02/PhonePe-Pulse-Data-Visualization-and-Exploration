import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image

# Dataframe Collection

# Mysql_connection:
mydb=mysql.connector.connect(host="127.0.0.1",
                            user="root",
                            password="rootroot",
                            database="phonepe_data",
                            port="3306")
cursor= mydb.cursor()

# 1. Aggregated_Insurence_[DF]:
cursor.execute("SELECT * FROM aggregated_insurance")
table_1=cursor.fetchall()
mydb.commit()

Aggr_insurance = pd.DataFrame(table_1, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count",
                                                "Transaction_amount"))

# 2. Aggregated_Transaction_[DF]:
cursor.execute("SELECT * FROM aggregated_transaction")
table_2=cursor.fetchall()
mydb.commit()

Aggr_transaction = pd.DataFrame(table_2, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count",
                                                "Transaction_amount"))

# 3. Aggregated_user_[DF]:
cursor.execute("SELECT * FROM aggregated_user")
table_3=cursor.fetchall()
mydb.commit()

Aggr_user = pd.DataFrame(table_3, columns=("States", "Years", "Quarter", "Brands", "Transaction_count",
                                            "Percentage"))

# 4. Map_Insurance_[DF]:
cursor.execute("SELECT * FROM map_insurance")
table_4=cursor.fetchall()
mydb.commit()

Map_insurance = pd.DataFrame(table_4, columns=("States", "Years", "Quarter", "Districts", "Transaction_count",
                                               "Transaction_amount"))

# 5. Map_Transaction_[DF]:
cursor.execute("SELECT * FROM map_transaction")
table_5=cursor.fetchall()
mydb.commit()

Map_transaction = pd.DataFrame(table_5, columns=("States", "Years", "Quarter", "Districts", "Transaction_count",
                                                 "Transaction_amount"))

# 6. Map_User_[DF]:
cursor.execute("SELECT * FROM map_user")
table_6=cursor.fetchall()
mydb.commit()

Map_user = pd.DataFrame(table_6, columns=("States", "Years", "Quarter", "Districts", "RegisteredUsers",
                                          "AppOpens"))

# 7. Top_Insurance_[DF]:
cursor.execute("SELECT * FROM top_insurance")
table_7=cursor.fetchall()
mydb.commit()

Top_insurance = pd.DataFrame(table_7, columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count",
                                               "Transaction_amount"))

# 8. Top_Transaction_[DF]:
cursor.execute("SELECT * FROM top_transaction")
table_8=cursor.fetchall()
mydb.commit()

Top_transaction = pd.DataFrame(table_8, columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count",
                                               "Transaction_amount"))

# 9. Top_User_[DF]:
cursor.execute("SELECT * FROM top_user")
table_9=cursor.fetchall()
mydb.commit()

Top_user = pd.DataFrame(table_9, columns=("States", "Years", "Quarter", "Pincodes", "RegisteredUsers"))

#....................................................[Aggregated_Insurance]...................................................................#

def Transaction_amount_count_Yr(df, year):

    tr_am_ct_yr=df[df["Years"] == year]
    tr_am_ct_yr.reset_index(drop = True, inplace = True)

    tr_am_ct_yr_g = tr_am_ct_yr.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tr_am_ct_yr_g.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:

        tra_amount = px.bar(tr_am_ct_yr_g, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence= px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(tra_amount)

    with col2:   

        tra_count = px.bar(tr_am_ct_yr_g, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                            color_discrete_sequence= px.colors.sequential.thermal_r, height= 650, width= 600)
        st.plotly_chart(tra_count)


    col1,col2= st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_names = []
        for feature in data1["features"]:
            states_names.append(feature["properties"]["ST_NM"])

        states_names.sort()

        fig_india_1 = px.choropleth(tr_am_ct_yr_g, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount", color_continuous_scale= "viridis",
                                    range_color= (tr_am_ct_yr_g["Transaction_amount"].min(), tr_am_ct_yr_g["Transaction_amount"].max()),
                                    hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                    height= 600, width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2 = px.choropleth(tr_am_ct_yr_g, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count", color_continuous_scale= "Plasma",
                                    range_color= (tr_am_ct_yr_g["Transaction_count"].min(), tr_am_ct_yr_g["Transaction_count"].max()),
                                    hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                    height= 600, width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tr_am_ct_yr

def Transaction_amount_count_Yr_Q(df, quarter):
    tr_am_ct_yr=df[df["Quarter"] == quarter]
    tr_am_ct_yr.reset_index(drop = True, inplace = True)

    tr_am_ct_yr_g = tr_am_ct_yr.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tr_am_ct_yr_g.reset_index(inplace = True)

    col1,col2= st.columns(2)
    with col1:

        tra_amount = px.bar(tr_am_ct_yr_g, x="States", y="Transaction_amount", title=f"{tr_am_ct_yr['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence= px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(tra_amount)

    with col2:

        tra_count = px.bar(tr_am_ct_yr_g, x="States", y="Transaction_count", title=f"{tr_am_ct_yr['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                            color_discrete_sequence= px.colors.sequential.thermal_r, height= 650, width= 600)
        st.plotly_chart(tra_count)

    col1,col2= st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_names = []
        for feature in data1["features"]:
            states_names.append(feature["properties"]["ST_NM"])

        states_names.sort()
        # MAP PLOT:
        fig_india_1 = px.choropleth(tr_am_ct_yr_g, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount", color_continuous_scale= "viridis",
                                    range_color= (tr_am_ct_yr_g["Transaction_amount"].min(), tr_am_ct_yr_g["Transaction_amount"].max()),
                                    hover_name= "States", title= f"{tr_am_ct_yr['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                    height= 600, width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(tr_am_ct_yr_g, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count", color_continuous_scale= "Plasma",
                                    range_color= (tr_am_ct_yr_g["Transaction_count"].min(), tr_am_ct_yr_g["Transaction_count"].max()),
                                    hover_name= "States", title= f"{tr_am_ct_yr['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                    height= 600, width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tr_am_ct_yr

#................................................[Aggregated_Transaction]......................................................................#

def Aggr_Tran_Transaction_Type(df, state):

    tr_am_ct_yr=df[df["States"] == state]
    tr_am_ct_yr.reset_index(drop = True, inplace = True)

    tr_am_ct_yr_g = tr_am_ct_yr.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    tr_am_ct_yr_g.reset_index(inplace = True)

    col1,col2= st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame= tr_am_ct_yr_g, names= "Transaction_type", values= "Transaction_amount",
                        width= 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame= tr_am_ct_yr_g, names= "Transaction_type", values= "Transaction_count",
                        width= 600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)

# [1]. AGGREGATED_USER_ANALYSIS:
def Aggregated_user_plot_1(df, year):
    ag_u_y= df[df["Years"]== year]
    ag_u_y.reset_index(drop= True, inplace= True)

    ag_u_y_g= pd.DataFrame(ag_u_y.groupby("Brands")["Transaction_count"].sum())
    ag_u_y_g.reset_index(inplace= True)

    fig_bar_1= px.bar(ag_u_y_g, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Bluered, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return ag_u_y

# [2]. AGGREGATED_USER_ANALYSIS:
def Aggregated_user_plot_2(df, quarter):
    ag_u_y_q= df[df["Quarter"]== quarter]
    ag_u_y_q.reset_index(drop= True, inplace= True)

    ag_u_y_q_g= pd.DataFrame(ag_u_y_q.groupby("Brands")["Transaction_count"].sum())
    ag_u_y_q_g.reset_index(inplace= True)

    fig_bar_1= px.bar(ag_u_y_q_g, x= "Brands", y= "Transaction_count", title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return ag_u_y_q

# [3]. AGGREGATED_USER_ANALYSIS:
def Aggregated_user_plot_3(df, state):
    ag_u_y_q_s= df[df["States"] == state]
    ag_u_y_q_s.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(ag_u_y_q_s, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", color_discrete_sequence= px.colors.sequential.Magma,
                        width= 1000, markers= True)
    st.plotly_chart(fig_line_1)

# MAP_INSURANCE_DISTRICT:
def Map_Ins_Districts(df, state):

    tr_am_ct_yr=df[df["States"] == state]
    tr_am_ct_yr.reset_index(drop = True, inplace = True)

    tr_am_ct_yr_g = tr_am_ct_yr.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    tr_am_ct_yr_g.reset_index(inplace = True)

    col1,col2= st.columns(2)

    with col1:

        fig_bar_1 = px.bar(data_frame= tr_am_ct_yr_g, x= "Transaction_amount", y= "Districts", orientation= "h", height= 600,
                        title = f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Burgyl_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2 = px.bar(data_frame= tr_am_ct_yr_g, x= "Transaction_count", y= "Districts", orientation= "h", height= 600,
                        title = f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.solar_r)
        st.plotly_chart(fig_bar_2)

# [1]. MAP_USER_PLOT
def Map_user_plot_1(df, year):
    Map_use_y= df[df["Years"]== year].drop_duplicates().reset_index(drop=True)
    Map_use_y.reset_index(drop= True, inplace= True)

    Map_use_y_g= Map_use_y.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    Map_use_y_g.reset_index(inplace= True)

    fig_line_1= px.line(Map_use_y_g, x= "States", y= ["RegisteredUsers", "AppOpens"],
                        title= f"{year} REGISTERED USER AND APPOPENS",width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return Map_use_y

# [2]. MAP_USER_PLOT
def Map_user_plot_2(df, quarter):
    Map_use_y_q= df[df["Quarter"]== quarter].drop_duplicates().reset_index(drop=True)
    Map_use_y_q.reset_index(drop= True, inplace= True)

    Map_use_y_q_g= Map_use_y_q.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    Map_use_y_q_g.reset_index(inplace= True)

    fig_line_1= px.line(Map_use_y_q_g, x= "States", y= ["RegisteredUsers", "AppOpens"],
                        title= f"{df['Years'].min()} YEAR, {quarter} QUARTER REGISTERED USER AND APPOPENS",width= 1000, height= 800, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return Map_use_y_q

# [3]. MAP_USER_PLOT
def Map_user_plot_3(df, states):
    Map_use_y_q_s= df[df["States"]== states].drop_duplicates().reset_index(drop=True)
    Map_use_y_q_s.reset_index(drop= True, inplace= True)

    fig_map_user_bar_1= px.bar(Map_use_y_q_s, x= "RegisteredUsers", y= "Districts", orientation= "h",
                            title= f"{states.upper()} REGESTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_map_user_bar_1)

    fig_map_user_bar_2= px.bar(Map_use_y_q_s, x= "AppOpens", y= "Districts", orientation= "h",
                            title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Bluered)
    st.plotly_chart(fig_map_user_bar_2)

# [1]. TOP_INSURANCE_PLOT:
def Top_insurance_plot_1(df, state):
    trn_ins_y= df[df["States"]== state]
    trn_ins_y.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)

    with col1:

        fig_top_ins_bar_1= px.bar(trn_ins_y, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                title= "TRANSACTION AMOUNT", height= 650, color_discrete_sequence= px.colors.sequential.Oranges_r)
        st.plotly_chart(fig_top_ins_bar_1)

    with col2:

        fig_top_ins_bar_2= px.bar(trn_ins_y, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                                title= "TRANSACTION COUNT", height= 650, color_discrete_sequence= px.colors.sequential.Emrld)
        st.plotly_chart(fig_top_ins_bar_2)

# [1]. TOP_USER_PLOT_1:
def Top_user_plot_1(df, year):
    Top_u_y= df[df["Years"]== year]
    Top_u_y.reset_index(drop= True, inplace= True)

    Top_u_y_g= pd.DataFrame(Top_u_y.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    Top_u_y_g.reset_index(inplace= True)

    fig_top_use_plot_1= px.bar(Top_u_y_g, x= "States", y= "RegisteredUsers", color= "Quarter", width= 1000, height= 800,
                            color_discrete_sequence= px.colors.sequential.Viridis_r, hover_name= "States",
                            title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_use_plot_1)

    return Top_u_y

# [2]. TOP_USER_PLOT:
def Top_user_plot_2(df, state):
    Top_u_y_s= df[df["States"]== state]
    Top_u_y_s.reset_index(drop= True, inplace= True)

    fig_top_use_plot_2= px.bar(Top_u_y_s, x= "Quarter", y= "RegisteredUsers", title= "REGISTERED USER, PINCODES, QUARTER",
                            width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                            color_continuous_scale= px.colors.sequential.Viridis_r)

    st.plotly_chart(fig_top_use_plot_2)

#[1]
# Mysql_connection :
def Top_chart_transaction_amount(table_name):
    mydb=mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="rootroot",
                                database="phonepe_data",
                                port="3306")
    cursor= mydb.cursor()

    # QUERY_1
    query1= f'''SELECT states, SUM(Transaction_amount) AS Transaction_amount FROM {table_name}
                GROUP BY states ORDER BY Transaction_amount DESC LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("States", "Transaction_amount"))

    col1,col2= st.columns(2)
    with col1:

        tra_amount = px.bar(df_1, x="States", y="Transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "States",
                            color_discrete_sequence= px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(tra_amount)

    # QUERY_2
    query2= f'''SELECT states, SUM(Transaction_amount) AS Transaction_amount FROM {table_name}
                GROUP BY states ORDER BY Transaction_amount LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("States", "Transaction_amount"))

    with col2:
        tra_amount_2 = px.bar(df_2, x="States", y="Transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "States",
                            color_discrete_sequence= px.colors.sequential.Bluered, height= 650, width= 600)
        st.plotly_chart(tra_amount_2)

    # QUERY_3
    query3= f'''SELECT states, AVG(Transaction_amount) AS Transaction_amount FROM {table_name}
            GROUP BY states ORDER BY Transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("States", "Transaction_amount"))

    tra_amount_3 = px.bar(df_3, y="States", x="Transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "States", orientation= "h",
                        color_discrete_sequence= px.colors.sequential.Cividis_r, height= 800, width= 1000)
    st.plotly_chart(tra_amount_3)

# [2]
# Mysql_connection :
def Top_chart_transaction_count(table_name):
    mydb=mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="rootroot",
                                database="phonepe_data",
                                port="3306")
    cursor= mydb.cursor()

    # QUERY_1
    query1= f'''SELECT states, SUM(Transaction_count) AS Transaction_count FROM {table_name}
                GROUP BY states ORDER BY Transaction_count DESC LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("States", "Transaction_count"))

    col1,col2= st.columns(2)
    with col1:

        tra_amount = px.bar(df_1, x="States", y="Transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "States",
                            color_discrete_sequence= px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(tra_amount)

    # QUERY_2
    query2= f'''SELECT states, SUM(Transaction_count) AS Transaction_count FROM {table_name}
                GROUP BY states ORDER BY Transaction_count LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("States", "Transaction_count"))

    with col2:

        tra_amount_2 = px.bar(df_2, x="States", y="Transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "States",
                            color_discrete_sequence= px.colors.sequential.Bluered, height= 650, width= 600)
        st.plotly_chart(tra_amount_2)

    # QUERY_3
    query3= f'''SELECT states, AVG(Transaction_count) AS Transaction_count FROM {table_name}
            GROUP BY states ORDER BY Transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("States", "Transaction_count"))

    tra_amount_3 = px.bar(df_3, y="States", x="Transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "States", orientation= "h",
                        color_discrete_sequence= px.colors.sequential.Cividis_r, height= 800, width= 1000)
    st.plotly_chart(tra_amount_3)

# [3]
# Mysql_connection :
def Top_chart_Registered_user(table_name, state):
    mydb=mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="rootroot",
                                database="phonepe_data",
                                port="3306")
    cursor= mydb.cursor()

    # QUERY_1
    query1= f'''SELECT Districts, SUM(RegisteredUsers) AS RegisteredUsers  FROM {table_name} WHERE states= "{state}"
                GROUP BY Districts ORDER BY RegisteredUsers DESC LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("Districts", "RegisteredUsers"))

    col1,col2= st.columns(2)
    with col1:

        tra_amount = px.bar(df_1, x="Districts", y="RegisteredUsers", title="TOP 10 REGISTERED USER", hover_name= "Districts",
                            color_discrete_sequence= px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(tra_amount)

    # QUERY_2
    query2= f'''SELECT Districts, SUM(RegisteredUsers) AS RegisteredUsers  FROM {table_name} WHERE states= "{state}"
                GROUP BY Districts ORDER BY RegisteredUsers ASC LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("Districts", "RegisteredUsers"))

    with col2:

        tra_amount_2 = px.bar(df_2, x="Districts", y="RegisteredUsers", title="LAST 10 REGISTERED USERS", hover_name= "Districts",
                            color_discrete_sequence= px.colors.sequential.Bluered, height= 650, width= 600)
        st.plotly_chart(tra_amount_2)

    # QUERY_3
    query3= f'''SELECT Districts, AVG(RegisteredUsers) AS RegisteredUsers  FROM {table_name}  WHERE states= "{state}"
                GROUP BY Districts ORDER BY RegisteredUsers;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("Districts", "RegisteredUsers"))

    tra_amount_3 = px.bar(df_3, y="Districts", x="RegisteredUsers", title="AVERAGE OF REGISTERED USERS", hover_name= "Districts", orientation= "h",
                        color_discrete_sequence= px.colors.sequential.Cividis_r, height= 800, width= 1000)
    st.plotly_chart(tra_amount_3)

# [4]
# Mysql_connection :
def Top_chart_Appopens(table_name, state):
    mydb=mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="rootroot",
                                database="phonepe_data",
                                port="3306")
    cursor= mydb.cursor()

    # QUERY_1
    query1= f'''SELECT Districts, SUM(AppOpens) AS AppOpens  FROM {table_name} WHERE states= "{state}"
                GROUP BY Districts ORDER BY AppOpens DESC LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("Districts", "AppOpens"))

    col1,col2= st.columns(2)
    with col1:

        tra_amount = px.bar(df_1, x="Districts", y="AppOpens", title="TOP 10 APPOPENS", hover_name= "Districts",
                            color_discrete_sequence= px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(tra_amount)

    # QUERY_2
    query2= f'''SELECT Districts, SUM(AppOpens) AS AppOpens  FROM {table_name} WHERE states= "{state}"
                GROUP BY Districts ORDER BY AppOpens ASC LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("Districts", "AppOpens"))

    with col2:

        tra_amount_2 = px.bar(df_2, x="Districts", y="AppOpens", title="LAST 10 APPOPENS", hover_name= "Districts",
                            color_discrete_sequence= px.colors.sequential.Bluered, height= 650, width= 600)
        st.plotly_chart(tra_amount_2)

    # QUERY_3
    query3= f'''SELECT Districts, AVG(AppOpens) AS AppOpens  FROM {table_name}  WHERE states= "{state}"
                GROUP BY Districts ORDER BY AppOpens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("Districts", "AppOpens"))

    tra_amount_3 = px.bar(df_3, y="Districts", x="AppOpens", title="AVERAGE OF APPOPENS", hover_name= "Districts", orientation= "h",
                        color_discrete_sequence= px.colors.sequential.Cividis_r, height= 800, width= 1000)
    st.plotly_chart(tra_amount_3)

# [5]
# Mysql_connection :
def Top_chart_Registered_users(table_name):
    mydb=mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="rootroot",
                                database="phonepe_data",
                                port="3306")
    cursor= mydb.cursor()

    # QUERY_1
    query1= f'''SELECT States, SUM(RegisteredUsers) AS RegisteredUsers FROM {table_name} GROUP BY States
                ORDER BY RegisteredUsers DESC LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("States", "RegisteredUsers"))

    col1,col2= st.columns(2)
    with col1:

        tra_amount = px.bar(df_1, x="States", y="RegisteredUsers", title="TOP 10 REGISTERED USERS", hover_name= "States",
                            color_discrete_sequence= px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(tra_amount)

    # QUERY_2
    query2= f'''SELECT States, SUM(RegisteredUsers) AS RegisteredUsers FROM {table_name} GROUP BY States
                ORDER BY RegisteredUsers ASC LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("States", "RegisteredUsers"))

    with col2:

        tra_amount_2 = px.bar(df_2, x="States", y="RegisteredUsers", title="LAST 10 REGISTERED USERS", hover_name= "States",
                            color_discrete_sequence= px.colors.sequential.Bluered, height= 650, width= 600)
        st.plotly_chart(tra_amount_2)

    # QUERY_3
    query3= f'''SELECT States, AVG(RegisteredUsers) AS RegisteredUsers FROM {table_name} GROUP BY States
                ORDER BY RegisteredUsers ASC;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("States", "RegisteredUsers"))

    tra_amount_3 = px.bar(df_3, y="States", x="RegisteredUsers", title="AVERAGE OF REGISTERED USERS", hover_name= "States", orientation= "h",
                        color_discrete_sequence= px.colors.sequential.Cividis_r, height= 800, width= 1000)
    st.plotly_chart(tra_amount_3)



# STREAMLIT PART

st.set_page_config(layout= "wide")
st.title(":violet[PHONEPE DATA VISUALISATION AND EXPLORATION]")
 
select = option_menu(None,
                       options = ["About","Home","Statistical analysis","Top Charts"],
                                  orientation="horizontal")
#.........................................................[ABOUT]..............................................................................#
if select == "About":

    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:    
        st.markdown("# :violet[Data Visualization and Exploration]")
        st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
        st.write(" ")
        st.write(" ")
        st.markdown(
            "### :violet[Technologies used :] We have used following technologies in our project Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown(
            "### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
        
    

    image_path = r"C:\Users\user2\OneDrive\Desktop\PhonePe\image 3.jpg"

    image = Image.open(image_path)

        # Resize the image using the PIL resize method
    new_width = 400
    new_height = 350
    image_resized = image.resize((new_width, new_height))

    with col2:
        # Display the resized image in Streamlit
        st.image(image_resized)

#.........................................................[HOME]...............................................................................#
elif select == "Home":
    
    col1,col2= st.columns(2)

    with col1:
            st.subheader(
            "PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
            st.markdown("[DOWNLOAD THE APP NOW](https://www.phonepe.com/app-download/)")
            st.title(':violet[PHONEPE PULSE DATA VISUALISATION]')
            st.subheader(':violet[Phonepe Pulse]:')
            st.write('PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.')  # Add newline after typing text
            st.subheader(':violet[Phonepe Pulse Data Visualisation]:')
            st.write('Data visualization refers to the graphical representation of data using charts, graphs, and other visual elements to facilitate understanding and analysis in a visually appealing manner.'
                'The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.')
    with col2:

        st.image(Image.open(r"C:\Users\user2\OneDrive\Desktop\PhonePe\IMAGE 1.jpg"), width= 600)
#.................................................[Statistical analysis].......................................................................#
elif select == "Statistical analysis":
    
    col1,col2= st.columns(2)

    with col1:

        selected_tab = st.selectbox('Select an analysis type', ["Aggregated Analysis", "Map Analysis", "Top Analysis"],
                                    key='selectbox_analysis_type_1')
        
    # Handle selected tab
    if selected_tab == "Aggregated Analysis":

        with col2:
         
         method = st.selectbox("select the method",["Insurance Analysis", "Transactional Analysis", "User Analysis"], 
                               key='selectbox_method_1')

                #...................................[Insurance Analysis]....................................#
        if method == "Insurance Analysis":
           
            col1,col2= st.columns(2)
            with col1:
           
                years = st.slider("Select The Year",Aggr_insurance["Years"].min(), Aggr_insurance["Years"].max(),Aggr_insurance["Years"].min())
            tac_y= Transaction_amount_count_Yr(Aggr_insurance, years)

            col1,col2= st.columns(2) 
            with col1:
               
                quarters = st.selectbox("Select The Quarter", tac_y["Quarter"].unique())
            Transaction_amount_count_Yr_Q(tac_y, quarters)
               #quarters = st.slider("Select The Quarter",tac_y["Quarter"].min(), tac_y["Quarter"].max(), tac_y["Quarter"].min())
           #Transaction_amount_count_Yr_Q(tac_y, quarters)

               #...................................[Transactional Analysis]....................................#

        elif method == "Transactional Analysis":
           
            col1,col2= st.columns(2)
            with col1:
           
                years = st.slider("Select The Year",Aggr_transaction["Years"].min(), Aggr_transaction["Years"].max(),Aggr_transaction["Years"].min())
            Agg_trn_tac_y= Transaction_amount_count_Yr(Aggr_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Agg_trn_tac_y["States"].unique())
            Aggr_Tran_Transaction_Type(Agg_trn_tac_y, states)

            col1,col2= st.columns(2) 
            with col1:
               
                quarters = st.selectbox("Select The Quarter", Agg_trn_tac_y["Quarter"].unique())
            Agg_trn_tac_y_q= Transaction_amount_count_Yr_Q(Agg_trn_tac_y, quarters)
                #quarters = st.slider("Select The Quarter",Agg_trn_tac_y["Quarter"].min(), Agg_trn_tac_y["Quarter"].max(), Agg_trn_tac_y["Quarter"].min())
            #Agg_trn_tac_y_q= Transaction_amount_count_Yr_Q(Agg_trn_tac_y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Type", Agg_trn_tac_y_q["States"].unique())
            Aggr_Tran_Transaction_Type(Agg_trn_tac_y_q, states)

                #.................................[User Analysis].........................................#

        elif method == "User Analysis":
            
            col1,col2= st.columns(2)
            with col1:
           
                years = st.slider("Select The Year",Aggr_user["Years"].min(), Aggr_user["Years"].max(),Aggr_user["Years"].min())
            Aggr_user_y= Aggregated_user_plot_1(Aggr_user, years)

            col1,col2= st.columns(2) 
            with col1:
               
                quarters = st.selectbox("Select The Quarter", Aggr_user_y["Quarter"].unique())
            Aggr_user_y_q= Aggregated_user_plot_2(Aggr_user_y, quarters)
                #quarters = st.slider("Select The Quarter",Aggr_user_y["Quarter"].min(), Aggr_user_y["Quarter"].max(), Aggr_user_y["Quarter"].min())
            #Aggr_user_y_q= Aggregated_user_plot_2(Aggr_user_y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Aggr_user_y_q["States"].unique())
            Aggregated_user_plot_3(Aggr_user_y_q, states)
        
#.................................................[Map Analysis]...............................................................................#        

    elif selected_tab == "Map Analysis":

        with col2:
         
         method_2 = st.selectbox("select the method",["Insurance Analysis", "Transactional Analysis", "User Analysis"], 
                                 key='selectbox_method_2')


                 #.................................[Insurance Analysis].....................................#

        if method_2 == "Insurance Analysis":
            
            col1,col2= st.columns(2)
            with col1:
           
                years = st.slider("Select The Year",Map_insurance["Years"].min(), Map_insurance["Years"].max(), Map_insurance["Years"].min())
            Map_in_tac_y= Transaction_amount_count_Yr(Map_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State Map_in", Map_in_tac_y["States"].unique())

            Map_Ins_Districts(Map_in_tac_y, states)

            col1,col2= st.columns(2) 
            with col1:
               
                quarters = st.selectbox("Select The Quarter", Map_in_tac_y["Quarter"].unique())
            Map_in_tac_y_q= Transaction_amount_count_Yr_Q(Map_in_tac_y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Type", Map_in_tac_y_q["States"].unique())
            Map_Ins_Districts(Map_in_tac_y_q, states)

                 #.................................[Transactional Analysis].................................#

        elif method_2 == "Transactional Analysis":
            
            col1,col2= st.columns(2)
            with col1:
           
                years = st.slider("Select The Year",Map_transaction["Years"].min(), Map_transaction["Years"].max(), Map_transaction["Years"].min())
            Map_trn_tac_y= Transaction_amount_count_Yr(Map_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State Map_Tr", Map_trn_tac_y["States"].unique())

            Map_Ins_Districts(Map_trn_tac_y, states)

            col1,col2= st.columns(2) 
            with col1:
               
                quarters = st.selectbox("Select The Quarter", Map_trn_tac_y["Quarter"].unique())
            Map_trn_tac_y_q= Transaction_amount_count_Yr_Q(Map_trn_tac_y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Type", Map_trn_tac_y_q["States"].unique())
            Map_Ins_Districts(Map_trn_tac_y_q, states)

                 #.................................[User Analysis].........................................#

        elif method_2 == "User Analysis":
            
            col1,col2= st.columns(2)
            with col1:
           
                years = st.slider("Select The Year",Map_user["Years"].min(), Map_user["Years"].max(), Map_user["Years"].min())
            Map_user_Y= Map_user_plot_1(Map_user, years)

            col1,col2= st.columns(2) 
            with col1:
               
                quarters = st.selectbox("Select The Quarter", Map_user_Y["Quarter"].unique())
            Map_user_Y_Q= Map_user_plot_2(Map_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:

                states = st.selectbox("Select The State", Map_user_Y_Q["States"].unique())
            Map_user_plot_3(Map_user_Y_Q, states)
     
#.................................................[Top Analysis]...............................................................................#

    elif selected_tab == "Top Analysis":
        
        with col2:
          method_3 = st.selectbox("Select the method", ["Insurance Analysis", "Transactional Analysis", "User Analysis"],
                               key='selectbox_method_3')

                #.................................[Insurance Analysis].....................................#

        if method_3 == "Insurance Analysis":
            
            col1,col2= st.columns(2)
            with col1:
           
                years = st.slider("Select The Year",Top_insurance["Years"].min(), Top_insurance["Years"].max(), Top_insurance["Years"].min())
            Top_ins_tac_y= Transaction_amount_count_Yr(Top_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Top_ins_tac_y["States"].unique())
            Top_insurance_plot_1(Top_ins_tac_y, states)

            col1,col2= st.columns(2) 
            with col1:
               
                quarters = st.selectbox("Select The Quarter", Top_ins_tac_y["Quarter"].unique())
            Top_ins_tac_y_q= Transaction_amount_count_Yr_Q(Top_ins_tac_y, quarters)

                #.................................[Transactional Analysis].................................#

        elif method_3 == "Transactional Analysis":
            
            col1,col2= st.columns(2)
            with col1:
           
                years = st.slider("Select The Year",Top_transaction["Years"].min(), Top_transaction["Years"].max(), Top_transaction["Years"].min())
            Top_trn_tac_y= Transaction_amount_count_Yr(Top_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Top_trn_tac_y["States"].unique())
            Top_insurance_plot_1(Top_trn_tac_y, states)

            col1,col2= st.columns(2) 
            with col1:
               
                quarters = st.selectbox("Select The Quarter", Top_trn_tac_y["Quarter"].unique())
            Top_trn_tac_y_q= Transaction_amount_count_Yr_Q(Top_trn_tac_y, quarters)

                #.................................[User Analysis].........................................#

        elif method_3 == "User Analysis":
            
            col1,col2= st.columns(2)
            with col1:
           
                years = st.slider("Select The Year",Top_user["Years"].min(), Top_user["Years"].max(), Top_user["Years"].min())
            Top_user_Y= Top_user_plot_1(Top_user, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Top_user_Y["States"].unique())
            Top_user_plot_2(Top_user_Y, states) 
#....................................................[Top Charts]..............................................................................#
elif select == "Top Charts":
    
    select = st.selectbox(":red[Select the option]",["1. Transaction Amount and Count of Aggregated Insurance",
                                                "2. Transaction Amount and Count of Map Insurance",
                                                "3. Transaction Amount and Count of Top Insurance",
                                                "4. Transaction Amount and Count of Aggregated Transaction",
                                                "5. Transaction Amount and Count of Map Transaction",
                                                "6. Transaction Amount and Count of Top Transaction",
                                                "7. Transaction Count of Aggregated User",
                                                "8. Registered users of Map User",
                                                "9. App opens of Map User",
                                                "10. Registered users of Top User",])

    if select == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader(":violet[TANSACTION AMOUNT of Aggregated Insurance]")
        Top_chart_transaction_amount("aggregated_insurance")

        st.subheader(":violet[TANSACTION COUNT of Aggregated Insurance]")
        Top_chart_transaction_count("aggregated_insurance")

    elif select == "2. Transaction Amount and Count of Map Insurance":

        st.subheader(":violet[TANSACTION AMOUNT of Map Insurance]")
        Top_chart_transaction_amount("map_insurance")

        st.subheader(":violet[TANSACTION COUNT of Map Insurance]")
        Top_chart_transaction_count("map_insurance")

    elif select == "3. Transaction Amount and Count of Top Insurance":

        st.subheader(":violet[TANSACTION AMOUNT of Top Insurance]")
        Top_chart_transaction_amount("top_insurance")

        st.subheader(":violet[TANSACTION COUNT of Top Insurance]")
        Top_chart_transaction_count("top_insurance")

    elif select == "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader(":violet[TANSACTION AMOUNT of Aggregated Transaction]")
        Top_chart_transaction_amount("aggregated_transaction")

        st.subheader(":violet[TANSACTION COUNT of Aggregated Transaction]")
        Top_chart_transaction_count("aggregated_transaction")

    elif select == "5. Transaction Amount and Count of Map Transaction":

        st.subheader(":violet[TANSACTION AMOUNT of Map Transaction]")
        Top_chart_transaction_amount("map_transaction")

        st.subheader(":violet[TANSACTION COUNT of Map Transaction]")
        Top_chart_transaction_count("map_transaction")

    elif select == "6. Transaction Amount and Count of Top Transaction":

        st.subheader(":violet[TANSACTION AMOUNT of Top Transaction]")
        Top_chart_transaction_amount("top_transaction")

        st.subheader(":violet[TANSACTION COUNT of Top Transaction]")
        Top_chart_transaction_count("top_transaction")

    elif select == "7. Transaction Count of Aggregated User":

        st.subheader(":violet[TANSACTION COUNT of Aggregated User]")
        Top_chart_transaction_count("aggregated_user")

    elif select == "8. Registered users of Map User":

        States= st.selectbox(":green[select The State]", Map_user["States"].unique()) 
        st.subheader(":violet[REGISTERED USER of Map User]")
        Top_chart_Registered_user("map_user", States)

    elif select == "9. App opens of Map User":

        States= st.selectbox(":green[select The State]", Map_user["States"].unique()) 
        st.subheader(":violet[APPOPENS of Map User]")
        Top_chart_Appopens("map_user", States)

    elif select == "10. Registered users of Top User":

        st.subheader(":violet[REGISTERED USER of Top User]")
        Top_chart_Registered_users("top_user")