# Micro Paper: Offline Motivational Video Generator
This document outlines the reasoning behind key model and design choices made during the development of the Offline Motivational Video Generator. The goal was to create an end-to-end pipeline that runs entirely offline, handles audio + image generation, and outputs clean, themed videos using Python.

## Why Tacotron2 + HiFi-GAN for TTS

There are several local TTS models available today, but Tacotron2 paired with HiFi-GAN hits a good balance between quality, speed, and local compatibility
* **Tacotron2** is well-documented and relatively stable. It maps text to mel-spectrograms with clear structure
* **HiFi-GAN** is a fast, non-autoregressive vocoder that converts spectrograms to audio with minimal artifacts
* Both models are compatible with GPU/CPU execution and can run with pre-trained weights (LJSpeech) without needing extra setup or finetuning

## Why Stable Diffusion v1.4 for Image Generation

Image generation was handled using Stable Diffusion v1.4 due to the following reasons:

* **Offline support**: It’s one of the most accessible diffusion models with local inference capabilities
* **Model size vs. quality**: v1.4 hits a good middle ground in quality while being reasonably lightweight compared to later versions (like v2.1)
* **Control over prompts**: Since the task was to generate images that fit motivational quotes, prompt tuning and repeatability mattered more than ultra-high fidelity

## Why Docker for Reproducibility

Rather than asking users to set up Python environments, manage CUDA versions, or troubleshoot missing dependencies, Docker simplifies the entire process

* Ensures that the exact runtime environment (Python version, library versions, CUDA toolkits, etc.) is preserved
* Removes inconsistencies across machines
* Makes sharing, testing, and deployment smoother, especially for setups involving complex ML dependencies

## Resource Considerations & CPU Fallback

This project assumes access to a GPU for smoother performance, especially for image generation

* TTS runs fine on CPU, though slower
* Stable Diffusion, however, is quite slow on CPU generating a single image can take several minutes

That said, the code includes CPU support for all models. A flag isn’t explicitly required if CUDA is unavailable, the models will default to CPU

This makes the script more accessible to users on low-resource systems, even if it’s not ideal for production-scale use

---

These choices were made to prioritize stability, compatibility, and local-first workflows, which aligned with the core requirement: build something that works offline and cleanly ties all components together
