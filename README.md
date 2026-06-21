# Autonomous AI Claim Agent for Global E-Commerce Logistics

An enterprise-grade, high-throughput asynchronous API micro-SaaS designed to automatically detect delivery delays in international e-commerce orders, calculate financial losses, and deploy formal legal claim complaints to carriers using AI agents.

## 🚀 Architectural Overview
This system is engineered for distributed resilience, utilizing three core technology layers:
- **Core API Engine:** Powered by **FastAPI** & **Uvicorn** for low-latency asynchronous routing and automated OpenAPI/Swagger UI generation.
- **Data Persistence & State Management:** Powered by **Supabase (PostgreSQL)** utilizing bulk inserts to execute stress-test loads up to 500 concurrent requests without thread starvation.
- **Cognitive Lawyer Agent:** Powered by **OpenAI (GPT-4o-mini)**, implementing a strictly constrained System Prompt to mitigate hallucinations and enforce professional legal English output.

## 🛡️ Fault Tolerance & Cyber Security
- **Asynchronous Airbags:** Implemented utilizing Pythonic `try/except` operational blocks to capture API status errors (e.g., HTTP 401 Authentication Failures) without degrading or crashing the main server application.
- **Data Encapsulation:** Zero hardcoded credentials. All secret access keys (`SUPABASE_KEY`, `OPENAI_API_KEY`) are dynamically loaded via environment variables (`.env`) for server-side security.

## 🛠️ Local Installation & Testing
Clone the repository and install the production dependencies:
```bash
git clone https://github.com
pip install -r requirements.txt
```

Run the local development web server:
```bash
uvicorn main:app --reload
```

## 🌐 Production Deployment
The infrastructure is fully containerized and continuously deployed on the **Vercel** serverless network, utilizing an integrated Git webhook for instant global rollouts.
