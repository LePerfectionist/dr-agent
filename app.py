# import streamlit as st
# from dotenv import load_dotenv
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chat_models import ChatOpenAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.callbacks import get_openai_callback
# import os
# import json
# from openai import OpenAI

# from file_processing import get_responses
# from file_processing import extract_text

# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

# if not openai_api_key:
#     st.error("🔴 OpenAI API key not found. Please set the OPENAI_API_KEY in your .env file and restart the app.")



# # Mockup: Enhanced DR Assistant Interface

# # Title and Sidebar Configuration
# logo_url = "https://digitalprocurement.dib.ae/images/logo.png"
# st.set_page_config(page_title="DR Assistant", page_icon=logo_url)

# st.image(logo_url, width=200)
# st.title("Generative AI-Powered Disaster Recovery Assistant")
# st.sidebar.title("DR Engineer Interface")
# st.sidebar.subheader("Steps to Execute DR Procedures")

# # Customizing Theme
# st.markdown(
#     """
#     <style>
#     body {
#         background-color: #FFFFFF;
#         color: #004080;
#     }
#     .sidebar .sidebar-content {
#         background-color: #F0F8FF;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Upload Section
# st.sidebar.header("Upload Run Books")
# uploaded_files = st.sidebar.file_uploader(
#     "Upload Run Books (Word Documents)", type=["docx", "pdf"], accept_multiple_files=True
# )

# # Placeholder to store uploaded run book names
# if "run_books" not in st.session_state:
#     st.session_state["run_books"] = []

# # Display Uploaded Run Books
# if uploaded_files:
#     for file in uploaded_files:
#         if file.name not in st.session_state["run_books"]:
#             st.session_state["run_books"].append(file.name)

# st.sidebar.write("**Uploaded Run Books:**")
# st.sidebar.write(st.session_state["run_books"])

# # Mock System and DR Engineer Selection
# st.header("System and DR Configuration")

# # Placeholder for systems (based on mock data extracted from run books)
# systems = {
#     "Payments (EPH)": ["Primary", "Secondary"],
#     "Core Banking (Temenos)": ["Primary", "Secondary"],
#     "Cards (Vision Plus+)": ["Primary", "Secondary"],
# }

# system_choices = {}
# # Create a form to allow selection for each system
# with st.form(key="dr_system_form"):
#     st.write("Select Primary or Secondary for each System:")
#     for system, options in systems.items():
#         system_choices[system] = st.radio(system, options, index=0)

#     submit_button = st.form_submit_button(label="Generate Drill Steps")

# # prompt = "Attached is a Disaster Recovery Runbook for a core banking application, for testing as well as actual failure cases. Many components (like core, payments, cards, etc) primary and secondary (backup) are switched on or off to see if it's linking correctly and instantly. The following sytems are in place:\n"
# # for system in system_choices:
# #     prompt += f"{system} : {system_choices[system]}\n"
# # prompt += "Give a detail step by step checklist that this person needs to do to perform test from start to end, including relevant scripts and conditions"

# prompt = "I want to do a disaster recovery scripting from the persona of DR engineer. I want to keep the"
# system_selected = ""
# for system in system_choices:
#     prompt += f"{system} systems in the {system_choices[system]} node,"
#     if system_choices[system] == "Secondary":
#         system_selected = system

# prompt += f"as a part of my DR drill.\nConsider the dependent systems mentioned in the {system_selected} runbook. Give me one output as a steps that I need to perform as a DR engineer with the scripts that I will require to run to validate the scenario and to change from primary to secondary based on the run book uploaded with the prompt during a DR drill"
# prompt += f"Consider the dependent applications from {system_selected} runbook, and use IP, hostname and port details from the dependent systems runbooks to form the scripts, as a part of the validating the dependent systems. Factor it as a part of the steps.  Also add communication spocs from the document and get the details. Add the IP, hostname and port details from the documents." #Generate a table with IP address, host name, and port for both primary and secondary for all the applications from the runbooks"
# # Generate Steps if form is submitted
# prompt_1 = f"as a part of my DR drill.\nConsider the dependency mapping systems mentioned in the {system_selected} runbook. Consider the dependent applications from {system_selected} runbook, and use IP, hostname and port details from the EPH Primary instance, EPH Secondary instance, and CoreBanking Primary instance, CoreBanking Secondary instance IP addresses to form the specific scripts, as a part of the validating the dependent systems. Do not generate generic scripts. Factor it as a part of the steps"
# if submit_button:
#     st.success("Configuration Submitted Successfully!")

#     st.header("Generated DR Drill Steps")

#     # response = get_responses(uploaded_files, [prompt])[prompt]

#     # st.write(response)

#     # prompt_1 = f"as a part of my DR drill.\nConsider the dependent systems mentioned in the {system_selected} runbook. Consider the dependent applications from {system_selected} runbook, and use IP, hostname and port details from the EPH Primary instance, EPH Secondary instance, and CoreBanking Primary instance, and CoreBanking Secondary instance sections to form the scripts, as a part of the validating the dependent systems. Factor it as a part of the steps"

#     st.subheader("Validating Dependencies")
#     # st.write(get_responses(uploaded_files, [prompt])[prompt])

