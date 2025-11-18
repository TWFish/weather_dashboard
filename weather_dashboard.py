import requests
import streamlit as st
import pandas as pd

st.title("台灣氣象資料 Dashboard")
LOCATION = st.selectbox("選擇城市", ["Taipei","Taichung","Kaohsiung"])

ulr = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-EE0FA5AF-16E7-4E77-80A0-97172349E1A5&locationName=%E8%87%BA%E5%8C%97%E5%B8%82'

data = requests.get(ulr).json()
location = data['records']['location'][0]
st.subheader(f"{location['locationName']}36小時預報")

for element in location['weatherElement']:
    name = element['elementName']
    value = element['time'][0]['parameter']['parameterName']
    st.write(f"{name}:{value}")
