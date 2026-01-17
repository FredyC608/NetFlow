# NetFlow: Financial Intelligence System

![NetFlow Architecture Banner](docs/images/banner_placeholder.png)
## Problem Statement

Current personal finance tools (Mint, YNAB, Excel) operate on a passive model: they categorize money that has already been spent. This approach suffers from three technical limitations:
1.  **Latency:** Spending data is reviewed retroactively, often weeks after the transaction.
2.  **Hidden Inflation:** Gradual price increases (1-3%) in recurring bills (ISPs, Insurance) are often masked within broad categories, compounding over time.
3.  **Suboptimal Allocation:** Debt repayment strategies are often based on intuition (e.g., "Snowball Method") rather than mathematical optimization, resulting in excess interest payments.

## Solution

**NetFlow** is an active defense system designed to transition personal finance from tracking to optimization. It utilizes an event-driven architecture to:
1.  **Ingest** financial documents via a secure, client-encrypted pipeline.
2.  **Audit** expenses against real-time market data using headless browser scraping.
3.  **Optimize** debt allocation using Linear Programming (Operations Research).

## Key Features

* **The Vault (Secure Ingestion):** A drag-and-drop interface that handles client-side encryption. Files are processed via a custom C++ extension for memory-safe decryption and PII redaction before persistence.
* **Arbitrage Engine:** Deploys headless browsers (Playwright) to scrape vendor sites (e.g., Comcast) and compare user bills against current "New Customer" rates.
* **Debt Solver:** Implements Google OR-Tools to solve a Linear Programming model, outputting the mathematically optimal payment vector to minimize total interest $\sum (Interest_i)$.
* **Stealth Inflation Forensics:** Applies Unsupervised Learning (Isolation Forest) to transaction history to detect slope anomalies and "price creep" in recurring costs.
* **The Time Machine:** Runs a Monte Carlo simulation (10,000 iterations) to project future net worth based on variable market returns and inflation volatility.

## Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend API** | Python 3.11, FastAPI | Request handling, Auth, Validation. |
| **Compute Engine** | C++17, Pybind11 | Cryptography, Heavy computation modules. |
| **Async Tasks** | Celery, Redis | Distributed task queue (OCR, Scraping). |
| **Database** | TimescaleDB (PostgreSQL) | Time-series storage for financial data. |
| **Scraping** | Playwright | Headless browser automation. |
| **Frontend** | Next.js 14, TypeScript | UI and D3.js Visualization. |
| **Infra** | Docker Compose | Container orchestration. |

## System Architecture

NetFlow follows an **Event-Driven Microservices** pattern. The system decouples the synchronous API Gateway from heavy computational tasks (OCR, Scraping, Solving) using a Message Broker.

![System Architecture Diagram](docs/images/architecture_diagram.png)
### The Data Pipeline
1.  **Ingest:** Client uploads an encrypted blob.
2.  **Decrypt:** C++ Module decrypts the blob in RAM (no disk write).
3.  **Queue:** The job is serialized and pushed to Redis.
4.  **Process:** A Worker Node claims the task:
    * **Worker A:** Runs Tesseract OCR to extract text.
    * **Worker B:** Runs Playwright to scrape market data.
5.  **Persist:** Structured data is written to TimescaleDB.

## Installation & Setup

NetFlow runs entirely within Docker containers. No local Python or Node.js environment is required.

### Prerequisites
* Docker Desktop (v4.0+)
* Git

### Quick Start

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-org/netflow.git](https://github.com/your-org/netflow.git)
    cd netflow
    ```

2.  **Configure Environment**
    Create the `.env` file from the example template.
    ```bash
    cp infra/env.example .env
    ```

3.  **Build and Run**
    This command compiles the C++ extension, builds the frontend, and starts all services.
    ```bash
    docker compose up --build
    ```

4.  **Verify Status**
    * **Frontend:** [http://localhost:3000](http://localhost:3000)
    * **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

## Usage

### 1. Uploading Documents
Navigate to the **Vault** tab on the frontend. Drag and drop a PDF bank statement. The UI will visualize the encryption process.

![Vault Interface](docs/images/vault_ui.png)
### 2. Manual API Testing
To test the C++ Decryption and Celery handoff without using the Frontend, use the following `curl` command:

```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
     -F "file=@./test_statement.pdf" \
     -F "key=test_secret"
