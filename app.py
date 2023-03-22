import streamlit as st
from utils import parse_pdf, embed_text, get_answer


# Load custom CSS
st.markdown("""
    <style>
        %s
    </style>
""" % open("style.css").read(), unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])
with col1:
    st.image("pdfbot.png")
with col2:
    st.header("PDF Bot")
uploaded_file = st.file_uploader("Upload any PDF and ask questions about the document", type=["pdf"])

if uploaded_file is not None:
    index = embed_text(parse_pdf(uploaded_file))
    query = st.text_area("Ask a question about the document")
    button = st.button("Submit")
    if button:
        result = get_answer(index, query)
        output_text = result['result']
        output_paragraphs = output_text.split('\n\n')
        formatted_text = '\n\n'.join([f'<p>{p}</p>' for p in output_paragraphs])
        st.write(f"Your results:", unsafe_allow_html=True)
        st.markdown(formatted_text, unsafe_allow_html=True)

