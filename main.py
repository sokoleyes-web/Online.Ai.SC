import streamlit as st
from openai import OpenAI

# 1. Настройка вкладки браузера
st.set_page_config(page_title="ОНЛАЙН", page_icon="logo.png", layout="wide")

# 2. Заголовок и ЛОГОТИП
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=80)  # <-- Твой логотип!
with col2:
    st.title("ОНЛАЙН")
    st.caption("Твой персональный AI-ассистент")

# 3. Подключение к API
client = OpenAI(
    api_key=st.secrets.get("QWEN_API_KEY", ""),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

if not client.api_key:
    st.error("⚠️ API-ключ не найден.")
    st.stop()

# 4. История чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Вывод сообщений
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Ввод и ответ
if prompt := st.chat_input("Напиши сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            response = client.chat.completions.create(
                model="qwen-plus",
                messages=[
                    {"role": "system", "content": "Ты — AI-ассистент ОНЛАЙН. Отвечай чётко и кратко."}
                ] + st.session_state.messages,
                stream=True
            )
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"❌ Ошибка: {str(e)}")
