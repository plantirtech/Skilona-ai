# Skilona-ai Backend

This is the backend for Skilona-ai, the AI-powered skincare app.

## Endpoints

- GET / → Health check
- POST /text → Ask questions (JSON: {"prompt":"your question"})
- POST /vision → Analyze skin images (Form-data: image file + prompt)
- POST /search → Search skincare info (JSON: {"query":"your query"})

## Deployment

1. Set environment variables on Render or your server:
   - GEMINI_API_KEY
   - GOOGLE_API_KEY
   - CX_ID (Google Custom Search Engine ID)
2. Run: