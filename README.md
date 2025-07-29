# 📱 Refurbished Phone Listing Helper

A Streamlit-based web app that helps you decide where to list refurbished phones for resale by calculating platform-specific prices, fees, and profit margins. Easily view stock, grading conditions, and get clear listability suggestions.

## 🔑 Features

- 🔐 Admin login
- 📦 Inventory loading from CSV
- 📊 Platform-specific price and condition mapping
- ✅ Listability suggestions based on stock and profitability
- 📉 Fee calculation for Platform X, Y, and Z
- 🖥️ Simple, clean Streamlit UI

## 🗂️ File Structure

├── app.py # Main Streamlit app
├── auth.py # Handles login authentication
├── phones.py # Inventory display and logic
├── utils.py # Pricing logic and condition mapping
├── inventory.csv # Sample phone inventory
├── requirements.txt # Python dependencies
└── README.md # Project info

## 🧪 Demo Credentials

- **Username:** `admin`
- **Password:** `admin`

## 🚀 How to Run

```bash
git clone https://github.com/PranjalAyare/refurbished-phone-app.git
cd refurbished-phone-listing
pip install -r requirements.txt
streamlit run app.py
📄 Sample Inventory Format
name,condition,cost,stock
iPhone 12,Like New,400,2
Samsung Galaxy S21,Fair,250,0
OnePlus 9,Good,300,1
🧠 Condition Mapping Example
App Condition	Platform X	Platform Y	Platform Z
Like New	New	3 Stars	As New
Good	Good	2 Stars	Good
Fair	Scrap	1 Star	Good

🛠️ Tech Stack
Python 3
Streamlit
Pandas

📬 Author
Made by Pranjal Ayare

