# test_currency_api.py
import requests

def test_currency_api():
    """Test frankfurter.app API before integrating"""
    
    # Simple conversion
    response = requests.get('https://api.frankfurter.app/latest?from=USD&to=EUR')
    print("USD to EUR:")
    print(response.json())
    
    # Multiple currencies
    response = requests.get('https://api.frankfurter.app/latest?from=USD&to=EUR,GBP,INR')
    print("\nUSD to multiple currencies:")
    print(response.json())
    
    # Available currencies
    response = requests.get('https://api.frankfurter.app/currencies')
    print("\nAvailable currencies:")
    print(response.json())

if __name__ == "__main__":
    test_currency_api()