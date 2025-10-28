# Neural Machine Translation (NMT) API Documentation

**Base URL:** `https://nmt-api.umuganda.digital`

## Overview

The Neural Machine Translation API facilitates translation of text between English and Kinyarwanda. The API provides accurate bidirectional translation using neural machine translation models.

## Supported Languages

- **English** (`en`)
- **French** (`fr`) - Language detection only, translation not supported
- **Kinyarwanda** (`rw`)

---

## API Endpoints

### 1. Get Supported Languages and Models

**Purpose:** Retrieves all supported languages and available translation models.

**Endpoint:** `GET /api/v1/translate/`

**Request:** No body required

**Response:**
```json
{
  "models": {
    "en": {"rw": ["MULTI-en-rw"]},
    "rw": {"en": ["MULTI-rw-en"]}
  },
  "languages": {
    "en": "English",
    "fr": "French",
    "rw": "Kinyarwanda"
  }
}
```

**Example cURL:**
```bash
curl -X GET "https://nmt-api.umuganda.digital/api/v1/translate/"
```

### 2. Translate Text

**Purpose:** Translates text from one language to another.

**Endpoint:** `POST /api/v1/translate/`

**Request Body:**
```json
{
  "src": "en",
  "tgt": "rw",
  "text": "Hello, how are you?"
}
```

**Parameters:**
- `src` (string, required): Source language code (e.g., 'en' for English, 'rw' for Kinyarwanda)
- `tgt` (string, required): Target language code for the translation
- `text` (string, required): The text to be translated

**Response:**
```json
{
  "translation": "Muraho, mumeze mute?"
}
```

**Supported Language Pairs:**
- English → Kinyarwanda (`en` → `rw`)
- Kinyarwanda → English (`rw` → `en`)

**Example cURL:**
```bash
curl -X POST "https://nmt-api.umuganda.digital/api/v1/translate/" \
     -H "Content-Type: application/json" \
     -d '{
           "src": "en",
           "tgt": "rw",
           "text": "Hello, how are you?"
         }'
```

---

## API Information

- **Full Documentation:** https://nmt-api.umuganda.digital/docs#/
- **Base URL:** `https://nmt-api.umuganda.digital/api/v1/translate/`
- **Supported Translation Directions:**
  - English → Kinyarwanda (`en` → `rw`)
  - Kinyarwanda → English (`rw` → `en`)
- **Note:** French (`fr`) is listed as a supported language but actual translation from/to French is not supported yet.

## Language Codes

| Code | Language    | Translation Support |
|------|-------------|-------------------|
| `en` | English     | ✓ Yes             |
| `fr` | French      | ✗ No              |
| `rw` | Kinyarwanda | ✓ Yes             |

## Error Handling

If an unsupported language pair is requested, the API returns a 406 error:

```json
{
  "detail": "Language pair fr-rw is not supported."
}
```

## Model Information

- **Model Name (en→rw):** `MULTI-en-rw`
- **Model Name (rw→en):** `MULTI-rw-en`

## References

- API Documentation: https://nmt-api.umuganda.digital/docs#/

