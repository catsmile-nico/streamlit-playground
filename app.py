import glob
import os
import time

import streamlit as st


def restart():
    for key in st.session_state.keys():
        del st.session_state[key]

def main():
    st.title("SQLPlayground")

    option = st.selectbox('Select Template',map(os.path.basename,glob.glob("./SQL/*.sql")),on_change=restart)
    if option and "template" not in st.session_state:
        fd = open(f'./SQL/{option}', 'r')
        st.session_state["template"] = fd.read()
        fd.close()

    st.markdown("---")

    st.write('<style> div.stRadio > div{flex-direction: row;}</style>', unsafe_allow_html=True)
    sel_edit = st.radio("Mode", ("Simple", "Editor"), key="editor_radio_select")

    if sel_edit == "Simple":
        if "query" not in st.session_state:
            st.session_state["query"] = ""

        query_area = st.empty()
        query_area.code(st.session_state["template"].format(st.session_state["query"]))
        col1, col2 = st.columns(2)

        with col1:
            with st.form("edit_query1",clear_on_submit = True):
                txt1 = st.text_input("AND",key="txt1")
                submit_button = st.form_submit_button(label = 'ADD')	
                if submit_button and txt1 != "":
                    st.session_state["query"] += f"\n    AND {txt1}"
                    query_area.code(st.session_state["template"].format(st.session_state["query"]))
        with col2:
            with st.form("edit_query2",clear_on_submit = True):
                txt2 = st.text_input("OR",key="txt2")
                submit_button = st.form_submit_button(label = 'ADD')	
                if submit_button and txt2 != "":
                    st.session_state["query"] += f"\n    OR {txt2}"
                    query_area.code(st.session_state["template"].format(st.session_state["query"]))

    if sel_edit == "Editor":
        st.session_state["template"] = st.session_state["template"].format(st.session_state["query"])
        st.session_state["query"] = ""
        st.text_area("",st.session_state["template"], key="editor_textarea1")
        save_button = st.button("SAVE", key="editor_btn_save1")
        if save_button:
            st.session_state["template"] = st.session_state.editor_textarea1 + " {0}"
            tv_success = st.empty()
            tv_success.success("SAVED")
            time.sleep(1)
            tv_success.empty()
        
                
    # if "query" in st.session_state:
    #     st.write("QUERYSESS:",st.session_state["query"]) 

    st.markdown("---")

    st.help(st.write)

if __name__ == '__main__':
	main()
