import re
import glob
import os

import streamlit as st
import extra_streamlit_components as stx
from streamlit_ace import st_ace


st.set_page_config(layout="wide")

def restart():
    """
    Delete all cache
    """    
    for key in st.session_state.keys():
        # if key == "query": continue
        del st.session_state[key]

def parse_param(query):
    tmp_param = re.findall(r"{(\w+)}", query)
    st.session_state["final_data"] = {a:None for a in tmp_param}

def main():
    with st.sidebar:
        template_sel = st.selectbox('Select Template',map(os.path.basename,glob.glob("./SQL/*.sql")),on_change=restart)
        if template_sel and "query" not in st.session_state:
            fd = open(f'./SQL/{template_sel}', 'r')
            st.session_state["query"] = fd.read()
            fd.close()
            parse_param(st.session_state["query"])
            
        st.code(st.session_state["query"])

        st.markdown("---")

    # st.write('<style> div.stRadio > div{flex-direction: row;}</style>', unsafe_allow_html=True)
    # editor_sel = st.radio("Mode", ("Simple", "Editor"), key="editor_radio_select", horizontal=True)
    tab_simple, tab_editor = st.tabs(["Simple", "Editor"])

    #region SIMPLE MODE
    # if editor_sel == "Simple":
    with tab_simple:
        simple_col1, simple_col2 = st.columns(2)
        with simple_col2:
            st.session_state["container"] = st.container()
            param_num = 0
            for key in st.session_state["final_data"].keys():
                if key == "date_range":
                    create_daterange(key,param_num)
                    param_num+=1
                elif key == "db_name":
                    create_text(key,param_num)
                    param_num+=1
                elif key == "sel_var":
                    create_text(key,param_num)
                    param_num+=1
        with simple_col1:
            st.code(st.session_state["query"].format(**st.session_state["final_data"]))
    #endregion

    #region EDITOR MODE
    # if editor_sel == "Editor":
    with tab_editor:
        st.warning(":bulb: SAVE/APPLY changes after edit (CTRL+ENTER) :bulb:")
        st.sidebar.title("Editor settings")
        editor_content = st_ace(
            value=st.session_state["query"].format(**st.session_state["final_data"]),
            placeholder="Write your code here",
            language=st.sidebar.selectbox("Language", options=("sql","sqlserver","mysql")),
            theme=st.sidebar.selectbox("Theme", options=("cobalt","sqlserver","terminal","xcode")),
            keybinding="vscode",
            font_size=16, tab_size=2,
            show_gutter=True, show_print_margin=False,
            wrap=False, min_lines=10,
            auto_update=False, readonly=False,
            key="ace",
        )
        if editor_content:
            st.session_state["query"] = editor_content
        #endregion

    
def create_daterange(key,id):
    st.session_state["final_data"][key] = st.session_state["container"].date_input("Date Range", key="param"+str(id))
    
def create_text(key,id):
    st.session_state["final_data"][key] = st.session_state["container"].text_input("DB Name", key="param"+str(id))


if __name__ == '__main__':
    main()