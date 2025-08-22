import json
from pyexpat.errors import messages
import sqlite3
from datetime import datetime, timedelta
from typing import List
from xmlrpc import client
from tool_database import create_db_and_tables

DB_FILE = "dummy_database.db"
create_db_and_tables()

def verify_customer(name: str, pin: str) -> int:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    first_name, last_name = name.lower().split()
    cursor.execute(
        "SELECT id FROM customers WHERE LOWER(first_name) = ? AND LOWER(last_name) = ? AND pin = ?",
        (first_name, last_name, pin),
    )
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return -1

def get_all_data(table_name: str) -> List[dict]:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    statement = f"SELECT * FROM {table_name}"
    cursor.execute(statement)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_orders(customer_id: int) -> List[dict]:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
    orders = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return orders

def check_refund_eligibility(customer_id: int, order_id: int) -> bool:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT date FROM orders WHERE id = ? AND customer_id = ?", (
            order_id, customer_id)
    )
    result = cursor.fetchone()
    conn.close()
    if not result:
        return False
    order_date = datetime.fromisoformat(result[0])
    return (datetime.now() - order_date).days <= 30

def issue_refund(customer_id: int, order_id: int) -> bool:
    print(f"Refund issued for order {order_id} for customer {customer_id}")
    return True

def share_feedback(customer_id: int, feedback: str) -> str:
    print(f"Feedback received from customer {customer_id}: {feedback}")
    return "Thank you for your feedback!"

def execute_tool_call(tool_call:dict) -> str:
    fn_name = tool_call["name"]
    fn_args = tool_call["arguments"]

    if fn_name in available_functions:
        function_to_call = available_functions[fn_name]
        try:
            print(f"Calling {fn_name} with arguments: {fn_args}")
            return str(function_to_call(**fn_args))
        except Exception as e:
            return f"Error calling {fn_name}: {e}"

    return f"Unknown tool: {fn_name}"

available_functions = {
    "verify_customer": verify_customer,
    "get_orders": get_orders,
    "check_refund_eligibility": check_refund_eligibility,
    "issue_refund": issue_refund,
    "share_feedback": share_feedback,
    "get_all_data": get_all_data,
}

tools = [
    {
        "type": "function",
        "function":{
            "name": "verify_customer",
            "description": "Verifies a customer's identity using their full name and PIN.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The customer's full name, e.g., 'John Doe'.",
                    },
                    "pin": {"type": "string", "description": "The customer's PIN."},
                },
                "required": ["name", "pin"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_orders",
            "description": "Retrieves the order history for a verified customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": "The customer's unique ID.",
                    }
                },
            "required": ["customer_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_refund_eligibility",
            "description": "Checks if an order is eligible for a refund based on the order date.",
            "parameters": {
                "type": "object",
                "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "The customer's unique ID.",
                },
                "order_id": {
                    "type": "integer",
                    "description": "The unique ID of the order.",
                },
            },
            "required": ["customer_id", "order_id"],
        },
    },
    },
    {
        "type": "function",
        "function": {
            "name": "issue_refund",
            "description": "Issues a refund for an order.",
            "parameters": {
                "type": "object",
                "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "The customer's unique ID.",
                },
                "order_id": {
                    "type": "integer",
                    "description": "The unique ID of the order.",
                },
            },
            "required": ["customer_id", "order_id"],
        },
    },
    },
    {
        "type": "function",
        "function": {
            "name": "share_feedback",
            "description": "Allows a customer to provide feedback about their experience.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": "The customer's unique ID.",
                    },
                    "feedback": {
                        "type": "string",
                        "description": "The feedback text from the customer.",
                    },
                },
            "required": ["customer_id", "feedback"],
        },
    },
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_data",
            "description": "Retrieves the entire data from a table in database. It could be either 'customers', 'orders', or 'products'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "The name of the table in database.",
                    }
                },
            "required": ["table_name"],
            },
        },
    },
]

def main():
    messages = [
        {
            "role": "developer",
            "content": """
                You are a friendly and helpful customer service agent. 
                You must ALWAYS verify the customer's identity before providing any sensitive information. 
                You MUST NOT expose any information to unverified customers.
                You MUST NOT provide any information that is not related to the customer's question.
                DON'T guess any information - neither customer nor order related (or anything else).
                If you can't perform a certain customer or order-related task, you must direct the user to a human agent.
                Ask for confirmation before performing any key actions.
                If you can't help a customer or if a customer is asking for something that is not related to the customer service, you MUST say "I'm sorry, I can't help with that."
            """}
    ]

    print("Welcome to the customer service chatbot! How can we help you today? Please type 'exit' to end the conversation.")
    while True:
        user_input = input("Your input: ")
        if user_input.lower() == "exit":
            print("Thank you for using the customer service chatbot. Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})
        for _ in range(5):  # limit tool call / assistant cycles to prevent infinite loops
            response: ChatResponse = chat(
                model='llama3.1',
                messages=messages,
                tools=tools,
            )

            output = response.message.tool_calls
            if output:
                for reply in output:
                    if reply.function:
                        tool_call = {
                            "name": reply.function.name,
                            "arguments": reply.function.arguments,
                        }
                        result = execute_tool_call(tool_call)
                        messages.append({
                            "role": "tool",
                            "content": result,
                            "tool_name": reply.function.name,
                        })
                    else:
                        messages.append({"role": "assistant", "content": reply})
                        print('Received Not a Function tool call:', reply)
            else:
                break  # Exit the loop if no tool calls are made
        print('Final response:', result)

if __name__ == "__main__":
    main()