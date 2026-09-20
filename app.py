import streamlit as st
import pandas as pd
from nl_to_sql import nl_to_sql, is_select_only, explain_result
from ask import clean_sql, execute_sql
from audit import log_query

st.set_page_config(page_title="Bank NL-to-SQL Assistant", page_icon="🏦")
st.title("🏦 Ask Your Bank Data")

question = st.text_input("Ask a question about the data:")

if st.button("Ask"):
    if not question:
        st.warning("Type a question first.")
    else:
        with st.spinner("Thinking..."):
            raw_sql = nl_to_sql(question)
            sql = clean_sql(raw_sql)

        if not is_select_only(sql):
            st.error("⚠️ Refusing to run this — validator confirmed it isn't a plain SELECT.")
            log_query(question, sql, "blocked")
        else:
            try:
                columns, rows = execute_sql(sql)
            except Exception as e:
                st.error(f"⚠️ Couldn't run that query: {e}")
                log_query(question, sql, "error")
            else:
                st.code(sql, language="sql")

                if not rows:
                    st.info("No results found for that question.")
                    log_query(question, sql, "success", 0)
                else:
                    df = pd.DataFrame(rows, columns=columns)
                    st.dataframe(df)

                    with st.spinner("Summarizing..."):
                        explanation = explain_result(question, columns, rows)
                    st.success(explanation)
                    log_query(question, sql, "success", len(rows))