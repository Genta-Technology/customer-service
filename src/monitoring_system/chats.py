"""
This is the place where the view chats works
"""

import streamlit as st
from datetime import datetime
import json

def chats_page():
    """
    Main chat menu
    """
    st.title('Genta Social Media Chat Page')    
    st.write('Welcome to the chats page!')

    if "data" not in st.session_state:
        st.session_state["data"] = json.load(open("chat_history.json"))["data"]
    
    st.session_state["data"] = sorted(st.session_state["data"], key=lambda d: d['time_last_conversation'])
    chat_index = 0
    for d in st.session_state.data:
        chat_index += 1
        
        with st.expander("Chat " + str(chat_index)):
            chat_col1, chat_col2 = st.columns(2)
            with chat_col1:
            
                # print chat id
                st.write("Chat ID: "+d["chat_id"])
                
                # print time of last response
                st.write("Last response: "+
                         datetime.utcfromtimestamp(d["time_last_conversation"]).strftime('%Y-%m-%d %H:%M:%S'))
            
            with chat_col2:
                # delete button and edit button 
                del_button = st.button("delete last response", key="del_last_msg/id="+d["chat_id"])
                edit_button = st.button("edit last response", key="edit_msg/id="+d["chat_id"])
            
            # check if the last message is assistant role
            if del_button and d["chat_history"][-1]["role"] == "assistant":
                # remove the last message
                st.session_state["del_last_msg"+d["chat_id"]] = True
                d["chat_history"] = d["chat_history"][:-1]
                
            
            # edit the messages
            if edit_button:
                if d["chat_history"][-1]["role"] == "assistant" or d["chat_history"][-1]["role"] == "response":
                    st.text_input("insert your new response", key="edit_msg/val/id="+d["chat_id"])
                else:
                    st.warning("we cannot change the last message")
            if "edit_msg/val/id="+d["chat_id"] in st.session_state:
                d["chat_history"][-1]["content"] = st.session_state["edit_msg/val/id="+d["chat_id"]]
            
            # render the chats
            for chats in d["chat_history"]:
                with st.chat_message(chats["role"]):
                    st.write(chats["content"])
    try:
        json.dump({"data": st.session_state["data"]}, open("chat_history.json", "w"))["data"]
    except:
        pass