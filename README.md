# INTEL.ai — Company Intelligence On Demand

> *Enter a company name. Get a full strategic report in minutes.*

## 🚀 Live Demo

👉 [https://autonomous-company-research-report.onrender.com](https://autonomous-company-research-report.onrender.com)

> Note: The free instance may take 30-50 seconds to wake up on first visit.

## What Is This?

INTEL.ai is an AI-powered research assistant that automatically generates professional company intelligence reports. Just type a company name, and the system does all the heavy lifting — searching the web, pulling financial data, reading the latest news, and writing a structured strategic report.

No manual research. No copy-pasting. Just results.

## What It Does

1. **You type a company name** — e.g. "Apple" or "Tesla"
2. **The agent searches the web** for recent news, financials, and market data
3. **A professional report is generated** covering:
   - Financial overview with real numbers
   - Recent news and market sentiment
   - Competitive landscape
   - Strategic risks and recommendations
4. **Download the report as PDF** with one click

## Who Is This For?

- Business analysts who need quick company overviews
- Investors researching companies before making decisions
- Students and researchers studying market dynamics
- Anyone who wants to understand a company fast

## How To Run It Locally

1. Clone this repo
2. Create a `.env` file with your API keys (see `.env.example`)
3. Install dependencies: `pip install -r requirements.txt`
4. Start n8n and activate the workflow
5. Run: `python agent/server.py`
6. Open: `http://127.0.0.1:5000`

## Built With

- **n8n** — orchestrates the data collection pipeline
- **LangGraph** — powers the AI reasoning agent
- **GPT-4o-mini** — generates the written report
- **Serper, Guardian, Alpha Vantage** — real-time data sources
- **Pinecone** — provides structural guidance to the agent
- **Flask** — serves the web interface
