import streamlit as st
from openai import OpenAI

# Настройка страницы
st.set_page_config(page_title="Qwen Studio Lite", page_icon="🤖", layout="wide")
st.title("🤖 Qwen Studio Lite")
st.caption("Облачный чат на базе Qwen API")

# Подключение к API (ключ берётся из безопасного хранилища Streamlit)
client = OpenAI(
    api_key=st.secrets.get("QWEN_API_KEY", ""),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

if not client.api_key:
    st.error("⚠️ API-ключ не найден. Добавь его в настройки Streamlit Cloud.")
    st.stop()

# История сообщений
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение диалога
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Поле ввода
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
                    {"role": "system", "content": "Ты — умный ассистент в стиле Qwen Studio. Отвечай чётко, используй markdown."}
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
            st.error(f"❌ Ошибка API: {str(e)}")
