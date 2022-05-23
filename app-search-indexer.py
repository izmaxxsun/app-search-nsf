from elastic_enterprise_search import AppSearch
import os

app_search = AppSearch("https://izmaxx-hostrisk-8-1.ent.us-central1.gcp.cloud.es.io:9243",bearer_auth=os.environ.get('APP_SEARCH_API_KEY'))

engine_info = app_search.get_engine(engine_name='nsf-test')
print(engine_info)

app_search.index_documents(
    engine_name="nsf-test",
    documents=doc_list
)