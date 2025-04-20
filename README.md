# Flurry

## Requirements
- Node.js (v14 or higher)
- NPM or Yarn for managing dependencies
- [Azure Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-csharp)



## Installation
1. Clone the repo
```bash
git clone https://github.com/ArchitAnant/Flurry.git
```

2. Install and Run React
```bash
cd flurry-app

npm install
npm install gsap

npm start
```
2. Install and Run Backend
```bash
cd flurry-back

pip install -r requirements.txt
```
3. You would require a `.env` file inside `flurry-back`.
```
GNEWS_API_KEY = 
GEMINI_API_KEY = 
SEPAPI_API_KEY = 
GROQ_API_KEY =
```

4. Run the function
```bash
func start
```


