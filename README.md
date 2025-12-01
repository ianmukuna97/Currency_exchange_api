# 🏦 Currency Exchange API

A lightweight, modular, and secure backend API for performing real-time currency conversions using external data providers such as **Fixer / APILayer**.
Built with **Python**, designed for clarity, scalability, and production-ready structure.

---

## 🚀 Features

* 🔄 **Real-time currency conversion**
* 🔑 **Secure API key handling** using `.env` variables
* 🌍 **External API integration** (Fixer / APILayer)
* ⚙️ **Custom ExchangeRateProvider class**
* ❗ **Robust error handling** (401 Unauthorized, missing key, etc.)
* 🧱 **Clean backend architecture**
* 📦 **Django/Django REST Framework compatible structure**
* 🛡 **API key protection included in `.gitignore`**

---

## 📁 Project Structure

```
project/
│── exchange/
│   ├── provider.py        # Contains ExchangeRateProvider class
│   ├── views.py           # API endpoint logic
│   ├── urls.py            # URL routing for the conversion endpoint
│── .env                   # Environment variables (NOT committed)
│── .gitignore             # Ensures .env is ignored
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation
```

---

## ⚙️ Environment Setup

### 1. **Clone the Repository**

```bash
git clone https://github.com/yourname/currency-exchange-api.git
cd currency-exchange-api
```

### 2. **Create Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3. **Install Requirements**

```bash
pip install -r requirements.txt
```

### 4. **Create `.env` File**

Create a `.env` file in the project root:

```
EXCHANGE_API_KEY=your_api_key_here
PROVIDER_URL=http://data.fixer.io/api/
```

---

## 🔧 ExchangeRateProvider Class

Handles all outbound requests to the currency provider.

```python
import requests
import os

BASE_URL = os.getenv("PROVIDER_URL", "http://data.fixer.io/api/")
API_KEY = os.getenv("EXCHANGE_API_KEY")

class ExchangeRateProvider:
    @staticmethod
    def get_latest(base="USD", symbols=None):
        try:
            url = f"{BASE_URL}latest?access_key={API_KEY}&base={base}"
            if symbols:
                url += f"&symbols={symbols}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
```

---

## 🔗 API Endpoint

### **Convert Currency**

```
GET /convert?from=USD&to=KES&amount=100
```

### **Response Example**

```json
{
  "success": true,
  "from": "USD",
  "to": "KES",
  "amount": 100,
  "rate": 153.45,
  "converted_amount": 15345
}
```

---

## 🛡 Error Handling

The API includes graceful handling for:

| Error Type       | Example                      |
| ---------------- | ---------------------------- |
| Missing API Key  | `401: missing_access_key`    |
| Unauthorized Key | `401: invalid_access_key`    |
| Invalid Currency | `400: invalid_currency_code` |
| Provider Failure | `500: provider_error`        |

---

## 🧪 Testing

Use **Postman**, **Insomnia**, or browser query:

```
http://127.0.0.1:8000/convert?from=USD&to=KES&amount=100
```

---

## 🧰 Future Enhancements

* Add caching (Redis)
* Add rate history endpoint
* Dockerize the project
* Add authentication (JWT)
* Add frontend dashboard

---

## 🤝 Contributing

Pull requests are welcome!
Feel free to fork this repo and open an issue for suggestions.

---
