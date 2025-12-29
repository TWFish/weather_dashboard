import requests
import streamlit as st
import google.generativeai as genai
import pandas as pd

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3-flash-preview')
except Exception as e:
    st.error(f"Gemini 配置錯誤: {e}")

st.title("台灣氣象與 AI 穿搭推薦")

LOCATION = st.selectbox("選擇城市", ["臺北市", "臺中市", "高雄市", "嘉義縣"])

url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-EE0FA5AF-16E7-4E77-80A0-97172349E1A5'

try:
    data = requests.get(url, verify=False).json()
    all_locations = data['records']['location']

    location_data = next((item for item in all_locations if item['locationName'] == LOCATION), None)

    if location_data:
        st.subheader(f"{location_data['locationName']} 36小時預報")
        
        display_list = []

        for element in location_data['weatherElement']:
            name = element['elementName']
            value = element['time'][0]['parameter']['parameterName']
            unit = element['time'][0]['parameter'].get('parameterUnit', '') 
            
            if unit == "C": unit = "°C"
            if unit == "百分比": unit = "%"
            
            display_text = f"{name}: {value}{unit}"
            st.write(display_text)
            display_list.append(display_text)

        weather_context = f"地點：{location_data['locationName']}，詳細預報資訊如下：{', '.join(display_list)}"

        if st.button("生成今日穿搭建議"):
            prompt = f"你是一位穿搭專家。根據以下氣象資料：'{weather_context}'。請給予具體的穿搭建議（包含衣服件數、是否帶傘、材質建議），並解釋原因。"
            
            with st.spinner('AI 正在根據氣象數據思考穿搭...'):
                response = model.generate_content(prompt)
                st.subheader("👕 AI 穿搭推薦：")
                st.info(response.text)
    else:
        st.warning(f"在 API 中找不到「{LOCATION}」的資料，請確認名稱是否正確。")

except Exception as e:
    st.error(f"連線氣象局 API 發生錯誤: {e}")
