# Import necessary modules from FastAPI
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from pdf2image import convert_from_path
import TORReader

# Initialize the FastAPI application
app = FastAPI(
    title="Basic FastAPI Boilerplate",
    description="A simple starting point for your FastAPI projects.",
    version="0.1.0"
)

# --- Data Models (using Pydantic) ---
# Pydantic models define the structure of your data (request bodies and response models).

class Table(BaseModel):
    """
    Represents an item with a name and an optional description and price.
    """
    # overallGWA: float
    recordTable: dict[str, List[str | float]]

    class Config:
        """
        Configuration for the Pydantic model.
        Used to provide example data for API documentation (OpenAPI/Swagger UI).
        """
        schema_extra = {
            "example": {
                # "overallGWA": 1.00,
                "recordTable": {"HK 12": ["Human Kinetics", 1.00]}
            }
        }

# --- PDF TO PNG CONVERSION ---

def convert_to_png():
    images = convert_from_path('/Users/fianchetto/Downloads/TORSample.pdf', output_folder='/Users/fianchetto/Desktop/Internship', fmt='png')
    return images

def process_img(images, records_table):
    for image in images:
        records_table = TORReader.process(image, records_table)

    return records_table

# --- API Endpoints (Routes) ---

@app.get("/api/")
async def run_func():
    images = convert_to_png()
    records_table = dict()
    process_img(images, records_table)
    return records_table

# --- Run the application ---
# This block allows you to run the FastAPI application directly using `python main.py`.
# For production, you would typically run it using `uvicorn main:app --host 0.0.0.0 --port 8000`.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

