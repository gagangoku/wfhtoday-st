import ssl
import uuid

import mysql.connector
import streamlit as st
from streamlit_ws_localstorage import injectWebsocketCode

KEY_DEVICE_ID = 'deviceId'

def getDeviceIdBase():
    uid = str(uuid.uuid1())
    code = injectWebsocketCode('linode.liquidco.in', uid)
    deviceId = st.session_state.deviceId if 'deviceId' in st.session_state else code.getLocalStorageVal(key=KEY_DEVICE_ID)
    print ('got saved deviceId: ', deviceId)
    if not deviceId:
        code.setLocalStorageVal(key=KEY_DEVICE_ID, val=uid)
        deviceId = uid
        st.session_state.deviceId = deviceId
        print ('saved deviceId: ', deviceId)
    return deviceId, uid

def styleOverrideForButton():
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: rgb(253, 151, 31);
        border-color: rgb(253, 151, 31);
        color: rgb(0, 0, 0);
    }
    div.stButton > button:first-child:hover {
        background-color: rgb(0, 0, 0);
        border-color: rgb(253, 151, 31);
        color: rgb(253, 151, 31);
    }
    </style>""", unsafe_allow_html=True)


# Initialize connection.
# @st.experimental_memo(ttl=300)
@st.experimental_singleton
def initMysqlConnection():
    return mysql.connector.connect(**st.secrets["mysql"])

# Perform query.
# @st.experimental_memo(ttl=300)
def runMysqlQuery(query, _conn, returnResult):
    with _conn.cursor(buffered=True) as cur:
        cur.execute(query)
        _conn.commit()
        if returnResult:
            return cur.fetchall()
