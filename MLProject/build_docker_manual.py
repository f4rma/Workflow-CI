# masih pakai format dan structure MLflow model.

import os
import shutil
import subprocess
import tempfile

# Configuration
MODEL_PATH = "mlruns/740110415802254864/4f61de53d267453a953500fd7d4ee35b/artifacts/model"
IMAGE_NAME = "f4rma/heart-disease-model:latest"

print(f"Building Docker image: {IMAGE_NAME}")
print(f"Using model from: {MODEL_PATH}")

# Create temporary directory for Docker build context
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"\nCreating build context in: {tmpdir}")
    
    # Copy model to temp directory
    model_dest = os.path.join(tmpdir, "model")
    shutil.copytree(MODEL_PATH, model_dest)
    print(f"✓ Model copied to build context")
    
    # Create Dockerfile
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /opt/ml

# Copy model files
COPY model /opt/ml/model

# Install MLflow and dependencies from model's requirements
RUN pip install --no-cache-dir mlflow==2.9.2 && \\
    if [ -f /opt/ml/model/requirements.txt ]; then \\
        pip install --no-cache-dir -r /opt/ml/model/requirements.txt; \\
    fi

# Set environment variables
ENV MLFLOW_TRACKING_URI=""
ENV MLFLOW_MODEL_DIR=/opt/ml/model

# Expose port for model serving
EXPOSE 8080

# Command to serve the model
CMD mlflow models serve -m /opt/ml/model -h 0.0.0.0 -p 8080 --no-conda
"""
    
    dockerfile_path = os.path.join(tmpdir, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(dockerfile_content)
    print(f"✓ Dockerfile created")
    
    # Build Docker image
    print(f"\n📦 Building Docker image...")
    try:
        result = subprocess.run(
            ["docker", "build", "-t", IMAGE_NAME, "."],
            cwd=tmpdir,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(f"\nDocker image built successfully: {IMAGE_NAME}")
        print(f"\nNext steps:")
        print(f"1. Login to Docker Hub: docker login")
        print(f"2. Push image: docker push {IMAGE_NAME}")
    except subprocess.CalledProcessError as e:
        print(f"\nDocker build failed!")
        print(f"Error output:\n{e.stderr}")

