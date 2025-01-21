import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import metadata_routes, chatbot_routes

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="RNA-seq Metadata Management API",
    description="Manages RDF data for RNA-seq experiments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(metadata_routes.router)
app.include_router(chatbot_routes.router)

# Root Endpoint
@app.get("/")
def root():
    """
    Root endpoint for API.
    """
    return {"message": "Welcome to RNA-seq Metadata API"}

