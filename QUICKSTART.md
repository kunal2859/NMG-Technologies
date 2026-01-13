# Quick Start Guide - Auto Dealership Voice Assistant

## Overview
This is a multi-agent voice assistant for auto dealerships that handles customer inquiries and test drive bookings through natural conversation.

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Set up environment**:
   - Copy `.env.example` to `.env`
   - Add your Groq API key: `GROQ_API_KEY=your_key_here`
   - Get free key from: https://console.groq.com/keys

3. **Run the server**:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

4. **Open browser**: http://localhost:8000

## Example Usage

### Scenario 1: Simple Inquiry
**You**: "What SUVs do you have?"  
**Agent**: "We have three excellent SUVs: the Adventure SUV with all-wheel drive, the Urban SUV Compact, and the Luxury SUV Elite."

### Scenario 2: Direct Booking
**You**: "Book a test drive for the Adventure SUV tomorrow at 11 AM"  
**Agent**: "Perfect! Your test drive for the Adventure SUV is scheduled for tomorrow at 11 AM. Booking ID: TD1001."

### Scenario 3: Multi-Step Conversation
**You**: "I want to test drive a sedan"  
**Agent**: "Great! We have the Luxury Sedan Pro, Executive Sedan, and Sport Sedan GT. Which interests you?"

**You**: "The Luxury Sedan Pro"  
**Agent**: "Excellent choice! It has a 2.0L turbocharged engine with 250 HP, leather seats, and adaptive cruise control. When would you like to test drive it?"

**You**: "Tomorrow at 2 PM"  
**Agent**: "Perfect! Your test drive is confirmed for tomorrow at 2 PM. Booking ID: TD1002."

## Architecture

The system uses **LangChain** with a tool-calling agent powered by Groq's `openai/gpt-oss-20b` model:

- **LangChain Agent** - Handles reasoning, tool selection, and response generation
- **Tools** - Inventory search, booking management, availability checking
- **STT/TTS** - Faster-Whisper for speech-to-text, Edge TTS for text-to-speech

## Available Cars

- **Sedans**: Luxury Sedan Pro ($45k), Executive Sedan ($52k), Sport Sedan GT ($38k)
- **SUVs**: Adventure SUV ($48k), Urban SUV Compact ($32k), Luxury SUV Elite ($68k)
- **Hatchbacks**: City Hatchback ($22k), Sport Hatchback RS ($28k)
- **Electric**: EcoElectric Sedan ($55k), EcoElectric SUV ($72k)
- **Luxury**: Presidential Luxury Sedan ($95k)

## Key Features

✅ Real-time voice interaction (STT + TTS)  
✅ Context-aware conversations  
✅ Smart booking with availability validation  
✅ Comprehensive car knowledge base  
✅ Multi-agent collaboration  

## Testing

Try these voice commands:
- "What electric cars do you have?"
- "Tell me about the Adventure SUV"
- "Book a test drive for tomorrow at 3 PM"
- "Compare the Luxury Sedan Pro and Executive Sedan"

## Documentation

- **README.md** - Full project documentation
- **writeup.md** - Technical implementation details
- **test_scenarios.md** - 11 comprehensive test cases
- **walkthrough.md** - Complete implementation walkthrough