#     openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#     completion = openai_client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": prompt_1},
#                 {"role": "user", "content": extract_text(uploaded_files)}
#             ],
#             max_tokens=4096,
#             temperature=0.6,
#             frequency_penalty=0.0,
#             presence_penalty=0.0,
#         )
    
#     response = completion.choices[0].message.content.strip()

#     st.write(response)

#     # Download Steps as .txt file
#     st.download_button(
#         label=f"Download Steps",
#         data=response,
#         file_name=f"DR_Steps.txt",
#         mime="text/plain",
#     )

# # Footer Section
# st.sidebar.markdown("---")
# st.sidebar.write("Powered by Streamlit, OpenAI, and FAISS.")

# app.py
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os
import json
from openai import OpenAI

from file_processing import get_responses, extract_text, get_chatbot_chain

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("🔴 OpenAI API key not found. Please set the OPENAI_API_KEY in your .env file and restart the app.")

# Title and Sidebar Configuration
logo_url = "https://digitalprocurement.dib.ae/images/logo.png"
st.set_page_config(page_title="DR Assistant", page_icon=logo_url)

st.image(logo_url, width=200)
st.title("Generative AI-Powered Disaster Recovery Assistant")
st.sidebar.title("DR Engineer Interface")
st.sidebar.subheader("Steps to Execute DR Procedures")

# Customizing Theme
st.markdown(
    """
    <style>
    body {
        background-color: #FFFFFF;
        color: #004080;
    }
    .sidebar .sidebar-content {
        background-color: #F0F8FF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Upload Section
st.sidebar.header("Upload Run Books")
uploaded_files = st.sidebar.file_uploader(
    "Upload Run Books (Word Documents)", type=["docx", "pdf", "txt"], accept_multiple_files=True
)

# Placeholder to store uploaded run book names
if "run_books" not in st.session_state:
    st.session_state["run_books"] = []

# Display Uploaded Run Books
if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state["run_books"]:
            st.session_state["run_books"].append(file.name)

st.sidebar.write("**Uploaded Run Books:**")
st.sidebar.write(st.session_state["run_books"])

# Mock System and DR Engineer Selection
st.header("System and DR Configuration")

# Placeholder for systems (based on mock data extracted from run books)
systems = {
    "Payments (EPH)": ["Primary", "Secondary"],
    "Core Banking (Temenos)": ["Primary", "Secondary"],
    "Cards (Vision Plus+)": ["Primary", "Secondary"],
}

system_choices = {}
# Create a form to allow selection for each system
with st.form(key="dr_system_form"):
    st.write("Select Primary or Secondary for each System:")
    for system, options in systems.items():
        system_choices[system] = st.radio(system, options, index=0)

    submit_button = st.form_submit_button(label="Generate Drill Steps")

prompt = "I want to do a disaster recovery scripting from the persona of DR engineer. I want to keep the"
system_selected = ""
for system in system_choices:
    prompt += f"{system} systems in the {system_choices[system]} node,"
    if system_choices[system] == "Secondary":
        system_selected = system

prompt += f"as a part of my DR drill.\nConsider the dependent systems mentioned in the {system_selected} runbook. Give me one output as a steps that I need to perform as a DR engineer with the scripts that I will require to run to validate the scenario and to change from primary to secondary based on the run book uploaded with the prompt during a DR drill"
prompt += f"Consider the dependent applications from {system_selected} runbook, and use IP, hostname and port details from the dependent systems runbooks to form the scripts, as a part of the validating the dependent systems. Factor it as a part of the steps.  Also add communication spocs from the document and get the details. Add the IP, hostname and port details from the documents."

prompt_1 = f"as a part of my DR drill.\nConsider the dependency mapping systems mentioned in the {system_selected} runbook. Consider the dependent applications from {system_selected} runbook, and use IP, hostname and port details from the EPH Primary instance, EPH Secondary instance, and CoreBanking Primary instance, CoreBanking Secondary instance IP addresses to form the specific scripts, as a part of the validating the dependent systems. Do not generate generic scripts. Factor it as a part of the steps"

if submit_button:
    st.success("Configuration Submitted Successfully!")
    st.header("Generated DR Drill Steps")

    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt_1},
            {"role": "user", "content": extract_text(uploaded_files)}
        ],
        max_tokens=4096,
        temperature=0.6,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    response = completion.choices[0].message.content.strip()

    st.write(response)

    st.download_button(
        label=f"Download Steps",
        data=response,
        file_name=f"DR_Steps.txt",
        mime="text/plain",
    )

# Chatbot Section
st.markdown("---")
st.header("\U0001F4AC Chat with Your Runbooks")

if uploaded_files:
    chatbot = get_chatbot_chain(uploaded_files)

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    user_input = st.text_input("Ask a question about your runbooks:")

    if user_input:
        result = chatbot.run(user_input)
        st.session_state["chat_history"].append(("You", user_input))
        st.session_state["chat_history"].append(("Assistant", result))

    for sender, msg in st.session_state["chat_history"]:
        if sender == "You":
            st.markdown(f"**\U0001F9D1‍💻 {sender}:** {msg}")
        else:
            st.markdown(f"**\U0001F916 {sender}:** {msg}")

st.sidebar.markdown("---")
st.sidebar.write("Powered by Streamlit, OpenAI, and FAISS.")

