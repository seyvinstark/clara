# Clara - Translation Assistant

A Streamlit web application for translating between English and Kinyarwanda using the NMT API.

## Features

- 🌐 Translate between English and Kinyarwanda
- 💬 Chat-style interface with message history
- 📱 Responsive design for mobile, tablet, and desktop
- 🎨 Modern blue-themed UI inspired by popular messenger apps
- ⚙️ Customizable language selection
- 🗑️ Clear chat history

## API

This app uses the Neural Machine Translation API from [umuganda.digital](https://nmt-api.umuganda.digital/docs#/).

Supported language pairs:
- English → Kinyarwanda
- Kinyarwanda → English

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/clara.git
cd clara
```

2. Create a virtual environment:
```bash
python3.11 -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows
.\venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run main.py
```

The app will open at `http://localhost:8501`

## Project Structure

```
clara/
├── main.py                  # Streamlit application
├── test_api.py              # API testing script
├── api_mapping.json         # API test results
├── NMT_API_DOCUMENTATION.md # API documentation
├── requirements.txt         # Dependencies
├── .streamlit/              
│   └── config.toml          # Streamlit configuration
└── README.md
```

## Dependencies

- streamlit >= 1.28.0
- requests >= 2.31.0

## License

MIT

