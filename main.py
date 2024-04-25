from fastapi import FastAPI
from utils import get_result_from_object

app = FastAPI()


@app.get("/api/test/")
def test():
    return {"message": "Results API"}


@app.get("/api/precautions/{query}")
async def read_precautions(query: str = None):
    try:
        print("Precautions", query)
        precautions = get_result_from_object("precautions", query)
        return {"status": "OK", "query": query, "precautions": precautions}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"Error": "Error in api call"}


@app.get("/api/procedures/{query}")
async def read_procedures(query: str = None):
    try:
        print("Procedures", query)
        procedures = get_result_from_object("procedures", query)
        return {"status": "OK", "query": query, "procedures": procedures}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"Error": "Error in api call"}


@app.get("/api/sections/{query}")
async def read_sections(query: str = None):
    try:
        print("Sections", query)
        sections = get_result_from_object("sections", query)
        return {"status": "OK", "query": query, "sections": sections}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"Error": "Error in api call"}
