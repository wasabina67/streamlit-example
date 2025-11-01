import streamlit as st
from openai import OpenAI


def main():
    st.set_page_config(
        page_title="Streamlit example",
        page_icon=None,
        layout="wide",
    )
    st.title("Streamlit example")

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="api_key",
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("メッセージを入力してください"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                stream = client.chat.completions.create(
                    model="gpt-oss:20b",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )

                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

            except Exception as e:
                full_response = f"エラーが発生しました: {str(e)}"
                message_placeholder.markdown(full_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )


if __name__ == "__main__":
    main()
