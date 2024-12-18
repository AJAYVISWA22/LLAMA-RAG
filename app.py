import streamlit as st
from rag import RAGSystem


def main():

    ## Page configuration
    st.set_page_config(
        page_title='PDF Question answering system',
        page_icon=':Book:',
        layout='wide'
    )

    if 'rag_system' not in st.session_state:
        st.session_state.rag_system=RAGSystem()

    if 'query_engine' not in st.session_state:
        st.session_state.query_engine=None

    if 'pdf_processor' not in st.session_state:
        st.session_state.pdf_processed=False
        
    st.title('PDF Question Answering System ')


    # page Side bar
    st.sidebar.header('Upload PDF')

    uploaded_file=st.sidebar.file_uploader('Choose a PDF file',type='pdf')

    if uploaded_file:
        with st.spinner('processing PDF >>> This might take a minute'):
            try:
                success=st.session_state.rag_system.process_pdf(uploaded_file.getvalue())
                if success:
                    st.session_state.query_engine=st.session_state.rag_system.get_querry_engine()
                    st.session_state.pdf_processed = True
                    st.sidebar.success('PDF processed Successfully')
                else:
                    st.sidebar.error("Error processing PDF!")

            except Exception as e:
                st.sidebar.error(f'ERROR:{str(e)}')

    st.header("Ask a question")
    question= st.text_input("Enter your question")

    # Generate Response
    if st.button('GET ANSWER'):
        if not question:
            st.warning("Please enter a question")
        elif not st.session_state.pdf_processed:
            st.warning("Please upload a pdf first")
        else:
            with st.spinner('Generating anwser...'):
                try:
                    response=st.session_state.rag_system.generate_response(
                        st.session_state.query_engine,
                        question
                    )
                    st.subheader("Anwser")
                    st.write(response)
                except Exception as e:
                    st.error (f'Error:{str(e)}') 

        
if __name__== '__main__':
    main()
