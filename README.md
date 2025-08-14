# Price_tracker
Price tracker in amazon run daily for automated msj through telegram

Price_tracker is a Python-based price tracking tool that monitors one or more product URLs from Amazon and alerts you when the price drops below a target value.
It is designed to run locally or on a server, with customizable settings via .env.

📌 Features
	•	Multiple product tracking – monitor any number of Amazon products at once.
	•	Custom target price – set an alert threshold for each product individually.
	•	Environment-based configuration – store product list and settings securely in .env.
	•	Timeout control – avoid hanging requests and reduce scraping footprint.
	•	Scraping-safe practices – randomized delays between requests to avoid being blocked.

Price_tracker/
│
├── source/
│   ├── price_tracker.py    # Main script
│
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md               # Documentation


📌 Notes
	•	This script is for personal use only.
	•	Please Avoid sending too many requests in short intervals.
