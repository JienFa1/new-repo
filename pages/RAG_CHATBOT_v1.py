import streamlit as st
import requests

st.set_page_config(layout="wide") 

# Ngrok API endpoint
flask_api_url = "https://e574-34-124-133-84.ngrok-free.app/v1/chat"
st.markdown(f"API endpoint: [{flask_api_url}]({flask_api_url})")

# Khởi tạo lịch sử chat
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

# Hiển thị lịch sử chat
for message in st.session_state.chat_display:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nhận input người dùng
if prompt := st.chat_input(key="chat", placeholder="May I help you?"):
    # Hiển thị message của user
    st.session_state.chat_display.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi request đến Flask backend
    payload = {
        "question": prompt,
        "stream": True  # 👈 Thêm flag để backend hiểu rõ nếu muốn
    }

    # Nhận stream response từ Flask
    with st.chat_message("assistant"):
        streamed_content = ""
        response_placeholder = st.empty()

        try:
            response = requests.post(flask_api_url, json=payload, stream=True)

            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        streamed_content += chunk
                        response_placeholder.markdown(streamed_content)
                # Lưu vào chat history
                st.session_state.chat_display.append({"role": "assistant", "content": streamed_content})
            else:
                st.error(f"Lỗi từ API: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Lỗi kết nối: {str(e)}")
