# 🧪 API Tester CLI Tool



A lightweight, terminal-based API testing tool that mimics basic functionality of Postman. Supports GET, POST, PUT, DELETE, request history, JSON input/output, auth headers, and curl command generation.



---



## ✅ Features



* 🟢 Supports all major HTTP methods

* 🔐 Supports Basic and Bearer Token Authentication

* 🖍 Pretty-prints responses using `rich`

* 📜 Saves last 5 request histories

* 📋 Generates curl equivalent command for reuse

* 🧠 Input headers and data in JSON format



---



## 📦 Requirements



Python 3.7+



Install dependencies:



```bash

pip install -r requirements.txt

```



`requirements.txt`:



```

requests

rich

```



---



## 🚀 Usage



\### 🔎 Basic GET Request



```bash

python apitest.py --method GET --url https://api.github.com

```



### 📬 POST Request with JSON Body



```bash

python apitest.py --method POST --url https://httpbin.org/post --data '{"name": "Aayushman"}'

```



### 🔐 With Headers and Bearer Token



```bash

python apitest.py --method GET --url https://api.example.com/data \\

    --headers '{"Accept": "application/json"}' \\

    --bearer YOUR\_TOKEN\_HERE

```



### 🧾 Basic Authentication



```bash

python apitest.py --method GET --url https://httpbin.org/basic-auth/user/pass --auth user:pass

```



### 📜 View Request History



```bash

python apitest.py --history

```



---



## 🧰 Example Output



* Status Code

* Time Taken

* Response Size

* Content-Type

* Response Body (formatted JSON if applicable)

* Curl Command for the request



---



## 📂 Project Structure



```

├── apitest.py              # Main CLI script

├── requirements.txt        # Python dependencies

└── ~/.apitest\_history.json # History file (auto-generated)

```



---




