import streamlit as st
from get_answer import get_completion


def run() -> None:
    with st.sidebar:
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[Report an issue](https://blog.dwj601.cn)"

    st.title("💬 Version 1.0.0")
    st.caption("🚀 A streamlit chatbot powered by Tech LLM")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "有什么可以帮助您的吗 🤔"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = get_completion(prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

    # prompt = st.text_input("Please input your question here: :heart:")
    # if st.button("Submit"):
    #     result = get_completion(prompt)
    #     st.write(result)
    # else:
    #     st.write("Please click the button to submit your question.")


if __name__ == "__main__":
    run()
