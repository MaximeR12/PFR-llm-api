import unittest
import json
from fastapi.testclient import TestClient  # assuming that the FastAPI app is in a file named main.py
import main

def get_unitest_token(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if 'tokens' in data and 'unitest' in data['tokens']:
                return data['tokens']['unitest']
            else:
                return None
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"The file '{file_path}' is not a valid JSON file.")
        return None
    

class TestFastAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)

    def test_ollama_chat(self):
    
        # Define a sample script
        sample_script = {"script": "INSERT INTO test_target FROM test_source"}

        # Test with a valid token and script
        valid_token = {"Authorization" : f"Bearer {get_unitest_token('main/tokens.json')}"}
        response = self.client.post("/script_analyse", json=sample_script, headers=valid_token)
        print(response)
        self.assertEqual(response.status_code, 200)

        # Test with an invalid token
        invalid_token = {"Authorization" : "Bearer cACab0ud1"}
        response = self.client.post("/script_analyse", json=sample_script, headers=invalid_token)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
