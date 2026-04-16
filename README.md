# AB Ventures Hub — WhatsApp AI Support Bot

A RAG-powered WhatsApp customer support bot built for AB Ventures Hub, a Nigerian business dealing in phones, computer gadgets, and real estate. Customers send a WhatsApp message and receive instant, accurate answers 24 hours a day, 7 days a week.

**Live on:** WhatsApp via Twilio · Deployed on Render

---

## What It Does

- Answers customer questions instantly over WhatsApp
- Responds only from the company's own knowledge base — never guesses
- Handles enquiries about phones, laptops, accessories, warranties, payments, and real estate
- Escalates to a human agent with a clear message when it cannot answer
- Runs 24/7 in the cloud without any manual intervention

---

## The Problem It Solves

AB Ventures Hub serves customers across Lagos who have questions about product availability, pricing, warranties, land documents, and property locations. Before this bot, enquiries outside business hours went unanswered, leading to lost sales and frustrated customers.

This bot provides an always-on first line of support that handles routine questions instantly, freeing the team to focus on closing sales and complex enquiries.

---

## How It Works

1. Customer sends a WhatsApp message to the business number
2. Twilio receives the message and forwards it to the FastAPI webhook on Render
3. The app searches a ChromaDB vector database built from the company's knowledge base
4. The 5 most relevant chunks are passed to GPT-4o-mini
5. GPT generates a grounded answer using only those chunks
6. The answer is sent back through Twilio to the customer's WhatsApp

This pattern is called **RAG (Retrieval-Augmented Generation)**.

---

## Key Features

- **WhatsApp native** — customers use the app they already have, no downloads needed
- **Grounded answers** — responds only from company documents, never the internet
- **Graceful escalation** — directs customers to call or visit when it cannot help
- **Easy knowledge base updates** — update the text file and redeploy in minutes
- **Cloud deployed** — runs on Render 24/7, no laptop required

---

## Tech Stack

| Layer | Tool |
|---|---|
| Messaging | Twilio WhatsApp API |
| Web Framework | FastAPI |
| Server | Uvicorn on Render |
| LLM | GPT-4o-mini (OpenAI) |
| Embeddings | OpenAI text-embedding-ada-002 |
| Vector Store | ChromaDB |
| Orchestration | LangChain (LCEL) |
| Environment | python-dotenv |

---

## Project Structure

```
abventures-whatsapp/
├── main.py             # FastAPI app with WhatsApp webhook
├── requirements.txt    # Python dependencies
├── docs/               # Company knowledge base
│   └── abventures.txt  # FAQs, product info, real estate info
├── .env                # API keys (not committed to GitHub)
├── .gitignore          # Excludes .env, venv, ChromaDB files
└── .chroma/            # Local vector store (auto-created on first run)
```

---

## Updating the Knowledge Base

To update the bot with new products, prices, or policies:

1. Open `docs/abventures.txt`
2. Add or edit the relevant information
3. Delete the `.chroma` folder so the index rebuilds
4. Push to GitHub — Render redeploys automatically

---

## Deploying for a New Client

To adapt this bot for a different business:

1. Replace `docs/abventures.txt` with the new client's FAQ document
2. Update the company name and contact details in the prompt inside `main.py`
3. Connect a new Twilio WhatsApp number
4. Push to GitHub and deploy a new Render service

The entire RAG pipeline requires no changes.

---

## Production Deployment Notes

- **Twilio sandbox** is used for testing. For production, connect a dedicated WhatsApp Business number through Twilio
- **Render free tier** sleeps after 15 minutes of inactivity — first message after a long gap may take 30-50 seconds. Upgrade to Render paid tier ($7/month) for always-on performance
- **Knowledge base updates** take effect after redeployment — Render auto-deploys on every GitHub push

---

## Built By

**Olumide Daramola** — NVIDIA-certified Generative AI Developer
[Portfolio](https://olumidedaramola.dev) · [GitHub](https://github.com/DataBuster204)
