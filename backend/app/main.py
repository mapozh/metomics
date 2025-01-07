from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import metadata_routes

# Initialize FastAPI app
app = FastAPI(
    title="RNA-seq Metadata Management API",
    description="Manages RDF data for RNA-seq experiments",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc documentation
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to specific origins in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(metadata_routes.router)

# Root Endpoint
@app.get("/")
def root():
    return {"message": "Welcome to RNA-seq Metadata API"}

