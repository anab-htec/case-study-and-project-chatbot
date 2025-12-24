# AI Case Study & Project Matching Chatbot

An intelligent RAG-powered chatbot designed to retrieve detailed case study insights and match project requirements with historical data. This tool leverages **LlamaIndex Workflow**, **OpenAI**, and **Weaviate** to provide high-accuracy information retrieval.

---

## 🏗️ Architecture & System Design

The project is structured as a multi-container application managed by Docker Compose. The following diagram illustrates the relationship between the React frontend, the FastAPI backend (orchestrated by LlamaIndex), and the Weaviate vector database.

```mermaid
graph TD
    subgraph Docker_Host [Docker Compose Environment]
        
        direction TB
        
        %% Client Layer
        React_App[React Frontend Container]
        
        %% Logic Layer
        subgraph Backend_Service [FastAPI Backend Container]
            direction LR
            LI_Engine[LlamaIndex Workflow]
            Loader[[Data Loader Script]]
            Eval[[DeepEval Test Suite]]
        end
        
        %% Storage Layer
        Weaviate_DB[(Weaviate Vector DB Container)]
        
    end

    %% External Dependencies
    LLM_Service[OpenAI API]

    %% Connectivity (Static Relationships)
    React_App <--> Backend_Service
    Backend_Service <--> Weaviate_DB
    Backend_Service -.-> LLM_Service
```

## 🔄 RAG Workflow  

The chatbot uses an event-driven workflow to handle user queries, manage conversation state, and ensure high-precision retrieval.

```mermaid
graph TD
    %% Entry
    START([User Query]) --> PRE[Query Pre-processing]
    
    %% Conversation Context
    PRE --> CONTEXT{Is this a follow-up?}
    CONTEXT -->|Yes| REWRITE[Contextual Query Rewriting]
    CONTEXT -->|No| INTENT[Intent & Entity Extraction]
    REWRITE --> INTENT

    %% Intent Routing
    INTENT --> ROUTE{Detected Intent}
    
    ROUTE -->|Ambiguous| CLARIFY[Request Clarification]
    
    ROUTE -->|Case Study| CS_RET[Case Study Vector Retrieval]
    
    ROUTE -->|Project Matching| PROJ_RET[Dual-Vector Project Retrieval]
    PROJ_RET --> AGG[Similarity Score Aggregation]
    AGG --> THRESHOLD{Records with score > 0.6 found?}
    THRESHOLD -->|No| CLARIFY
    THRESHOLD -->|Yes| SUMMARIZE

    %% Results & Feedback
    CS_RET --> SUMMARIZE[LLM Summarization & Response]
    
    SUMMARIZE --> END([Display Result to User])

    %% The Guardrail / Loop
    CLARIFY --> LIMIT{Attempt < 3?}
    LIMIT -->|Yes| WAIT[Wait for User Input]
    LIMIT -->|No| EXIT_MSG[Final Failure Message]
    
    WAIT --> PRE
    EXIT_MSG --> END
```


## 🛠️ Tech Stack

* **AI/RAG**: LlamaIndex (Workflows), OpenAI
* **Backend**: FastAPI, Poetry (Dependency Management)
* **Frontend**: React
* **Vector Database**: Weaviate
* **Evaluation**: DeepEval



## 🚀 Getting Started

### 1. Prerequisites
Ensure you have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed.

### 2. Environment Setup
Run the following command from the root folder of the project to create your local environment file:

For Mac / Linux / Git Bash / PowerShell:
```bash
cp backend/.env.example backend/.env
```
For Windows Command Prompt (CMD):
```bash
copy backend\.env.example backend\.env
```
Once created, set the **OPENAI_API_KEY** and **OPENAI_BASE_URL** under .env

### 3. Launch the application
Start the entire stack (Weaviate, API, and Frontend) using Docker Compose:

```bash
docker compose up 
```

Verify that the services are running:

Chatbot UI: http://localhost:3000 — Main user interface.

API Health & Docs: http://localhost:8000/docs — FastAPI Swagger documentation.

Database Ready: http://localhost:8080/v1/.well-known/ready — Should return a 200 OK status.

### 4. Data Ingestion
Once the containers are healthy, the synthetic data must be loaded into Weaviate. Run the following command from the root folder of the project:
```bash
docker compose exec backend poetry run load-data
```

Data sources: _backend/data/case_studies.json_ and _backend/data/projects.json_.

## 📊 Evaluation

To ensure the quality of the chatbot responses, DeepEval is used to run "LLM-as-a-judge" audits across three core scenarios. Each scenario is tested against a specific set of metrics by executing the workflow against a **Golden Dataset** and scoring the results.

### 1. Multi-Scenario Testing
The evaluation suite categorizes tests into three distinct scenarios, applying specialized metrics to each:

* **Case Study Summarization**
* **Project Matching**
* **Clarification Logic**

### 2. Key Metrics

| Metric | Goal | Description |
| :--- | :--- | :--- |
| **Faithfulness** | Anti-Hallucination | Ensures the answer is derived *only* from retrieved Weaviate records. |
| **Intent Accuracy** | Classification | Measures if the system correctly identified the user's intent (project matching vs. case study retrieval). |
| **Attribute Coverage** | Completeness | Validates that key entities from the retrieved records are captured in the response. |
| **Score Threshold** | Quality Gate | Validates that retrieved projects meet the minimum $0.6$ similarity score. |
| **Latency** | Performance | Ensures the end-to-end RAG workflow completes within a 40-second window. |


### 3. Running Evaluations
The evaluation runs as an ephemeral task within the backend container to ensure it has direct access to the Weaviate network and it can be triggered by executing the following command from the root folder of the project:

```bash
docker compose exec backend poetry run run-eval
```
The script will output a Final Summary Report with a pass rate percentage and average scores for each metric per scenario.


## 📂 Project Structure

```text
├── backend
│   ├── app                     # FastAPI Application Source
│   │   ├── api/                # Route definitions and API endpoints
│   │   ├── core/               # Global configuration, settings, and LLM prompts
│   │   ├── models/             # Pydantic schemas and data models
│   │   ├── repositories/       # Data Access Layer (Weaviate-specific logic)
│   │   ├── services/           # Core Business Logic & LlamaIndex Workflow
│   │   ├── dependencies.py     # Dependency injection (Services, Repos)
│   │   └── main.py             # Application entry point
│   │   └── .env.example        # Template for required environment variables
│   ├── data/                   # Knowledge Base (case_studies.json, projects.json)
│   ├── evaluation/             # DeepEval suite, custom metrics, and golden dataset
│   └── scripts/                # Data ingestion and synthetic data generation
├── frontend/                   # React application source code
├── docker-compose.yml          # Multi-container orchestration config
```
