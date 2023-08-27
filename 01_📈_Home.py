from re import U
from typing import Final
import pandas as pd
import requests
import warnings as w
w.filterwarnings("ignore")

import streamlit as st
from streamlit_lottie import st_lottie,st_lottie_spinner


#----- modifying html/css and style of streamlit app--------------------------

st.set_page_config(page_title= "📈Performance Report",page_icon=":bar_chart:",layout="wide")

page_layout = """
<style>
    footer{
        visibility :hidden;
    }
    .css-912zdv {
        visibility :hidden;
    }
    .css-fgfsvk::before {
    background-image : none;
    }
    .css-fgfsvk::after {
    background-image : none;
    }
    .css-18e3th9 {
        padding-top: 20px;
        padding-right: 30px;
        padding-bottom: 50px;
        padding-left: 30px;
    }
</style>
"""
sidebar_style ="""
<style>
    [data-testid="stSidebar"]{
        background-image: url("https://images.unsplash.com/photo-1512551980832-13df02babc9e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1964&q=80");
        background-position: left top;
        background-attachment: scroll;
        background-size: cover;
        background-repeat: no-repeat;
    }
</style>
"""
st.markdown(page_layout,unsafe_allow_html= True)
st.markdown(sidebar_style,unsafe_allow_html= True)

st.title("Performance Report :bar_chart:")
st.markdown("-----")


#--------------------------------page setup---------------------------------------------


#-----------------------------------loading resources ----------------------------------#
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_loading = load_lottieurl("https://assets1.lottiefiles.com/private_files/lf30_icqbrqxr.json")
web_app = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_ye2v3dmd.json")

#-------------------------------- Read,clean and analysing_data  -----------------------------#

#Reading data 

with st_lottie_spinner(lottie_loading,height=300,key="loading_animation"):
    @st.experimental_singleton
    def analysing_data():
        sc_task_read = pd.read_excel("data/case.xlsx",sheet_name = 0,header = 3)
        ast_read = pd.read_excel("data/case.xlsx",sheet_name = 1,header =3)
        inc_resolved_read = pd.read_excel("data/case.xlsx",sheet_name =2,header = 3)
        inc_csat_read = pd.read_excel("data/csat.xlsx",sheet_name = 0,header =3)
        ast_csat_read = pd.read_excel("data/csat.xlsx",sheet_name =2,header =3)
        agent_table= pd.read_excel("data/agents.xlsx",)


        #function to drop first column and remove space in column headers
        def drop_and_rename_column(data_frame):
            df = data_frame.iloc[:,1:]
            df.columns =[column.replace(" ", "_") for column in df.columns]
            return df

        # step 1 :remove first column and fix column headers

        sc_task_1 = drop_and_rename_column(sc_task_read)
        ast_1 = drop_and_rename_column(ast_read)
        inc_resolved_1 = drop_and_rename_column(inc_resolved_read)
        inc_csat_1 = drop_and_rename_column(inc_csat_read)
        ast_csat_1 = drop_and_rename_column(ast_csat_read)

        # step 2 remove duplicates based on unique column

        sc_task = sc_task_1.drop_duplicates("SC_Task_Number")
        ast = ast_1.drop_duplicates("PC_Asset_Task_Number")
        inc_resolved = inc_resolved_1.drop_duplicates("Incident_Number")
        inc_csat = inc_csat_1.drop_duplicates("Incident_Number")
        ast_csat = ast_csat_1.drop_duplicates("PC_Asset_Task_Number")

        ast["User_Id"] = ast["PC_Asset_Task_Assigned_To"].str.extract('\((.*)\)',expand=True)
        sc_task["User_Id"] = sc_task["SC_Task_Assigned_To"].str.extract('\((.*)\)',expand=True)

        #----------------------------------pivot and calculation-------------------------------

        #voc_score from inc_csat df ==>

        voc_pivot = pd.pivot_table(inc_csat,index =["Incident_Assigned_To"], values =["Incident_Number","Incident_Survey_Average_(Q1)_(Experience)"],aggfunc={"Incident_Number" : "count","Incident_Survey_Average_(Q1)_(Experience)":"mean"})

        voc_pivot_table = pd.DataFrame(voc_pivot.to_records())

        voc_pivot_table.rename(columns = {'Incident_Assigned_To':'User_Id','Incident_Number':'Number_of_surveys','Incident_Survey_Average_(Q1)_(Experience)':'Voc_score'}, inplace = True)


        # inc_cases from inc_resolved df ==>

        inc_case_pivot = pd.pivot_table(inc_resolved,index=["Incident_Assigned_To"], values=["Incident_Number"],aggfunc={"Incident_Number" : "count"})

        inc_case_pivot_table = pd.DataFrame(inc_case_pivot.to_records())

        inc_case_pivot_table.rename(columns = {'Incident_Assigned_To':'User_Id'}, inplace = True)

        #ast cases from ast df ==>

        ast_case_pivot = pd.pivot_table(ast,index=["User_Id"],values=["PC_Asset_Task_Number"],aggfunc={"PC_Asset_Task_Number" : "count"})

        ast_case_pivot_table = pd.DataFrame(ast_case_pivot.to_records())

        #sc_task from sc_task df ==>  

        sc_task_pivot = pd.pivot_table(sc_task, index=["User_Id"],values=["SC_Task_Number"],aggfunc={"SC_Task_Number" : "count"})

        Sc_task_pivot_table = pd.DataFrame(sc_task_pivot.to_records())

        #final df by merging all the tables ==>

        final_df = agent_table.merge(inc_case_pivot_table,on='User_Id',how="left").merge(ast_case_pivot_table,on='User_Id',how="left").merge(Sc_task_pivot_table,on='User_Id',how="left").merge(voc_pivot_table,on='User_Id',how="left")

        return final_df
    
    final_df = analysing_data()

    st.session_state['df1'] = final_df
    st.session_state['page_layout'] = page_layout

#-------------------------------------streamlit code--------------------------------------

with st.container():

    buff_1,left_1,left_2,right= st.columns([0.25,0.5,0.5,1])

    with left_1:
        st.markdown("#")
        st.markdown("#")
        st.metric(label="No of Agent's", value=final_df['User_Id'].count())
        st.metric(label="Total AST", value=int(final_df['PC_Asset_Task_Number'].sum()))


    with left_2:
        st.markdown("#")
        st.markdown("#")
        st.metric(label="Total INC", value=int(final_df["Incident_Number"].sum()))
        st.metric(label="Total SC Tasks", value=int(final_df["SC_Task_Number"].sum()))
    
    with right:
        st.markdown("#")
        st_lottie(web_app,key="web_app",height= 200)


st.markdown("---------")
with st.container():
     st.markdown(
        """
        ### Usage
        To the left, is a dropdown main menu for navigating to 
        each page in the *Performance Report* :
        - **Home Page:** We are here!
        - **Individual Performance:** Search for individual and analyze performance for each agent(voc scores,number of INC, AST, SC_Task's handled by the agent).
        - **Team Performance:** Explore Region Wise or Team wise performance by selecting particular region or Team .
        - **Graphs and Table:** View chart or tabular Data which shows number of different cases handled, based on region and corresponding team in the region.
        """
    )



    

        

