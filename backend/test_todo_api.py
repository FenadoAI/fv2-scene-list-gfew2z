import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_todo_api():
    print("Testing Todo API endpoints...")
    
    # Test GET todos (empty list initially)
    print("\n1. Testing GET /todos (should be empty initially)")
    response = requests.get(f"{BASE_URL}/todos")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test POST todo
    print("\n2. Testing POST /todos")
    new_todo = {"text": "Test todo item"}
    response = requests.post(f"{BASE_URL}/todos", json=new_todo)
    print(f"Status: {response.status_code}")
    todo_data = response.json()
    print(f"Response: {todo_data}")
    todo_id = todo_data["id"]
    
    # Test GET todos (should have one item)
    print("\n3. Testing GET /todos (should have one item)")
    response = requests.get(f"{BASE_URL}/todos")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test PUT todo (mark as completed)
    print("\n4. Testing PUT /todos/{id} (mark as completed)")
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={"completed": True})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test DELETE todo
    print("\n5. Testing DELETE /todos/{id}")
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test GET todos (should be empty again)
    print("\n6. Testing GET /todos (should be empty again)")
    response = requests.get(f"{BASE_URL}/todos")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n✅ Todo API testing completed!")

if __name__ == "__main__":
    test_todo_api()