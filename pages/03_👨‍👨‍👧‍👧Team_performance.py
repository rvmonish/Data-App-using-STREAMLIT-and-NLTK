import pandas as pd
import requests
import warnings as w
w.filterwarnings("ignore")

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

#-----------------------------page setup---------------------------

st.set_page_config(page_title= "Team/Region Report",page_icon=":bar_chart:",layout="wide")

page_layout =st.session_state["page_layout"]
sidebar_style = """
<style>
    [data-testid="stSidebar"]{
        background-color : rgb(0,0,0);
    }
</style>
"""
st.markdown(page_layout,unsafe_allow_html= True)
st.markdown(sidebar_style,unsafe_allow_html= True)

st.sidebar.header("Filter Here")

#-----------------------------------loading resources ----------------------------------#
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_region = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_ptfmt0ts.json")
lottie_team = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_fclga8fl.json")



#--------------------------------import data from st.session----------------------------------------
final_df = st.session_state['df1']


#----------------------------------------end--------------------------------------------------------



#=============================== streamlit create navigation menu =========================#

selected = option_menu(menu_title= None,
                    options=["Region","Team"],
                    icons=[ "map-fill","people-fill"],
                    default_index=0,
                    orientation="horizontal")

#------------------------------------------- Team nav bar-----------------------------------------       
if selected == "Region":

    #================== streamlit filter to select region ==================#

    selected_region = st.sidebar.multiselect("Select Region:",options=final_df["Region"].sort_values().unique(),help="You can select one or more regions",default = "AMER")


    #-----------------------------calculation's for region wise ------------------------------------


    regional_voc_score = round(final_df.query('Region == @selected_region')["Voc_score"].mean(),2)

    stars = ":star:"* int(regional_voc_score) # add stars

    # calculation for total inc cases 

    regional_inc_total = int(final_df.query('Region == @selected_region')["Incident_Number"].sum())

    # calculation for total ast cases

    regional_ast_total = int(final_df.query('Region == @selected_region')["PC_Asset_Task_Number"].sum())

    #calculation for total sc_task

    regional_sc_total = int(final_df.query('Region == @selected_region')["SC_Task_Number"].sum())

    #========================== streamlit region page ================================#
    with st.container():
        buf_1,left,right,buf_2 = st.columns([0.5,4,1,0.5])
        with left:
            st.header(f"Selected Region :")
            st.markdown( f" #### {', '.join(selected_region)} ({stars})")
        with right:
            st_lottie(lottie_region,key="team_animation",height=200)

    st.markdown("-------------")
    with st.container():
    # layer 1 create three columns for agent voc score on the left and performance on the right
        buff_1,col_1,col_2,col_3,col_4,col_5,buff_2 = st.columns([1,1,1,1,1,1,0.5])

        with col_1:
            st.metric(label="Voc Score", value= regional_voc_score)

        with col_2:
            st.metric(label="INC resolved", value= regional_inc_total)

        with col_3:
            st.metric(label="Total AST", value= regional_ast_total)

        with col_4:
            st.metric(label="Total SC Task", value= regional_sc_total)
        
        with col_5:
            st.metric(label="Total case", value= sum([regional_inc_total,regional_ast_total,regional_sc_total]))

        #------------------------------------ region Graphs -----------------------------------------

#------------------------------------------- region nav bar---------------------------------------
else:

    #========================= streamlit filter to select team =====================#
    selected_Team = st.sidebar.multiselect("Select Team:",options=final_df["Team"].sort_values().unique(),help="You can select one or more Teams",default = "US AM")


    #------------------------------------calculation's for region wise ------------------------------------

    team_voc_score = round(final_df.query('Team == @selected_Team')["Voc_score"].mean(),2)

    stars = ":star:"* int(team_voc_score) # add stars

    # calculation for total inc cases 

    team_inc_total = int(final_df.query('Team == @selected_Team')["Incident_Number"].sum())

    # calculation for total ast cases

    team_ast_total = int(final_df.query('Team == @selected_Team')["PC_Asset_Task_Number"].sum())

    #calculation for total sc_task

    team_sc_total = int(final_df.query('Team == @selected_Team')["SC_Task_Number"].sum())

    #========================== streamlit Team page ================================#

    with st.container():
        buff_1,left,right,buff_2 = st.columns([0.5,4,1,0.5])
        with left:
            st.header(f"Selected Team :")
            st.markdown( f" #### {', '.join(selected_Team)} ({stars})")
        with right:
            st_lottie(lottie_team,key="team_animation",height=200)

    st.markdown("-------------")
    with st.container():
    # layer 1 create three columns for agent voc score on the left and performance on the right
        buff_1,col_1,col_2,col_3,col_4,col_5,buff_2 = st.columns([1,1,1,1,1,1,0.5])

        with col_1:
            st.metric(label="Voc Score", value= team_voc_score)

        with col_2:
            st.metric(label="INC resolved", value= team_inc_total)

        with col_3:
            st.metric(label="Total AST", value= team_ast_total)

        with col_4:
            st.metric(label="Total SC Task", value= team_sc_total)
        
        with col_5:
            st.metric(label="Total case", value= sum([team_inc_total,team_ast_total,team_sc_total]))

        #-------------------------------------- Team graphs----------------------------------------

#--------------------------------------------- end -----------------------------------------------

st.markdown("---")     