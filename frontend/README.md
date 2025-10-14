AI Customer Support Bot - React Frontend (Vite)

This frontend replaces the Gradio UI with a React app built using Vite. It connects to the existing Flask backend endpoints: `/chat`, `/reset`, `/health`.

Getting Started
1. Ensure the Flask backend is running on `http://127.0.0.1:5000`:
   ```bash
   python app.py
   ```
2. Start the React dev server:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Open the app at `http://localhost:5173`.

Build
```bash
cd frontend
npm run build
```

Preview production build
```bash
npm run preview
```

Environment
- The API base URL is currently hardcoded to `http://127.0.0.1:5000` in `src/api/client.js`. Adjust if your backend runs elsewhere.

Feature parity with Gradio
- Chat messages with assistant responses and source labels
- Health badge showing backend, FAQ count, and AI availability
- Quick prompts buttons
- New session (regenerates UUID) and reset backend history
