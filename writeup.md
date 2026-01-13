# Auto Dealership Voice Assistant - Implementation Writeup

## Project Overview

This project implements a sophisticated multi-agent voice assistant system designed for auto dealerships to handle customer inquiries and test drive bookings through natural voice conversations. The system demonstrates autonomous agent collaboration, real-time voice processing, and intelligent workflow orchestration.

## Multi-Agent Architecture

### Design Philosophy

The system is built on a **multi-agent architecture** where specialized agents collaborate autonomously to handle complex customer interactions. This approach provides:

- **Separation of Concerns**: Each agent has a specific responsibility
- **Scalability**: New agents can be added without modifying existing ones
- **Maintainability**: Agent logic is isolated and testable
- **Flexibility**: Agents can be composed in different ways for different workflows

### Agent Roles and Responsibilities

#### 1. IntentAgent (Conversational Agent)
**Purpose**: Natural language understanding and intent classification

**Capabilities**:
- Analyzes customer speech to identify intent
- Extracts structured entities from unstructured text
- Maintains conversation context for multi-turn dialogues
- Resolves references (e.g., "that SUV", "book it")

**Intents Supported**:
- `inquire_car`: Customer wants information about vehicles
- `book_test_drive`: Customer wants to schedule a test drive
- `check_availability`: Check time slot availability
- `compare_models`: Compare different car models
- `chat`: General conversation/greetings

**Example**:
```
Input: "I want to book a test drive for an SUV tomorrow at 11 AM"
Output: {
  "intent": "book_test_drive",
  "entities": {
    "car_type": "suv",
    "date": "tomorrow",
    "time": "11 AM"
  }
}
```

#### 2. KnowledgeAgent
**Purpose**: Vehicle information retrieval and management

**Capabilities**:
- Queries car inventory database (JSON-based)
- Filters by vehicle type (sedan, suv, hatchback, electric, luxury)
- Retrieves detailed specifications and features
- Supports model search and comparison

**Data Structure**:
The knowledge base contains 15+ vehicle models with:
- Model name and variant
- Engine/motor specifications
- Features (safety, technology, interior)
- Pricing and availability
- Available colors

**Methods**:
- `get_cars_by_type(car_type)`: Returns all cars of a specific type
- `get_car_by_model(model_name)`: Finds a specific model
- `get_all_available_cars()`: Returns in-stock vehicles
- `search_cars(query)`: Flexible search across all fields

#### 3. BookingAgent
**Purpose**: Test drive appointment scheduling and calendar management

**Capabilities**:
- Validates date/time availability
- Prevents double-booking
- Manages business hours (9 AM - 6 PM)
- Generates unique booking IDs
- Stores appointments in-memory (easily extensible to database)

**Key Features**:
- **Smart Date Parsing**: Handles relative dates ("tomorrow", "today")
- **Time Validation**: Ensures bookings fall within business hours
- **Conflict Detection**: Checks for existing appointments
- **Booking Confirmation**: Returns booking ID and details

**Example Booking**:
```json
{
  "booking_id": "TD1001",
  "customer_name": "John Doe",
  "car_model": "Adventure SUV",
  "date": "tomorrow",
  "time": "11 AM",
  "status": "Confirmed"
}
```

#### 4. ActionAgent (Orchestrator)
**Purpose**: Coordinates agent collaboration and workflow execution

**Responsibilities**:
- Receives intent data from IntentAgent
- Delegates to appropriate specialist agents
- Combines results from multiple agents
- Handles multi-step workflows

**Workflow Examples**:

**Simple Inquiry**:
```
IntentAgent → ActionAgent → KnowledgeAgent → ResponseAgent
```

**Test Drive Booking**:
```
IntentAgent → ActionAgent → BookingAgent → ResponseAgent
```

**Complex Multi-Step**:
```
1. Customer: "I want to test drive a sedan"
   IntentAgent → ActionAgent → KnowledgeAgent (lists sedans)
   
2. Customer: "Book the Luxury Sedan Pro for tomorrow at 2 PM"
   IntentAgent (resolves model from context) → ActionAgent → BookingAgent
```

#### 5. ResponseAgent
**Purpose**: Natural language generation for voice output

**Capabilities**:
- Converts structured data into conversational responses
- Optimized for Text-to-Speech (concise, natural)
- Professional and sales-oriented tone
- Contextual awareness

**Design Considerations**:
- Responses limited to 2-3 sentences for voice clarity
- Avoids markdown and special characters that TTS struggles with
- Highlights key information without overwhelming details
- Maintains friendly, helpful tone

## Voice Processing Pipeline

### Speech-to-Text (STT)
**Technology**: Faster-Whisper

**Why Faster-Whisper?**
- Optimized implementation of OpenAI's Whisper
- 4x faster than standard Whisper on CPU
- No API costs or latency
- Excellent accuracy for conversational speech

**Configuration**:
- Model: `base` (balance of speed and accuracy)
- Device: `cpu` (no GPU required)
- Compute type: `int8` (optimized for CPU)

### Text-to-Speech (TTS)
**Technology**: Microsoft Edge TTS

