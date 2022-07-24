import glob
import os

import streamlit as st
from streamlit_ace import st_ace

st.set_page_config(layout="wide")

def restart():
    """
    Delete all cache
    """    
    for key in st.session_state.keys():
        del st.session_state[key]

def main():
    with st.sidebar:
        template_sel = st.selectbox('Select Template',map(os.path.basename,glob.glob("./SQL/*.sql")),on_change=restart)
        if template_sel and "query" not in st.session_state:
            fd = open(f'./SQL/{template_sel}', 'r')
            st.session_state["query"] = fd.read()
            fd.close()

        st.markdown("---")

    with st.expander("QUERY EDITOR",expanded=True):

        st.write('<style> div.stRadio > div{flex-direction: row;}</style>', unsafe_allow_html=True)
        editor_sel = st.radio("Mode", ("Simple", "Editor"), key="editor_radio_select")

        #region SIMPLE MODE
        if editor_sel == "Simple":
            simple_col1, simple_col2 = st.columns(2)

            with simple_col1:
                with st.form("edit_query1",clear_on_submit = True):
                    simple_input1 = st.text_input("AND",key="simple_input1")
                    simple_form_submit = st.form_submit_button(label = 'ADD')	
                    if simple_form_submit and simple_input1 != "":
                        st.session_state["query"] += f"\n    AND {simple_input1}"
            with simple_col2:
                with st.form("edit_query2",clear_on_submit = True):
                    simple_input2 = st.text_input("OR",key="simple_input2")
                    simple_form_submit = st.form_submit_button(label = 'ADD')	
                    if simple_form_submit and simple_input2 != "":
                        st.session_state["query"] += f"\n    OR {simple_input2}"
        #endregion

        #region EDITOR MODE
        if editor_sel == "Editor":
            st.warning(":bulb: SAVE/APPLY changes after edit (CTRL+ENTER) :bulb:")
            st.sidebar.title("Editor settings")
            editor_content = st_ace(
                value=st.session_state["query"],
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

    st.markdown("---")

    with st.expander("ACTUAL QUERY",expanded=True):
        if "query" in st.session_state:
            st.code(st.session_state["query"])

    st.markdown("---")

    execute_btn = st.button("QUERY")
    if execute_btn: 
        st.write("some DBAPI happened...")

if __name__ == '__main__':
    main()
    