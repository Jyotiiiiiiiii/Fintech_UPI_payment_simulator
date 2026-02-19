from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from app.routes import users, transactions

# Initialize FastAPI app
app = FastAPI(
    title="UPI Payment Simulation System",
    description="A simulated UPI payment system built with FastAPI and SQLite",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(transactions.router)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.api_route("/{full_path:path}", methods=["GET"])
async def serve_spa(full_path: str):
    """Serve SPA - static files and fallback to index.html"""
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    file_path = os.path.join(static_dir, full_path)
    
    # Check if file exists
    if os.path.isfile(file_path) and os.path.commonpath([static_dir, file_path]) == static_dir:
        return FileResponse(file_path)
    
    # Return index.html for SPA routing (for unfound routes)
    index_path = os.path.join(static_dir, 'index.html')
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    
    return {"error": "Not found"}

# Handle root path
@app.get("/")
async def root():
    """Serve index.html"""
    index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'index.html')
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {"status": "API running", "docs": "/docs"}
