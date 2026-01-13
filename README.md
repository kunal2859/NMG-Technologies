# Auto Dealership Voice Assistant - Multi-Agent Test Drive Booking System

A real-time voice-based AI agent system for auto dealerships that enables customers to inquire about vehicles and book test drives through natural conversation. Built with a sophisticated multi-agent architecture for autonomous collaboration.

## Scenario

A customer calls an auto dealership. The voice agent:

1. **Greets** the customer and understands their intent (e.g., "I want to book a test drive for a sedan")
2. **Queries** the knowledge base to provide details about available models and features
3. **Confirms** details (model, date, time)
4. **Books** the test drive in the calendar system
5. **Responds** in voice with confirmation

## Core Features

### Voice Interaction
- **Speech-to-Text (STT)**: Faster-Whisper for accurate transcription
- **Text-to-Speech (TTS)**: Edge-TTS for natural voice responses
- Real-time audio streaming via WebSockets

### Multi-Agent Architecture

The system uses **autonomous agent collaboration** where agents work together to handle complex workflows:

#### 1. **Conversational Agent (IntentAgent)**
- Understands customer intent from natural language
- Extracts entities (car type, model, date, time, customer name)
- Maintains conversation context for multi-turn dialogues

#### 2. **Knowledge Agent (KnowledgeAgent)**
- Queries comprehensive car inventory database
- Provides detailed information about models, variants, and features
- Supports filtering by type (Sedan, SUV, Hatchback, Electric, Luxury)
- Handles model comparisons

#### 3. **Booking Agent (BookingAgent)**
- Schedules test drive appointments
- Validates date/time availability
- Prevents double-booking with calendar management
- Confirms bookings with unique IDs

#### 4. **Action Agent (ActionAgent)**
- Orchestrates collaboration between Knowledge and Booking agents
- Delegates tasks based on intent
- Coordinates multi-step workflows

#### 5. **Response Agent (ResponseAgent)**
- Generates natural, conversational responses
- Optimized for voice output (concise, TTS-friendly)
- Professional and sales-oriented tone

### Knowledge Base

Comprehensive JSON database with **15+ vehicle models** across 5 categories:
- **Sedans**: Luxury Sedan Pro, Executive Sedan, Sport Sedan GT
- **SUVs**: Adventure SUV, Urban SUV Compact, Luxury SUV Elite
- **Hatchbacks**: City Hatchback, Sport Hatchback RS
- **Electric**: EcoElectric Sedan, EcoElectric SUV
- **Luxury**: Presidential Luxury Sedan

Each model includes:
- Detailed specifications (engine, transmission, drivetrain)
- Features (safety, technology, interior)
- Pricing and availability
- Available colors

## Example Conversation Flow

**Customer**: "I want to book a test drive for an SUV tomorrow at 11 AM."

**System Processing**:
1. **STT**: Converts speech to text
2. **IntentAgent**: Identifies intent → `book_test_drive`, entities → `{car_type: "suv", date: "tomorrow", time: "11 AM"}`
3. **ActionAgent**: Delegates to KnowledgeAgent → Lists available SUVs
4. **ResponseAgent**: "We have several great SUVs available! The Adventure SUV, Urban SUV Compact, and Luxury SUV Elite. Which one would you like to test drive?"

**Customer**: "The Adventure SUV"

**System Processing**:
1. **IntentAgent**: Resolves "The Adventure SUV" from context
2. **ActionAgent**: Delegates to BookingAgent → Checks availability, creates booking
3. **ResponseAgent**: "Perfect! Your test drive for the Adventure SUV is scheduled for tomorrow at 11 AM. Your booking ID is TD1001."
4. **TTS**: Generates audio response

## Technologies Used & Rationale

- **Python (FastAPI)**: High-performance async framework for real-time WebSocket connections
- **WebSockets**: Bidirectional audio streaming for natural conversation flow
- **Google Gemini 2.5 Flash**: Low-latency AI model with generous free tier
- **Faster-Whisper**: Optimized Whisper implementation for fast CPU-based transcription
- **Edge-TTS**: High-quality neural voices at no cost

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
*Note: You may need to install `ffmpeg` on your system for audio processing.*

### 2. Environment Variables
- Rename `.env.example` to `.env`
- Add your Google Gemini API Key:
  ```
  GEMINI_API_KEY=your_key_here
  ```
- Get a free key from [Google AI Studio](https://aistudio.google.com/)

### 3. Run the Server
```bash
uvicorn backend.main:app --reload
```

### 4. Use the Application
- Open browser to `http://localhost:8000`
- Click and hold "Hold to Speak" button
- Try: "What SUVs do you have?" or "Book a test drive for tomorrow at 2 PM"

## Architecture

```text
+----------+       +----------+       +---------+
|  Customer| <---> | Frontend | <---> | Backend |
+----------+       +----------+       +----+----+
                                           |
                                           v
                                    +-------------+
                                    | Orchestrator|
                                    +------+------+
                                           |
         +---------------------------------+----------------------------------+
         |                                 |                                  |
         v                                 v                                  v
  +-------------+                   +-------------+                    +-------------+
  | STT Service |                   | Intent Agent|                    |Response Agt |
  +-------------+                   +------+------+                    +-------------+
                                           |
                         +-----------------+-----------------+
                         |                                   |
                         v                                   v
                  +-------------+                     +-------------+
                  |Knowledge Agt|                     | Booking Agt |
                  +-------------+                     +-------------+
                         |                                   |
                         v                                   v
                  +-------------+                     +-------------+
                  |Car Inventory|                     |  Calendar   |
                  +-------------+                     +-------------+
```

### Agent Collaboration Flow

1. **Frontend** captures audio → sends via WebSocket
2. **STT Service** transcribes audio to text
3. **IntentAgent** classifies intent and extracts entities
4. **ActionAgent** delegates to appropriate specialist:
   - **KnowledgeAgent** for car inquiries
   - **BookingAgent** for test drive scheduling
5. **ResponseAgent** generates natural language response
6. **TTS Service** converts text to speech
7. **Frontend** plays audio response

## Mock Data

### Sample Car Models
- **Adventure SUV**: 3.5L V6, AWD, 7 passengers, $48,000
- **Luxury Sedan Pro**: 2.0L Turbo, Premium features, $45,000
- **EcoElectric Sedan**: 450 HP Dual Motor, 350-mile range, $55,000

### Sample Bookings
Test drive appointments are stored in-memory with:
- Booking ID (e.g., TD1001)
- Customer name
- Car model
- Date and time
- Status (Confirmed)

## Key Differentiators

✅ **Multi-Agent Architecture**: Autonomous agents collaborate to handle complex workflows
✅ **Context-Aware**: Remembers conversation history to resolve references like "that one" or "book it"
✅ **Real-Time Voice**: Natural conversation flow with minimal latency
✅ **Comprehensive Knowledge Base**: Detailed vehicle information across multiple categories
✅ **Smart Booking System**: Validates availability and prevents conflicts
✅ **Free & Open-Source**: Runs entirely on free/open-source models and APIs
