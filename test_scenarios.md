# Walkthrough - Voice AI Agent

## Testing Scenarios

### 1. Track Order
*   **Scenario**: Checking a shipped order.
    *   **Say**: "Where is my order 123?"
    *   **Expected**: "Your order 123 is Shipped and will arrive on 2023-10-25."
*   **Scenario**: Checking an order out for delivery.
    *   **Say**: "Status of order 102."
    *   **Expected**: "Order 102 is Out for Delivery today!"

### 2. Search Product
*   **Scenario**: Finding an in-stock item.
    *   **Say**: "Do you have any gaming mice?"
    *   **Expected**: "Yes, we have a Gaming Mouse for $29.99."
*   **Scenario**: Finding a high-end item.
    *   **Say**: "I need a monitor."
    *   **Expected**: "We have a 4K Monitor available for $299.99."
*   **Scenario**: Checking stock.
    *   **Say**: "Is the USB cable in stock?"
    *   **Expected**: "Sorry, the USB-C Cable is currently Out of Stock."

### 3. Place Order (New!)
*   **Scenario**: Booking an item from context.
    *   **Step 1 Say**: "Do you have any gaming mice?"
    *   **Step 1 Expected**: "Yes, we have a Gaming Mouse..."
    *   **Step 2 Say**: "Yes, please book it for me."
    *   **Step 2 Expected**: "Order placed for Gaming Mouse! Your Order ID is [Random]. It will arrive in 3 days."

### 4. Return Item
*   **Scenario**: Returning a delivered item.
    *   **Say**: "I want to return order 789."
    *   **Expected**: "Return initiated for Order 789. You will receive a label shortly."
*   **Scenario**: Trying to return a processing order.
    *   **Say**: "Return order 456."
    *   **Expected**: "Order 456 cannot be returned yet as it is Processing."

### 5. General Chat
*   **Scenario**: Greeting.
    *   **Say**: "Hello, who are you?"
    *   **Expected**: "I am ShopAssist, your virtual customer support agent. How can I help you today?"

## Mock Data Reference
| Order ID | Status | Item |
| :--- | :--- | :--- |
| **123** | Shipped | Wireless Headphones |
| **456** | Processing | Gaming Mouse |
| **789** | Delivered | Mechanical Keyboard |
| **101** | Cancelled | Bluetooth Speaker |
| **102** | Out for Delivery | 4K Monitor |
| **999** | Delivered | Laptop Stand |
