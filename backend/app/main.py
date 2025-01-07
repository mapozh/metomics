from fastapi import FastAPI
from app.routes import metadata_routes

app = FastAPI(
    title="RNA-seq Metadata Management API",
    description="Manages RDF data for RNA-seq experiments",
    version="1.0.0",
)

# Include routes
app.include_router(metadata_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to RNA-seq Metadata API"}
