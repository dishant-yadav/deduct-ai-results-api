import os
from llama_index.llms.gradient import GradientBaseModelLLM
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.gradient import GradientEmbedding
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from dotenv import load_dotenv
import time


# Execution time decorator
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} execution time: {execution_time} seconds")
        return result

    return wrapper


# Global variable to store pre-loaded documents
documents = {}

path_mapping = {
    "precautions": "precautions",
    "procedures": "procedures",
    "sections": "sections",
}


# Load documents once
@measure_execution_time
def load_documents():
    global documents
    for action, path in path_mapping.items():
        load_dotenv(dotenv_path=f"./.env.{path}")
        try:
            documents[action] = SimpleDirectoryReader(f"./PDF/{path}").load_data()
            print(f"Loaded {len(documents[action])} document(s) for {action}.")
        except Exception as e:
            print(f"An error occurred while loading documents for {action}: {e}")


# Function to process queries
@measure_execution_time
def get_result_from_object(action, query):
    global documents
    if action not in documents:
        print(f"Error: Documents for {action} not loaded.")
        return {"Error": "Documents not loaded."}

    try:
        llm = GradientBaseModelLLM(
            base_model_slug="llama2-7b-chat",
            max_tokens=400,
        )

        embed_model = GradientEmbedding(
            gradient_access_token=os.getenv("GRADIENT_ACCESS_TOKEN"),
            gradient_workspace_id=os.getenv("GRADIENT_WORKSPACE_ID"),
            gradient_model_slug="bge-large",
        )

        Settings.embed_model = embed_model
        Settings.llm = llm
        Settings.chunk_size = 1024

        index = VectorStoreIndex.from_documents(documents[action])
        query_engine = index.as_query_engine()

        final_query = get_refined_query(action, query)

        print("Query :", final_query)
        response = query_engine.query(final_query)
        print("Response :", response)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"Error": "Error in model"}


# Function to generate refined query
def get_refined_query(action, query):
    get_response_in_list = "Provide only the list of required values in response. The Response should not exceed 700 words."
    refined_query = f"{get_query(action, query)} {get_response_in_list}"
    return refined_query


# Function to generate query based on action
def get_query(action, query):
    if action == "precautions":
        return f"List down {action} while collecting {query} as an evidence."
    elif action == "procedures":
        return f"List down {action} of collecting {query} as an evidence."
    elif action == "sections":
        return f"What would be the Sections of charges that can be imposed for {query}? Always Give list like eg. 1. Section 302 of IPC - Punishment for sabotage"


# Load documents once
load_documents()

# Example usage:
# get_result_from_object("precautions", "firearms")
# get_result_from_object("procedures", "knife")
# get_result_from_object("sections", "guns")
