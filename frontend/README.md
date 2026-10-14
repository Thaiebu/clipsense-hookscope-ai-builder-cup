# HookScope — Explainable Video Coach (Frontend)

Modern React + Vite frontend for HookScope, powered by Google Gemini 2.5 / 3.8 on Google Cloud.

---

## 🚀 Quick Start

### 1. Prerequisites
- Node.js (v18+)
- Backend running on `http://localhost:8080` (see `../backend/README.md`)

### 2. Install Dependencies
```bash
cd frontend
npm install
```

### 3. Start the Development Server
```bash
npm run dev
```

The frontend will start at **http://localhost:5173**.

> **Note:** The Vite dev server has a built-in proxy configured in `vite.config.js` that automatically forwards `/api/*` calls to `http://localhost:8080`.

---

## ⚙️ Environment Configuration (Optional)

If you are running the backend on a remote URL (like Google Cloud Run) rather than locally, copy `.env.example`:

```bash
cp .env.example .env
```

And set:
```bash
VITE_API_URL=https://your-cloud-run-service.a.run.app
VITE_API_KEY=your_optional_x_api_key
```

*(Leave `VITE_API_URL` empty to default to the local Vite proxy).*

---

## 🔨 Available Scripts

- `npm run dev` — Starts Vite development server at `http://localhost:5173` with HMR
- `npm run build` — Bundles production-ready assets into `dist/`
- `npm run preview` — Locally previews the production build in `dist/`

---

## 🌟 Key Features

1. **YouTube IFrame Player:**
   - Synchronized timeline navigation
   - Click any timestamp badge (e.g. `00:14`) to seek directly to the evidence moment with a 3-second pre-roll
2. **Hook Rubric Analysis:**
   - Evaluates Clarity, Curiosity, Pacing, and Payoff Promise with 0–10 score badges
3. **Simulated Audience Panel:**
   - 3 niche personas (Fitness, Tech, Cooking, Education, General) with highlights and concerns
   - Disagreements Matrix exposing conflicting viewer expectations
4. **Content Readiness Score:**
   - Circular 0–100 score with 4-factor breakdown and prioritized creator actions
5. **Shorts Candidates (Tier 3):**
   - Viral vertical clip candidates (<60s) with 0–3s hook captions
6. **Multilingual Translation (Tier 3):**
   - 1-click feedback translation into Hindi, Spanish, Japanese, German, or French
7. **Inspect AI Reasoning:**
   - Full transparency modal showing raw prompts and instructions sent to Google Gemini
