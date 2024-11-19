First of all configure environment variables.
 - add `.env` file into the root directory
 - add and configure following env variables:
```properties
AZURE_OPENAI_API_KEY="example-open-api-key"
AZURE_OPENAI_ENDPOINT="https://example.openai.azure.com"
AZURE_OPENAI_API_VERSION="2023-05-15"
OPENAI_API_VERSION="2023-05-15"
DATABASE_CONNECTION_STRING="postgresql://example:example@example.postgres.database.azure.com:5432/postgres"
CONFLUENCE_URL="https://example.atlassian.net/wiki"
CONFLUENCE_USERNAME="example@example.com"
CONFLUENCE_API_KEY="example-confluence-api-key"
SYSTEM_PROMPT_TEMPLATE="%prompt. Své odpovědi zakládej na zkladě totoho kontextu: %context. Kontext je struktuře data a zdroj. Odpovědi formátuj do Markdown. Na konci odpovědi vypiš odkazy na zdroje."
```

Index the data from confluence to PG vector:
 - run `gradio .\src\confluence.py` 

To start the application on local:
 - run `gradio .\src\main.py` 
 - Chatbot app should now be accessible at http://127.0.0.1:7860.

To build docker image:
 - run `docker build -t gradio-app .`

To run the image:
 - run `docker run -p 7860:7860 gradio-app`
 - Chatbot app should now be accessible at http://localhost:7860.