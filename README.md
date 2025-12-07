# Web Scraping Agent (AutoGen)

This project implements a simple web scraping agent using the AutoGen framework and LLM.

The agent:

- Downloads the HTML of a web page (e.g. Google Finance META page) using `requests`.
- Parses the HTML into visible text using BeautifulSoup.
- Calls an AutoGen `AssistantAgent` with a system message and a task.
- The agent reads the page content and returns a **structured JSON** answer with fields:
  - `answer`
  - `extracted_value`
  - `unit_or_currency`
  - `confidence`
  - `notes`

An evaluation script runs multiple use-cases and writes all inputs + outputs to a JSON file.

---

## 1. Project structure

Important files:

- `main.py`  
  Runs a single example:
  - Fetches the META Google Finance page  
  - Asks the agent: “Extract the current stock price of META in USD …”  
  - Prints the JSON result and the human-readable answer.

- `config.py`  
  Loads environment variables from `.env` and defines `LLM_CONFIG` (model name, API key, base URL, temperature).

- `WebScraping/tools.py`  
  - `fetch_page_html(url)`: downloads raw HTML using `requests`.
  - `html_to_visible_text(html)`: parses HTML with BeautifulSoup and converts it to clean visible text.

- `WebScraping/agent.py`  
  - Defines `SYSTEM_MESSAGE` (agent instructions and JSON output format).
  - `create_web_scraping_agent()`: creates an AutoGen `AssistantAgent`.
  - `ask_agent(...)`: sends `(task, url, page_text)` to the agent and returns a Python `dict` with keys:
    `answer`, `extracted_value`, `unit_or_currency`, `confidence`, `notes`.

- `WebScraping/evaluate.py`  
  - Defines several use-cases (URL + task).
  - Runs them and saves results to `use_cases_outputs.json`.

- `requirements.txt`  
  Lists Python dependencies for the project.

---

## 2. Setup

### 2.1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

### 2.2 Create a virtual environment (Python 3.12)
```bash -powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate
````

### 2.3 Install dependencies
```bash -powershell
pip install --upgrade pip
pip install -r requirements.txt
````
### 2.4 Configure API key and model (.env file)
```bash -powershell
Create a file named .env in the project root:
MISTRAL_API_KEY="your_api"
````

