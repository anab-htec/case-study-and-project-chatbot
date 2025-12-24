# AI Case Study & Project Matcher Chatbot

An intelligent RAG-powered chatbot designed to retrieve detailed case study insights and match project requirements with historical data. This tool leverages **LlamaIndex Workflow**, **OpenAI**, and **Weaviate** to provide high-accuracy information retrieval.

---

## Architecture

The project is structured as a multi-container application managed by Docker Compose:

* **Frontend**: React-based user interface.
* **Backend**: FastAPI server handling RAG logic.
* **Database**: Weaviate (Vector Database) for storing and querying embeddings.
* **Orchestration**: Docker Compose.

## Tech Stack

* **AI/RAG**: LlamaIndex (Workflows), OpenAI
* **Backend**: FastAPI, Poetry (Dependency Management)
* **Frontend**: React
* **Vector Database**: Weaviate
* **Evaluation**: DeepEval

---

## Getting Started

### 1. Prerequisites
Ensure you have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed.

### 2. Environment Setup
Copy the example environment file:

```bash
cp .env.example .env
```

Open .env and set OPENAI_API_KEY and OPENAI_BASE_URL

### 3. Launch the application
Start the entire stack (Weaviate, API, and Frontend) using Docker Compose:

```bash
docker compose up 
```

### 4. Data Ingestion
Once the containers are healthy, you must load the synthetic case studies and project data into Weaviate. Run the following command:
```bash
docker compose exec backend poetry run load-data
```

Data sources: backend/data/case_studies.json and backend/data/projects.json.

## Evaluation
To ensure the quality of the chatbot responses, we use DeepEval against a golden dataset located at backend/evaluation/golden_dataset.py.

To run the evaluation suite:
```bash
docker compose exec backend poetry run run-eval
```

## Project structure
```
├── backend
│   ├── data                 # Source data (case_studies.json, projects.json)
│   ├── evaluation           # Evaluation scripts, metrics and golden dataset
│   ├── scripts              # Scripts for synthetic data generation and loading
│   └── app                  # FastAPI app and RAG wofkflow
├── frontend                 # React application source code
├── .env.example             # Template for environment variables
└── docker-compose.yml       # Docker orchestration config
```
