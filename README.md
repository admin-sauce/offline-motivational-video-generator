# Offline Motivational Video Generator
This project was built as part of a technical assessment for icrewsystems. The goal was to build a fully offline pipeline that takes 10 motivational quotes, generates speech from them using a local TTS model, produces matching images via Stable Diffusion, and assembles them into short videos all without using any cloud APIs or external services

The task was not just about writing code, but about demonstrating the ability to integrate multiple tools locally, choose and justify appropriate models, and structure the project for reproducibility

## Table of Contents
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)
  * [Clone the Repo](#clone-the-repo)
  * [Using Docker (Recommended)](#using-docker-recommended)
  * [Local Install (Alternative)](#local-install-alternative)
* [Project Structure](#project-structure)
* [Design Decisions & Model Choices (Micro Paper)](#design-decisions--model-choices-micro-paper)
* [License](#license)

## Features
* Fully offline execution no internet or cloud APIs required
* Text-to-Speech using Tacotron2 + HiFi-GAN (trained on LJSpeech dataset)
* Image generation with Stable Diffusion v1.4, locally using diffusers or Automatic1111 backend
* Subtle video effects and assembly handled via MoviePy (zoom, fade, synced audio)
* Docker-based setup for reproducibility

## Prerequisites
### Hardware

* NVIDIA GPU with at least 8 GB VRAM (recommended for reasonable speed)
* CPU mode supported, but slower

### Software

* Docker ≥ 20.10 (preferred setup)
* Or Python 3.10+ and pip for local install

## Getting Started

### Clone the Repo

```bash
git clone https://github.com/<your-username>/offline-motivational-video-generator.git
cd offline-motivational-video-generator
```

### Using Docker (Recommended)
1. **Build the Docker image**

```bash
docker build -t motivator:latest .
```

2. **Run the container**

* With GPU:

```bash
docker run --gpus all -v "$(pwd)/motivational_videos:/app/output" motivator:latest
```

* CPU only:

```bash
docker run -e CUDA_VISIBLE_DEVICES="" -v "$(pwd)/motivational_videos:/app/output" motivator:latest
```

3. **View Results**

* Final videos will be in the `output/` directory

### Local Install (Alternative)
1. **Set up Python environment**

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. **Run the Script**

```bash
python app.py
```

3. **Check Output**

* The 10 MP4 files will be saved in `output/`

## Project Structure

```
.
├── Dockerfile
├── README.md
├── app.py
├── micropaper.md
├── requirements.txt
└── output/
```


## Design Decisions & Model Choices (Micro Paper)

All model decisions and prompt strategies are explained in `micropaper.md` It covers:
* Why Tacotron2 and HiFi-GAN were used for TTS
* Tradeoffs of Stable Diffusion v1.4 vs other variants
* Why Docker was used for reproducibility
* Resource considerations and fallback modes (e.g. CPU support)

## License

MIT License. See LICENSE file for details
