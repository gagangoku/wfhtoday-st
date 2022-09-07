import json
import os
import random
import time

import streamlit as st

from utils import getDeviceIdBase, styleOverrideForButton, runMysqlQuery, initMysqlConnection

COMMUTE_MODE_WFH = 1
COMMUTE_MODE_OFFICE = 2
ST_MEMO_DICT = {'show_spinner': True, 'suppress_st_warning': True}
ST_CACHE_DICT = {'show_spinner': False, 'suppress_st_warning': True, 'allow_output_mutation': True}
WFH_SUCCESS = [
    'Woo hooo. More power to you man !',
]
OFFICE_SUCCESS = [
    'Woo hooo. More power to you man !',
]
SPINNER_TEXTS = [
    'Pouring awesomeness 🫖',
    'Aligning the stars 🪐',
    'Slaying the monsters 🪓',
    'Making peace with aliens 👽',
    'Counting the hair on human head 👩',
    'Conquering new planets 🚀',
]
DRIVING_TEXTS = [
    'sailing ⛵',
    'driving 🚗',
    'flying 🚀',
]


@st.cache(**ST_CACHE_DICT)
def readBlrAreas(file):
    with open(file, encoding="utf-8") as fp:
        contents = fp.read()
        blrAreas = json.loads(contents)
        blrAreas.insert(0, '')
        return blrAreas

@st.cache(**ST_CACHE_DICT)
def readFunNames(file):
    with open(file, encoding="utf-8") as fp:
        contents = fp.read()
        return json.loads(contents)

def hideMainMenu():
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-hi6a2p {padding-top: 0rem;}
    .block-container {padding-top: 2rem;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def captureInteraction(residence, office, commuteMode, _conn):
    with st.spinner(SPINNER_TEXTS[random.randint(0, len(SPINNER_TEXTS) - 1)]):
        names = readFunNames('data/names.json')
        name = names[random.randint(0, len(names) - 1)]
        deviceId, _ = getDeviceIdBase()
        print ('name, deviceId, residence, office: ', ','.join([name, deviceId, residence, office]))

        timestamp = round(time.time() * 1000)
        query = 'insert into wfhtoday(name, deviceId, residence, office, timestamp, commuteMode) values("{}", "{}", "{}", "{}", {}, {})'.format(name, deviceId, residence, office, timestamp, commuteMode)
        res = runMysqlQuery(query, _conn, False)
        print ('res: ', res)


# @st.experimental_memo(ttl=300)
def getRecentActivity(_conn):
    query = 'select name, residence, office, timestamp, commuteMode from wfhtoday order by timestamp desc limit 100'
    res = runMysqlQuery(query, _conn, True)
    print ('res: ', res)
    data = [{'name': x[0], 'residence': x[1], 'office': x[2], 'timestamp': x[3], 'commuteMode': x[4]} for x in res]

    query = 'select count(*) from wfhtoday'
    res = runMysqlQuery(query, _conn, True)
    print ('res: ', res)
    numRows = res[0][0]
    return data, numRows


def main():
    random.seed(round(time.time() * 1000))
    st.set_page_config('WFH Today', '', layout='centered')
    hideMainMenu()
    styleOverrideForButton()
    st.markdown("""
# WFH Today
<div style="margin-top: -10px; font-size: 14px; color: rgba(253, 151, 31);">Inspired by the recent hardships of a daily commuter.</div>
<br/>

This page is dedicated to all the commuters out there going to office despite the Bangalore floods.

- Worried about water logging on your route ?
- Wanna know who else is working from home today ?
<div style="color: rgba(253, 151, 31); margin-top: -2px;">Read on ...</div>
<br/>
Some day I plan on hooking up <b>drones</b> 🚀🚀 to surveil certain pockets of the city to identify chokepoints / flooded regions.
It would give commuters a sense of what they're in for today (and help rescue operations, but that's later).

# 
Till then, tell us what you're upto today !
<br/><br/>
    """, unsafe_allow_html=True)

    blrAreas = readBlrAreas('data/blr-areas.json')

    col1, col2 = st.columns(2)
    with col1:
        residence = st.selectbox('I stay in', blrAreas)
    with col2:
        office = st.selectbox('My office is in', blrAreas)

    col1, col2, _ = st.columns([1.6, 3, 3])
    with col1:
        wfhToday = st.button('I\'m WFH today !')
    with col2:
        officeToday = st.button('I\'m going to office today !')

    _conn = initMysqlConnection()
    if wfhToday:
        captureInteraction(residence, office, COMMUTE_MODE_WFH, _conn)
        st.success(WFH_SUCCESS[random.randint(0, len(WFH_SUCCESS) - 1)])
    if officeToday:
        captureInteraction(residence, office, COMMUTE_MODE_OFFICE, _conn)
        st.success(OFFICE_SUCCESS[random.randint(0, len(OFFICE_SUCCESS) - 1)])


    images = list(filter(lambda x: 'ignore' not in x, os.listdir('data/images')))
    img = images[random.randint(0, len(images) - 1)]
    st.markdown("""
    <br/><br/>

    #### Enjoy a productive day. Here's a special meme for ya !
    
    """, unsafe_allow_html=True)
    st.image('data/images/' + img)

    st.markdown("""
    <div style="color: rgb(253, 151, 31);">{}</div>
    <br/><br/>

    ### Who else is out there slogging today !
    """.format(img), unsafe_allow_html=True)

    data, numRows = getRecentActivity(_conn)
    for d in data:
        office = d['office'] or '-'
        residence = d['residence'] or '-'
        if d['commuteMode'] == COMMUTE_MODE_WFH:
            st.markdown("""
            ❤️ <span style="color: pink;">{}</span> is <span style="color: rgb(253, 151, 31);">WFH</span> today ({} -> {})
            """.format(d['name'], residence, office), unsafe_allow_html=True)
        else:
            mode = DRIVING_TEXTS[random.randint(0, len(DRIVING_TEXTS) - 1)]
            st.markdown("""
            👽 <span style="color: pink;">{}</span> is <span style="color: rgb(253, 151, 31);">{}</span> to office today ({} -> {})
            """.format(d['name'], mode, residence, office), unsafe_allow_html=True)

    st.markdown('<br/><br/>', unsafe_allow_html=True)
    st.markdown('---', unsafe_allow_html=True)
    st.markdown('<br/><br/>', unsafe_allow_html=True)
    with st.expander('DEBUG info'):
        st.write(images)


print ('In Home.py')
main()
