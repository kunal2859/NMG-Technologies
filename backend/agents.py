import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Warning: GEMINI_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

# Initialize the Gemini model
# Using 'gemini-2.5-flash' for low latency responses, critical for voice interaction.
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
)

class IntentAgent:
    """
    Analyzes user input to determine the intent (e.g., track order, search).
    Uses conversation history to handle context (e.g., "book it").
    """
    def __init__(self):
        self.load_prompts()

    def load_prompts(self):
        try:
            with open("backend/prompts.json", "r") as f:
                prompts = json.load(f)
                self.system_prompt = prompts["intent_agent"]["system_prompt"]
        except Exception as e:
            print(f"Error loading prompts: {e}")
            # Fallback prompt if file load fails
            self.system_prompt = "You are an Intent Classification Agent."

    async def analyze(self, text, history=[]):
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-3:]])
        prompt = f"{self.system_prompt}\n\nConversation History:\n{history_text}\n\nUser Input: {text}"
        try:
            response = model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Error in IntentAgent: {e}")
            return {"intent": "chat", "entities": {"message": text}}

class ActionAgent:
    """
    Executes business logic based on the identified intent.
    Currently uses mock data, but would connect to a real DB/API in production.
    """
    def __init__(self):
        self.orders = {
            "123": {"status": "Shipped", "delivery_date": "2023-10-25", "items": ["Wireless Headphones"]},
            "456": {"status": "Processing", "delivery_date": "2023-10-28", "items": ["Gaming Mouse"]},
            "789": {"status": "Delivered", "delivery_date": "2023-10-20", "items": ["Mechanical Keyboard"]},
            "101": {"status": "Cancelled", "delivery_date": "N/A", "items": ["Bluetooth Speaker"]},
            "102": {"status": "Out for Delivery", "delivery_date": "Today", "items": ["4K Monitor"]},
            "999": {"status": "Delivered", "delivery_date": "2023-09-15", "items": ["Laptop Stand", "USB Hub"]}
        }
        self.products = [
            {"id": "p1", "name": "Wireless Headphones", "price": 59.99, "stock": "In Stock"},
            {"id": "p2", "name": "Gaming Mouse", "price": 29.99, "stock": "In Stock"},
            {"id": "p3", "name": "Mechanical Keyboard", "price": 89.99, "stock": "Low Stock"},
            {"id": "p4", "name": "USB-C Cable", "price": 9.99, "stock": "Out of Stock"},
            {"id": "p5", "name": "4K Monitor", "price": 299.99, "stock": "In Stock"},
            {"id": "p6", "name": "Bluetooth Speaker", "price": 45.00, "stock": "In Stock"},
            {"id": "p7", "name": "Laptop Stand", "price": 25.50, "stock": "In Stock"}
        ]

    def execute(self, intent_data):
        intent = intent_data.get("intent")
        entities = intent_data.get("entities", {})

        if intent == "track_order":
            order_id = entities.get("order_id")
            if not order_id:
                return {"status": "error", "message": "I need an order ID to track your package."}
           
            order = self.orders.get(str(order_id))
            if order:
                return {"status": "success", "data": order}
            else:
                return {"status": "error", "message": f"Order {order_id} not found."}

        elif intent == "search_products":
            query = entities.get("query", "").lower()
            results = [p for p in self.products if query in p["name"].lower()]
            if results:
                return {"status": "success", "data": results}
            else:
                return {"status": "empty", "message": f"No products found for '{query}'."}

        elif intent == "process_return":
            order_id = entities.get("order_id")
            if not order_id:
                return {"status": "error", "message": "Please provide the order ID for the return."}
            order = self.orders.get(str(order_id))
            if order:
                if order["status"] == "Delivered":
                    return {"status": "success", "message": f"Return initiated for Order {order_id}. You will receive a label shortly."}
                else:
                    return {"status": "error", "message": f"Order {order_id} cannot be returned yet as it is {order['status']}."}
            else:
                return {"status": "error", "message": f"Order {order_id} not found."}

        elif intent == "place_order":
            product_name = entities.get("product_name", "item")
            import random
            new_order_id = str(random.randint(1000, 9999))
            return {
                "status": "success", 
                "message": f"Order placed for {product_name}! Your Order ID is {new_order_id}. It will arrive in 3 days."
            }

        return {"status": "info", "message": "I can help with tracking orders, searching products, returns, or placing orders."}

class ResponseAgent:
    """
    Generates a natural language response based on the action result.
    Ensures the response is concise and suitable for Text-to-Speech.
    """
    def __init__(self):
        self.load_prompts()
        self.generation_config = {
            "temperature": 0.7,
            "max_output_tokens": 1024,
            "response_mime_type": "text/plain",
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=self.generation_config,
        )

    def load_prompts(self):
        try:
            with open("backend/prompts.json", "r") as f:
                prompts = json.load(f)
                self.system_prompt = prompts["response_agent"]["system_prompt"]
        except Exception as e:
            print(f"Error loading prompts: {e}")
            self.system_prompt = "You are a helpful assistant."

    async def generate_response(self, user_text, action_result):
        prompt = f"""
        {self.system_prompt}
        User Input: {user_text}
        System Action Result: {json.dumps(action_result)}

        Response:
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error in ResponseAgent: {e}")
            return "I'm sorry, I'm having trouble generating a response right now."
