import requests
import streamlit as st
import google.generativeai as genai
import pandas as pd

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.title("台灣氣象與 AI 穿搭推薦")
LOCATION = st.selectbox("選擇城市", ["臺北","臺中","高雄"])

ulr = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-EE0FA5AF-16E7-4E77-80A0-97172349E1A5'

data = requests.get(ulr,verify=False).json()
location = data['records']['location'][0]
st.subheader(f"{location['locationName']}36小時預報")

for element in location['weatherElement']:
    name = element['elementName']
    value = element['time'][0]['parameter']['parameterName']
    st.write(f"{name}:{value}")

weather_summary = f"地點：{location['locationName']}，預報內容：{name}:{value}..."

if st.button("生成今日穿搭建議"):
    # 設定 Prompt
    prompt = f"根據以下氣象資料：'{weather_summary}'。請給予今天的穿搭建議，並解釋原因。"
    
    # 呼叫 Gemini API
    response = model.generate_content(prompt)
    
    st.subheader("AI 穿搭推薦：")
    st.write(response.text)
