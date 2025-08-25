import streamlit as st
import requests

st.title("RAG Chatbot")

question = st.text_input("Nhập câu hỏi:")
if st.button("Gửi"):
    res = requests.post(
        "https://<your-ngrok-url>.ngrok.io/v1/chat",  # cập nhật đúng URL
        json={"question": question}
    )
    if res.status_code == 200:
        st.write("💬 Trả lời:", res.json()["response"])
    else:
        st.error("Lỗi:", res.json())
