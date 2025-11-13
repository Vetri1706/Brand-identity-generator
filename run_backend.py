#!/usr/bin/env python
"""Run the backend server"""
import sys
import os

if __name__ == "__main__":
    # Add backend to path
    backend_dir = r"C:\Users\vetri\Miniproj\brand_identity_generator_mvp\backend"
    sys.path.insert(0, backend_dir)
    os.chdir(backend_dir)

    # Run uvicorn
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
