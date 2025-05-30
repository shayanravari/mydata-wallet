from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import csv
from datetime import datetime
from dp_engine.query_logic import count_receipts_over_amount

app = FastAPI()

FIXED_USER_ID = "user123"
USER_VAULT_BASE = "user_vaults"

class QueryRequest(BaseModel):
    query_name: str
    epsilon: float

class IngestData(BaseModel):
    item_name: str
    amount: float
    category: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to MyData Wallet API!"}

@app.post("/query")
async def run_query(request: QueryRequest):
    user_data_path = os.path.join(USER_VAULT_BASE, FIXED_USER_ID, "receipts.csv")

    if not os.path.exists(user_data_path):
        raise HTTPException(status_code=404, detail="User data not found")

    if request.query_name == "count_receipts_over_50":
        result = count_receipts_over_amount(user_data_path, request.epsilon, 50.0)
        return {"result": result, "epsilon_used": request.epsilon}
    else:
        raise HTTPException(status_code=400, detail="Unknown query name")
    
@app.post("/ingest")
async def ingest_data(data: IngestData):
    user_data_path = os.path.join(USER_VAULT_BASE, FIXED_USER_ID, "receipts.csv")
    os.makedirs(os.path.dirname(user_data_path), exist_ok=True)

    file_exists = os.path.isfile(user_data_path)
    fieldnames = ['receipt_id', 'user_id', 'item_name', 'amount', 'category', 'timestamp']

    receipt_id = int(datetime.now().timestamp() * 1000)

    with open(user_data_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'receipt_id': receipt_id,
            'user_id': FIXED_USER_ID,
            'item_name': data.item_name,
            'amount': data.amount,
            'category': data.category,
            'timestamp': datetime.now().isoformat()
        })
    return {"message": "Data ingested", "receipt_id": receipt_id}

# To run: uvicorn main_api:app --reload