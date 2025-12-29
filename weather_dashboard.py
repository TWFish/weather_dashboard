import requests
import streamlit as st
import google.generativeai as genai
import pandas as pd

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3-flash-preview')

st.title("台灣氣象與 AI 穿搭推薦")
LOCATION = st.selectbox("選擇城市", ["臺北","臺中","高雄"])

url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-EE0FA5AF-16E7-4E77-80A0-97172349E1A5'

# --- 這裡之前是 API 請求 (requests.get) ---
data = requests.get(url, verify=False).json()
all_locations = data['records']['location']

# 【覆蓋開始】這一段取代你原本 location = data...[0] 的位置
location_data = next((item for item in all_locations if item['locationName'] == LOCATION), None)

if location_data:
    st.subheader(f"{location_data['locationName']} 36小時預報")
    
    weather_summary = []

    for element in location_data['weatherElement']:
        name = element['elementName']
        value = element['time'][0]['parameter']['parameterName']
        # 這裡加個 .get 以防有些欄位沒有單位
        unit = element['time'][0]['parameter'].get('parameterUnit', '') 
        
        # 轉換單位呈現方式 (選配，讓畫面更漂亮)
        if unit == "C": unit = "°C"
        if unit == "百分比": unit = "%"
        
        display_text = f"{name}: {value}{unit}"
        st.write(display_text)
        weather_summary.append(display_text)
# 【覆蓋結束】

weather_summary = f"地點：{location['locationName']}，預報內容：{name}:{value}..."

if st.button("生成今日穿搭建議"):
    # 設定 Prompt
    prompt = f"根據以下氣象資料：'{weather_summary}'。請給予今天的穿搭建議，並解釋原因。"
    
    # 呼叫 Gemini API
    response = model.generate_content(prompt)
    
    st.subheader("AI 穿搭推薦：")
    st.write(response.text)
