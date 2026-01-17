# NetFlow: Financial Intelligence Platform

![NetFlow Banner](docs/images/banner_placeholder.png)
## 🚩 Problem Statement: The "Rearview Mirror" Flaw

Modern personal finance tools (Mint, YNAB, Excel) suffer from a critical flaw: **Passivity**. They are excellent at categorizing money you have *already lost*, but terrible at preventing future waste.

* **The "Stealth Inflation" Gap:** Service providers (ISPs, Insurance) slowly creep prices up by 2-5% annually. Passive trackers bury this in "Utilities," making it invisible until it compounds into thousands of dollars of waste.
* **Algorithmic Asymmetry:** Large corporations use complex algorithms to maximize the price they extract from consumers. The average user fights back with mental math, creating an unfair fight.
* **The Optimization Fallacy:** When paying off multiple debts, users often rely on intuition (the "Snowball method") rather than mathematical proof, paying significantly more interest than necessary.
* **Security Theater:** Most apps require uploading unredacted statements to the cloud, creating a permanent attack vector for identity theft.

## 💡 Solution

**NetFlow** is an **Active Defense System**. It is an event-driven platform that transitions personal finance from tracking to optimization. It securely ingests documents, audits expenses against real-time market data (Web Scraping), and mathematically optimizes debt allocation using Operations Research.

## 🔑 Key Features

* **The Vault (Ingestion):** A secure drag-and-drop zone. Files are processed via a custom C++ pipeline for memory-safe handling before being permanently redacted of PII.
* **Arbitrage Engine:** Autonomous "Headless Browsers" (Playwright) scrape vendor websites (e.g., Comcast) to compare your current bill against new customer rates, flagging overpayment opportunities.
* **Debt Solver:** Uses Linear Programming (Google OR-Tools) to solve the mathematical inequality of debt interest, generating the mathematically optimal payment vector to minimize total interest paid.
* **Stealth Inflation Forensics:** Uses unsupervised learning (Isolation Forest) to detect slope anomalies in recurring bills, alerting you to "price creep" before it becomes a budget leak.
* **The Time Machine:** A Monte Carlo simulation that projects net worth based on 10,000 iterations of market variance.

## 🛠️ Technology Stack

| Category | Technology | Role |
| :--- | :--- | :--- |
| **Backend** | Python 3.11, FastAPI | The API Gateway ("The Doorman") |
| **Async Processing** | Celery, Redis | The Task Queue ("The Muscle" & "The Nervous System") |
| **Systems** | C++17, Pybind11 | Cryptography & Heavy Computation Extension |
| **Database** | TimescaleDB (PostgreSQL) | Time-series storage ("The Memory") |
| **Frontend** | Next.js 14, TypeScript, D3.js | Interactive Dashboard & Visualization |
| **DevOps** | Docker Compose, Nginx | Orchestration & Containerization |

## 🏗️ System Architecture

NetFlow operates as a distributed system using an Event-Driven Microservices pattern to decouple the UI from heavy computational tasks.

![System Architecture Diagram](docs/images/architecture_diagram.png)
### The "Bill Audit" Pipeline
1.  **Ingest:** User uploads an encrypted blob via the Frontend.
2.  **Decrypt:** The API Gateway passes the blob to the **C++ Extension**. Phase 1 implements an XOR simulation; Phase 2 will implement full AES-256. Decryption happens in RAM, preventing unencrypted data from touching the disk.
3.  **Queue:** The extracted text is pushed to Redis.
4.  **Analyze:** A generic Worker Node picks up the task, running OCR (Tesseract) and identifying the vendor.
5.  **Audit:** The Arbitrage Engine triggers a Playwright container to scrape live market data.
6.  **Alert:** If `Current_Price > Scraped_Price`, a WebSocket event notifies the user.

## 🚀 Installation & Setup

### Prerequisites
* Docker Desktop (v4.0+)
* Git

### Quick Start
NetFlow is container-native. You do not need Python or Node.js installed on your host machine to run it.

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/netflow.git](https://github.com/yourusername/netflow.git)
    cd netflow
    ```

2.  **Environment Configuration**
    Create a `.env` file in the root directory (refer to `infra/env.example`):
    ```bash
    cp infra/env.example .env
    ```

3.  **Build and Run**
    This command builds the C++ module, installs Python dependencies, and starts the Next.js frontend.
    ```bash
    docker compose up --build
    ```

4.  **Access the Application**
    * **Frontend (UI):** [http://localhost:3000](http://localhost:3000)
    * **API Documentation (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
    * **Database Admin (pgAdmin - Optional):** [http://localhost:5050](http://localhost:5050)

## 📖 Usage

### Uploading a Document (The Vault)
Navigate to the "Vault" tab. Drag and drop a sample PDF bank statement. You will see the "Locking" animation as the client-side encryption engages.

![Vault UI Screenshot](docs/images/vault_ui.png)
### Running a Manual Test (API)
To verify the C++ Decryption and Celery Handoff without the UI:

```bash
curl -X POST "http://localhost:8000/upload" \
     -F "file=@./test_document.pdf" \
     -F "key=secret_key"
