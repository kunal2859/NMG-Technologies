# Auto Dealership Voice Assistant - Test Scenarios

This document provides comprehensive test scenarios to validate the multi-agent voice assistant system for auto dealership test drive booking.

## Test Scenario 1: Simple Car Inquiry

**Customer Input**: "What SUVs do you have?"

**Expected Flow**:
1. STT transcribes the question
2. IntentAgent identifies: `intent: "inquire_car"`, `entities: {car_type: "suv"}`
3. ActionAgent delegates to KnowledgeAgent
4. KnowledgeAgent returns all SUV models (Adventure SUV, Urban SUV Compact, Luxury SUV Elite)
5. ResponseAgent generates natural response listing the SUVs
6. TTS converts to speech

**Expected Response**: "We have three excellent SUVs available: the Adventure SUV with all-wheel drive and seating for seven, the Urban SUV Compact perfect for city driving, and our premium Luxury SUV Elite with advanced features."

---

## Test Scenario 2: Specific Model Inquiry

**Customer Input**: "Tell me about the Adventure SUV"

**Expected Flow**:
1. IntentAgent identifies: `intent: "inquire_car"`, `entities: {model_name: "Adventure SUV"}`
2. ActionAgent → KnowledgeAgent retrieves specific model details
3. ResponseAgent highlights key features

**Expected Response**: "The Adventure SUV features a powerful 3.5-liter V6 engine with 295 horsepower, all-wheel drive, and seats seven passengers. It includes adaptive cruise control, a 12-inch touchscreen with navigation, and leather seats. It's priced at $48,000 and we have it in stock."

---

## Test Scenario 3: Direct Test Drive Booking

**Customer Input**: "I want to book a test drive for an SUV tomorrow at 11 AM"

**Expected Flow**:
1. IntentAgent identifies: `intent: "book_test_drive"`, `entities: {car_type: "suv", date: "tomorrow", time: "11 AM"}`
2. ActionAgent recognizes car_type but not specific model
3. KnowledgeAgent lists available SUVs
4. ResponseAgent asks for clarification

**Expected Response**: "I'd be happy to schedule a test drive for you! We have the Adventure SUV, Urban SUV Compact, and Luxury SUV Elite available. Which one would you like to test drive?"

**Follow-up Input**: "The Adventure SUV"

**Expected Flow**:
1. IntentAgent resolves model from context
2. ActionAgent → BookingAgent validates availability and creates booking
3. ResponseAgent confirms with booking ID

**Expected Response**: "Perfect! Your test drive for the Adventure SUV is scheduled for tomorrow at 11 AM. Your booking ID is TD1001. We'll see you then!"

---

## Test Scenario 4: Multi-Step Booking Workflow

**Step 1 - Customer Input**: "I want to test drive a sedan"

**Expected Response**: "Great choice! We have three sedans available: the Luxury Sedan Pro with turbocharged performance, the Executive Sedan with premium features, and the Sport Sedan GT. Which one interests you?"

**Step 2 - Customer Input**: "Tell me more about the Luxury Sedan Pro"

**Expected Response**: "The Luxury Sedan Pro has a 2.0-liter turbocharged engine with 250 horsepower, an 8-speed automatic transmission, and gets 28 MPG city. It features adaptive cruise control, a 12.3-inch touchscreen, leather seats, and a power sunroof. It's priced at $45,000."

**Step 3 - Customer Input**: "Book it for tomorrow at 2 PM"

**Expected Flow**:
1. IntentAgent resolves "it" to "Luxury Sedan Pro" from conversation history
2. BookingAgent validates time slot and creates booking

**Expected Response**: "Excellent! Your test drive for the Luxury Sedan Pro is confirmed for tomorrow at 2 PM. Your booking ID is TD1002."

---

## Test Scenario 5: Context Resolution

**Conversation Flow**:

**Customer**: "What electric cars do you have?"
**Agent**: "We have two electric vehicles: the EcoElectric Sedan with a 350-mile range and the EcoElectric SUV with a 400-mile range and tri-motor all-wheel drive."

**Customer**: "How much is the sedan?"
**Agent**: "The EcoElectric Sedan is priced at $55,000."

**Customer**: "Book a test drive for that one tomorrow at 3 PM"
**Agent**: "Perfect! Your test drive for the EcoElectric Sedan is scheduled for tomorrow at 3 PM. Your booking ID is TD1003."

**Validation**: System correctly resolves "the sedan" and "that one" from conversation context.

---

## Test Scenario 6: Availability Check

**Customer Input**: "Is 10 AM available tomorrow?"

**Expected Flow**:
1. IntentAgent identifies: `intent: "check_availability"`, `entities: {date: "tomorrow", time: "10 AM"}`
2. BookingAgent checks calendar
3. Returns availability status

**Expected Response** (if available): "Yes, 10 AM tomorrow is available for a test drive. Which car would you like to test drive?"