**Why Edge-TTS?**
- High-quality neural voices
- Completely free (no API limits)
- Natural-sounding speech
- Low latency

**Voice**: `en-US-AriaNeural` (professional, friendly female voice)

## Real-Time Communication

### WebSocket Architecture

**Why WebSockets?**
- Bidirectional communication for natural conversation flow
- Low latency (critical for voice interaction)
- Persistent connection reduces overhead
- Supports streaming audio

**Flow**:
1. Frontend captures audio via MediaRecorder API
2. Audio blob sent to backend via WebSocket
3. Backend processes through agent pipeline
4. Response (text + audio URL) sent back via WebSocket
5. Frontend plays audio response

### Session Management

Each client session maintains:
- **Session ID**: Unique identifier
- **Conversation History**: For context-aware responses
- **User Requests**: Tracking customer inquiries
- **Operations Performed**: Agent actions taken
- **Agent Flow**: Sequence of agents involved

This enables:
- Context resolution across multiple turns
- Session summaries for analytics
- Debugging and monitoring

## Knowledge Base Design

### Structure

The car inventory is organized by category for efficient querying:

```json
{
  "sedans": [...],
  "suvs": [...],
  "hatchbacks": [...],
  "electric": [...],
  "luxury": [...]
}
```

### Vehicle Schema

Each vehicle contains:
```json
{
  "id": "unique_identifier",
  "model": "Model Name",
  "variant": "Trim Level",
  "type": "category",
  "price": "$XX,XXX",
  "features": {
    "engine": "specifications",
    "transmission": "type",
    "safety": "features",
    "technology": "features",
    "interior": "features"
  },
  "availability": "In Stock | Limited Stock",
  "colors": ["available colors"]
}
```

### Extensibility

The JSON-based knowledge base can easily be:
- Migrated to a database (PostgreSQL, MongoDB)
- Updated with real-time inventory
- Extended with additional fields (VIN, location, images)
- Integrated with dealership management systems

## Booking System Implementation

### Calendar Management

**Current Implementation**: In-memory storage
- Fast access for demonstration
- No external dependencies
- Easy to understand

**Production-Ready Extensions**:
- Database persistence (PostgreSQL with datetime indexing)
- Google Calendar API integration
- SMS/Email confirmation notifications
- CRM system integration

### Availability Logic

```python
def check_availability(date, time):
    1. Parse date/time (handle "tomorrow", "today")
    2. Validate business hours (9 AM - 6 PM)
    3. Check for conflicts with existing bookings
    4. Return availability status
```

### Booking Workflow

```
1. Customer expresses interest in test drive
2. System confirms car model (from context or explicit)
3. Customer provides date/time
4. BookingAgent validates availability
5. If available: Create booking, generate ID
6. If unavailable: Suggest alternative times
7. Confirm booking details via voice
```

## Technical Implementation Details

### Asynchronous Processing

The system uses Python's `async/await` for non-blocking operations:
- STT transcription
- AI model inference (Gemini)
- TTS generation
- WebSocket communication

This ensures:
- Responsive user experience
- Efficient resource utilization
- Scalability for multiple concurrent users

### Error Handling

Robust error handling at each layer:
- **STT Failure**: Fallback message "I didn't hear anything"
- **Intent Classification Error**: Default to `chat` intent
- **Knowledge Base Error**: Graceful error messages
- **Booking Conflict**: Suggest alternatives
- **TTS Error**: Log error, return text response

### Prompt Engineering

**IntentAgent Prompt**:
- Clear intent definitions with examples
- Entity extraction guidelines
- Context resolution instructions
- JSON output format specification

**ResponseAgent Prompt**:
- Persona definition (professional, helpful)
- Response length constraints
- TTS optimization guidelines
- Sales-oriented tone

## Testing and Validation

### Test Scenarios

1. **Simple Inquiry**: "What SUVs do you have?"
2. **Specific Model**: "Tell me about the Adventure SUV"
3. **Direct Booking**: "Book a test drive for tomorrow at 11 AM"
4. **Multi-Step Booking**: 
   - "I want to test drive a sedan"
   - "Book the Luxury Sedan Pro for 2 PM tomorrow"
5. **Context Resolution**: "Book it for 3 PM" (after discussing a model)

### Verification Points

- ✅ Voice transcription accuracy
- ✅ Intent classification correctness
- ✅ Knowledge base query results
- ✅ Booking validation logic
- ✅ Response naturalness
- ✅ TTS audio quality
- ✅ Session context maintenance

## Future Enhancements

### Short-Term
- Database integration for persistent bookings
- Email/SMS confirmation notifications
- Multi-language support
- Voice customization options

### Long-Term
- Integration with dealership CRM systems
- Real-time inventory synchronization
- Video call integration for virtual test drives
- AI-powered vehicle recommendations based on customer preferences
- Analytics dashboard for dealership managers

## Conclusion

This multi-agent voice assistant demonstrates a production-ready architecture for handling complex customer interactions in the automotive industry. The modular design, autonomous agent collaboration, and real-time voice processing create a natural and efficient customer experience while maintaining code quality and extensibility.
