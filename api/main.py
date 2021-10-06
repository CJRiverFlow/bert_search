# index_name = "bert_betmaster"
import uvicorn
from query_master import QueryMaster
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()
qm = QueryMaster()

class Data(BaseModel):
    index_name: str
    query: str
    top_n: int

@app.get("/")
def read_root():
    return "App working great"

@app.post("/query_bert")
def query_bert(data : Data):
    res = {"result":[]}
    top_results = qm.query_question(data.index_name,
        data.query, data.top_n)
    res["result"].append(top_results)
    json_result = jsonable_encoder(res)
    return JSONResponse(content=json_result)

#Uvicorn configuration
if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=5050)