**Expected Response** (if booked): "I'm sorry, 10 AM tomorrow is already booked. We have availability at 11 AM, 2 PM, or 4 PM. Would any of those work for you?"

---

## Test Scenario 7: Outside Business Hours

**Customer Input**: "Can I book a test drive for 8 PM tomorrow?"

**Expected Flow**:
1. BookingAgent validates time against business hours (9 AM - 6 PM)
2. Returns error with business hours information

**Expected Response**: "I'm sorry, we're only open from 9 AM to 6 PM. Would you like to schedule during our business hours instead?"

---

## Test Scenario 8: Model Comparison

**Customer Input**: "Compare the Adventure SUV and the Luxury SUV Elite"

**Expected Flow**:
1. IntentAgent identifies: `intent: "compare_models"`, `entities: {model1: "Adventure SUV", model2: "Luxury SUV Elite"}`
2. KnowledgeAgent retrieves both models
3. ResponseAgent highlights key differences

**Expected Response**: "The Adventure SUV has a 3.5-liter V6 with 295 horsepower and is priced at $48,000, while the Luxury SUV Elite features a twin-turbo V6 with 400 horsepower, premium Nappa leather, massaging seats, and is priced at $68,000. Both seat seven passengers and have all-wheel drive."

---

## Test Scenario 9: General Conversation

**Customer Input**: "Hello, how are you?"

**Expected Flow**:
1. IntentAgent identifies: `intent: "chat"`
2. ResponseAgent generates friendly greeting

**Expected Response**: "Hello! I'm doing great, thank you for asking! I'm here to help you explore our vehicle inventory and schedule test drives. What can I help you with today?"

---

## Test Scenario 10: Hatchback Inquiry

**Customer Input**: "Do you have any sporty hatchbacks?"

**Expected Flow**:
1. IntentAgent identifies: `intent: "inquire_car"`, `entities: {car_type: "hatchback"}`
2. KnowledgeAgent filters for hatchbacks
3. ResponseAgent highlights sporty option

**Expected Response**: "Yes! We have the Sport Hatchback RS with a turbocharged 1.6-liter engine producing 201 horsepower, a 6-speed manual transmission, and sport bucket seats. It's priced at $28,000 and perfect for enthusiasts."

---

## Test Scenario 11: Complete End-to-End Workflow

**Full Conversation**:

1. **Customer**: "Hi, I'm looking for a family car"
   **Agent**: "Hello! I'd be happy to help. For families, I'd recommend our SUVs or sedans. We have spacious options with great safety features. Would you prefer an SUV or sedan?"

2. **Customer**: "An SUV would be better"
   **Agent**: "Excellent choice! We have the Adventure SUV that seats seven, the compact Urban SUV for five, and the luxury Luxury SUV Elite. The Adventure SUV is very popular with families."

3. **Customer**: "What safety features does the Adventure SUV have?"
   **Agent**: "The Adventure SUV includes adaptive cruise control, lane keep assist, blind spot monitoring, rear cross traffic alert, and hill descent control. It also has a 360-degree camera system."

4. **Customer**: "That sounds perfect. Can I test drive it tomorrow at 11 AM?"
   **Agent**: "Absolutely! Your test drive for the Adventure SUV is confirmed for tomorrow at 11 AM. Your booking ID is TD1001. We look forward to seeing you!"

5. **Customer**: "Thank you!"
   **Agent**: "You're very welcome! See you tomorrow at 11 AM. Have a great day!"

---

## Validation Checklist

For each test scenario, verify:

- [ ] STT accurately transcribes customer speech
- [ ] IntentAgent correctly identifies intent
- [ ] IntentAgent extracts all relevant entities
- [ ] ActionAgent delegates to appropriate specialist agent
- [ ] KnowledgeAgent returns accurate data from inventory
- [ ] BookingAgent validates availability correctly
- [ ] BookingAgent prevents double-booking
- [ ] ResponseAgent generates natural, concise responses
- [ ] TTS produces clear, natural-sounding audio
- [ ] Conversation context is maintained across turns
- [ ] Session summary captures all interactions

---

## Performance Metrics

Target benchmarks:
- **STT Latency**: < 2 seconds
- **Intent Classification**: < 1 second
- **Knowledge Query**: < 0.5 seconds
- **Booking Validation**: < 0.5 seconds
- **Response Generation**: < 2 seconds
- **TTS Generation**: < 3 seconds
- **Total Round-Trip**: < 8 seconds

---

## Edge Cases to Test

1. **Ambiguous Input**: "I want the blue one" (without prior context)
2. **Multiple Entities**: "Book the sedan or SUV for tomorrow"
3. **Invalid Date**: "Book for yesterday"
4. **Incomplete Information**: "Book a test drive" (missing model, date, time)
5. **Model Name Variations**: "Adventure" vs "Adventure SUV" vs "the adventure"
6. **Time Format Variations**: "11 AM" vs "11:00 AM" vs "eleven in the morning"
