# Use minimal Python 3.10 image
FROM python:3.10-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/app

WORKDIR $HOME

# 1) Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) Copy & install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 3) Copy application code
COPY . .

# 4) (Optional) Pre‐download models inside the image to avoid delays at runtime.
#    This assumes your app.py can accept a `--preload` flag to download models & then exit.
#    If you haven’t added that argument, you can skip this RUN step.
# RUN python app.py --preload

# 5) Define the default entrypoint
CMD ["python", "app.py"]
