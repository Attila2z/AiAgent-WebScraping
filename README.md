## **1. Project Setup**

### 1.1 Clone project folder
```bash
mkdir WebScraping
cd WebScraping
````

### 1.2 Create a virtual environment (Python 3.12)
```bash -powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate
````

### 1.3 Check python version inside venv
```bash -powershell
python --version
````

## 2. Install the required dependencies (inside venv)
```bash -powershell
C:\Users\xxxxx\WebScraping\venv\Scripts\python.exe -m pip install --upgrade pip
````
```bash -powershell
pip install "autogen-agentchat @ git+https://github.com/patrickstolc/autogen.git@0.2#egg=autogen-agentchat"
pip install autogen==0.3.1
pip install mistralai==1.2.3
pip install ollama==0.3.3
pip install fix-busted-json==0.0.18
````

### 2.1 Check instalation
```bash -powershell
pip list
````
You should now see the following packages installed:

1. [ ] autogen 0.3.1
3. [ ] autogen-agentchat 0.2.x
5. [ ] mistralai 1.2.3
7. [ ] ollama 0.3.3
9. [ ] fix-busted-json 0.0.18
11. [ ] and other dependencies# AI-Agents-Using-Autogen

## 3. Add Mistral API key
Create a .env file in the project root:
```
MISTRAL_API_KEY=your_key
````
config.py loads it automatically

## 4. Run Project
```bash -powershell
python main.py
````
