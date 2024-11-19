from langchain_community.document_loaders import ConfluenceLoader
from langchain_community.vectorstores import PGVector
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv
from os import getenv
from langchain_text_splitters import MarkdownTextSplitter

load_dotenv()

# def loadConfuencePages():
if __name__ == '__main__':
    confluenceApiKey = getenv("CONFLUENCE_API_KEY")
    confluenceUrl = getenv("CONFLUENCE_URL")
    confluenceUsername = getenv("CONFLUENCE_USERNAME")

    loader = ConfluenceLoader(
        url=confluenceUrl, username=confluenceUsername, api_key=confluenceApiKey, space_key="ITAA",
        include_attachments=False, keep_markdown_format=True
    )
    docs = loader.load()


    # See docker command above to launch a postgres instance with pgvector enabled.
    connection = getenv("DATABASE_CONNECTION_STRING")

    embeddings = AzureOpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = PGVector(
        connection_string=connection,
        embedding_function=embeddings,
        use_jsonb=True,
    )

    text_splitter = MarkdownTextSplitter()
    docs = text_splitter.split_documents(docs)

    vector_store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])

