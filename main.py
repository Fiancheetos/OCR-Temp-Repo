# Import necessary modules from FastAPI
from fastapi import FastAPI, Request
import uvicorn

from pdf2image import convert_from_path
import torReader
import upgComputation

# Initialize the FastAPI application
app = FastAPI(
    title="Transcript OCR",
    description="",
    version="0.1.0"
)

# --- FUNCTIONS ---

async def receive_blob(file):
    with open("tor.pdf", "wb") as fp:
        fp.write(file)

async def convert_to_png():
    images = convert_from_path("tor.pdf", fmt='png')
    return images

async def process_img(images, records_table, config):
    for image in images:
        records_table = torReader.process(image, torReader.detect_columns(image), records_table, config)

    return records_table

# --- API Endpoints (Routes) ---

@app.get("/api/{config}")
async def run_func(blob : Request, config: str):
    file : bytes = await blob.body()
    await receive_blob(file)

    images = await convert_to_png()
    records_table = dict()
    await process_img(images, records_table, config)
    gwa = upgComputation.compute_gwa(records_table)
    return {"table": records_table, "gwa": gwa}

# --- Run the application ---
# This block allows you to run the FastAPI application directly using `python main.py`.
# For production, you would typically run it using `uvicorn main:app --host 0.0.0.0 --port 8000`.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

