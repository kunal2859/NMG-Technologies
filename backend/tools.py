import json
from datetime import datetime, timedelta
from langchain_core.tools import tool
from backend.logger import setup_logger

logger = setup_logger(__name__)

def load_inventory():
    try:
        with open("backend/car_inventory.json", "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading car inventory: {e}", exc_info=True)
        return {}

INVENTORY = load_inventory()

@tool
def get_cars_by_type(car_type: str) -> str:
    """
    Get all cars of a specific type. 
    Supported types: sedan, suv, hatchback, electric, luxury.
    Useful when user asks "what SUVs do you have?" or "show me sedans".
    """
    car_type = car_type.lower()
    logger.info(f"Tool: get_cars_by_type called for '{car_type}'")
    
    type_map = {
        "sedan": "sedans",
        "suv": "suvs",
        "hatchback": "hatchbacks",
        "electric": "electric", 
        "luxury": "luxury" 
    }
    
    search_key = type_map.get(car_type, car_type)
    
    if search_key in INVENTORY:
        cars = INVENTORY[search_key]
        logger.info(f"Found {len(cars)} cars for type {car_type}")
        return json.dumps(cars, indent=2)
    
    logger.warning(f"No cars found for type: {car_type}")
    return f"No cars found for type: {car_type}. Available types: {list(INVENTORY.keys())}"

@tool
def get_car_by_model(model_name: str) -> str:
    """
    Search for a specific car model by name.
    Useful when user asks about a specific car like "tell me about the Adventure SUV".
    """
    model_name_lower = model_name.lower()
    logger.info(f"Tool: get_car_by_model called for '{model_name}'")
    
    for category, cars in INVENTORY.items():
        for car in cars:
            if model_name_lower in car["model"].lower():
                logger.info(f"Found car: {car['model']}")
                return json.dumps(car, indent=2)
                
    logger.warning(f"Model '{model_name}' not found")
    return f"Model '{model_name}' not found in inventory."

@tool
def get_all_available_cars() -> str:
    """
    Get a list of all available cars in stock.
    Useful for general inquiries like "what cars do you have?".
    """
    logger.info("Tool: get_all_available_cars called")
    available = []
    for category, cars in INVENTORY.items():
        for car in cars:
            if car["availability"] in ["In Stock", "Limited Stock"]:
                available.append(f"{car['model']} ({car['type']})")
    
    return json.dumps(available, indent=2)

BOOKINGS = []

def _is_business_hours(dt):
    return 9 <= dt.hour < 18

def _parse_datetime(date_str, time_str):
    today = datetime.now()
    date_str = date_str.lower()
    
    if "tomorrow" in date_str:
        target_date = today + timedelta(days=1)
    elif "today" in date_str:
        target_date = today
    else:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        except:
            target_date = today + timedelta(days=1)
            
    time_str = time_str.upper().replace(" ", "")
    try:
        if "AM" in time_str or "PM" in time_str:
            time_obj = datetime.strptime(time_str, "%I%p")
        else:
            time_obj = datetime.strptime(time_str, "%H:%M")
    except:
        time_obj = datetime.strptime("10AM", "%I%p")
        
    return target_date.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)

@tool
def check_availability(date: str, time: str) -> str:
    """
    Check if a time slot is available for a test drive.
    date: 'today', 'tomorrow', or 'YYYY-MM-DD'
    time: '10 AM', '2 PM', etc.
    """
    logger.info(f"Tool: check_availability called for {date} at {time}")
    try:
        booking_datetime = _parse_datetime(date, time)
        
        if not _is_business_hours(booking_datetime):
            return "We're only open from 9 AM to 6 PM. Please choose a time within business hours."
            
        for booking in BOOKINGS:
            if booking["datetime"] == booking_datetime:
                return f"Sorry, {time} on {date} is already booked."
                
        return "Time slot is available."
    except Exception as e:
        logger.error(f"Error checking availability: {e}")
        return f"Error checking availability: {e}"

@tool
def book_test_drive(car_model: str, date: str, time: str, customer_name: str = "Guest") -> str:
    """
    Book a test drive for a specific car.
    Requires car model, date, and time.
    """
    logger.info(f"Tool: book_test_drive called for {car_model} by {customer_name} on {date} at {time}")
    
    avail_msg = check_availability.invoke({"date": date, "time": time})
    if "already booked" in avail_msg or "only open" in avail_msg:
        return avail_msg
        
    try:
        booking_datetime = _parse_datetime(date, time)
        booking_id = f"TD{len(BOOKINGS) + 1001}"
        
        booking = {
            "booking_id": booking_id,
            "customer_name": customer_name,
            "car_model": car_model,
            "date": date,
            "time": time,
            "datetime": booking_datetime,
            "status": "Confirmed"
        }
        
        BOOKINGS.append(booking)
        logger.info(f"Booking confirmed: {booking_id}")
        return f"Test drive successfully booked! Your Booking ID is {booking_id}."
        
    except Exception as e:
        logger.error(f"Booking failed: {e}")
        return f"Booking failed due to an error: {e}"

tools_list = [get_cars_by_type, get_car_by_model, get_all_available_cars, check_availability, book_test_drive]
