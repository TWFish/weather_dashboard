import requests
import streamlit as st
import pandas as pd

st.title("台灣氣象資料 Dashboard")
LOCATION = st.selectbox("選擇城市", ["臺北","臺中","高雄"])

ulr = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-EE0FA5AF-16E7-4E77-80A0-97172349E1A5'

data = requests.get(ulr,verify=False).json()
location = data['records']['location'][0]
st.subheader(f"{location['locationName']}36小時預報")

for element in location['weatherElement']:
    name = element['elementName']
    value = element['time'][0]['parameter']['parameterName']
    st.write(f"{name}:{value}")
