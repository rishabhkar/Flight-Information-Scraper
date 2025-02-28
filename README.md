# Flight Information Scraper

A Python script that monitors flight prices using a RapidAPI flight search service. This project leverages the Skyscanner APIs on RapidAPI to fetch flight data. The script dynamically constructs the API URL from environment variables, retrieves the data, and displays the top three cheapest flights with their airline names.

## Features

- Constructs the API URL from environment variables.
- Fetches flight data using the `requests` library.
- Parses JSON responses to extract flight itineraries.
- Displays the top 3 cheapest flights with airline names and flight timings.

## Prerequisites

- Python 3.6 or higher
- `pip` package manager

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/rishabhkar/Flight-Information-Scraper.git
   cd <repository_directory>
   ```

2. **Install Dependencies**

   ```bash
   pip install requests python-dotenv
   ```
   

## Environment Setup

File named 'environment.env' is already created in the project root directory.
Replace 'your_api_key' with your actual RapidAPI key.

## RapidAPI and Skyscanner API Setup

1. **Sign Up or Log In:**  
   Visit [RapidAPI](https://rapidapi.com) and create an account or log in.

2. **Search for Skyscanner APIs:**  
   Use RapidAPI’s search feature to find the Skyscanner APIs that fit your needs.

3. **Subscribe to the API:**  
   Choose a plan that suits your requirements and subscribe.

4. **Retrieve Your API Key:**  
   Get your API key from your RapidAPI dashboard and update the `.env` file accordingly.

5. **Review Documentation:**  
   Refer to the API documentation on RapidAPI for further configuration and usage guidelines.


## Usage

Run the script with:

```bash
python flight_monitor.py
```
    
    
## Automated Scheduling

### Option 1: Python schedule Library

Add the following code to your script:

```python
import schedule
import time

def main():
    # Your existing script logic here
    pass

schedule.every(60).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)

```

### Option 2: Cron/Task Scheduler

### Option 2: Cron/Task Scheduler

**Linux/macOS:**

Add a cron job by editing your crontab:

```bash
crontab -e
```

Then add the following line:

```bash
*/60 * * * * /usr/bin/python3 /path/to/flight_monitor.py
```

Windows:
Use Task Scheduler to run the script with the following command:

```bash
python \path\to\flight_monitor.py
```
