import streamlit as st
from openai import OpenAI
from utils.ip_checker import get_remote_ip
from openai.types.beta.assistant_stream_event import (
    ThreadMessageCompleted,
    ThreadCreated,
    ThreadRunFailed,
)
from utils.helper_util import remove_text_inside_legacy_brackets


def app(session_state):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    assistant_id = 'asst_ZRXTRNO3mtSwoYUpiwmzEUiE'

    ip = get_remote_ip()

    with st.sidebar:
        st.info(f"Ip address: {ip}")

    st.info(
        f"{session_state['company']} Q&A session will be reset if you leave the page",
        icon="ℹ️",
    )

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    assistant = client.beta.assistants.retrieve(assistant_id)

    def run_thread(thread_id, assistant_id):
        run = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id, stream=True
        )
        for event in run:
            if isinstance(event, ThreadCreated):
                text_value = remove_text_inside_legacy_brackets(
                    event.data.content[0]['text']['value']
                )
                yield text_value
            elif isinstance(event, ThreadMessageCompleted):
                text_value = remove_text_inside_legacy_brackets(
                    event.data.content[0].text.value
                )
                yield text_value
            if isinstance(event, ThreadRunFailed):
                print(event)
                break

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(
        f"Ask me any question about annual reports of {session_state['company']} , including 3-years financial data and latest news"
    ):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            thread = client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": st.session_state.messages[-1]["content"]
                                + f" for company {session_state['company']}"
                                + "",
                            }
                        ],
                    }
                ]
            )

            response = st.write_stream(
                run_thread(thread_id=thread.id, assistant_id=assistant.id)
            )
        st.session_state.messages.append({"role": "assistant", "content": response})
