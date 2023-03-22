import streamlit as st
from utils import parse_pdf, embed_text, get_answer


# Load custom CSS
st.markdown("""
    <style>
        %s
    </style>
""" % open("style.css").read(), unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    st.image("pdfbot.png")
with col2:
    st.markdown("<div style='text-align: center; font-style: italic;'><h1>PDF Bot</h1><div style='margin-top: 1px;'><p style='font-size: 24px;'>AI-Powered Search For Any PDF</p></div></div>", unsafe_allow_html=True)




uploaded_file = st.file_uploader("Upload any PDF and when processed you can ask any question about the document", type=["pdf"])

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

# Add footer
footer_html = """
    <div style="position: fixed; bottom: 0; width: 100%; background-color: #f5f5f5; text-align: center; margin: auto;">
        <p>Made by <a href="mailto:kylelegare@gmail.com">Kyle Legare</a></p>
    </div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
