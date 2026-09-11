# Jarvis - AI Virtual Assistant

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--Powered-brightgreen)
![License](https://img.shields.io/badge/License-MIT-orange)

Jarvis is a voice-controlled AI virtual assistant. Built with Python, it listens to your voice commands, processes them intelligently using OpenAI's language models, and speaks back to you. 

This repository includes **two variations** of the assistant, allowing you to choose between ultra-realistic premium voice generation or a fully free local/Google TTS approach.

## Features

- **Wake Word Detection:** Constantly listens for the wake word *"Jarvis"* to activate.
- **Conversational AI:** Integrates with OpenAI to answer general questions and hold conversations.
- **Web Browsing:** Voice commands to open Google, YouTube, and Facebook.
- **Music Player:** Tell Jarvis to play specific songs from your custom `musicLibrary`.
- **Live News:** Fetches and reads out the top 5 latest news headlines using NewsAPI.

## Repository Structure & Implementations

There are two main scripts in this repository. You can run whichever fits your needs:

### 1. `jarvis_elevenlabs.py` (Premium TTS)
* **Text-to-Speech:** Uses **ElevenLabs** for ultra-realistic, natural human-like voice synthesis.
* **AI Model:** Powered by OpenAI (`gpt-5.6-luna`).
* *Best for:* Users who want the highest quality, most realistic voice experience.

### 2. `jarvis_gtts.py` (Free TTS)
* **Text-to-Speech:** Uses **gTTS (Google Text-to-Speech)** and **pyttsx3** alongside `pygame` for audio playback. 
* **AI Model:** Powered by OpenAI (`gpt-6-astra`).
* *Best for:* Users who want a free, reliable, and easy-to-run TTS solution without relying on premium voice APIs.

## Prerequisites & Installation

### 1. Install Python and PyAudio
Make sure you have Python 3.8+ installed. You will also need `PyAudio` for the microphone to work:
* **Windows:** `pip install pyaudio`
* **Mac:** `brew install portaudio` followed by `pip install pyaudio`
* **Linux:** `sudo apt install python3-pyaudio`

### 2. Install Dependencies

**Core Dependencies (Required for both):**
```bash
pip install SpeechRecognition openai requests





