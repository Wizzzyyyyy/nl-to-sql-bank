import streamlit as st

st.set_page_config(page_title="Bank NL-to-SQL Assistant", page_icon="📃")
st.title("📃 Ask Your Bank Data")

question = st.text_input("Ask a question about the data:")

if st.button("Ask"):
	if question:
		st.write("You asked:", question)
		st.info("(real results will appear here starting Day 14)")
	else:
		st.warning("Type a question first.")