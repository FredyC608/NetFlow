# 🛡️ WealthGuard: Financial Forensics & Optimization Engine

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Tech Stack](https://img.shields.io/badge/stack-FastAPI%20|%20Next.js%20|%20C++%20|%20TimescaleDB-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> **WealthGuard** is an active financial defense system that combines C++ cryptography, OCR forensics, and linear programming to protect wealth and optimize debt repayment.

---

## 🚩 The Problem
### Personal Finance is a "Rearview Mirror"
Modern personal finance tools (Mint, YNAB, Excel) suffer from a critical flaw: **Passivity**. They are excellent at categorizing money you have *already lost*, but terrible at preventing future waste.

1.  **The "Stealth Inflation" Gap:** Service providers (streaming, ISP, insurance) slowly creep prices up by 2-5% annually. Passive trackers bury this in "Utilities," making it invisible to the user until it compounds into thousands of dollars of waste.
2.  **The Algorithmic Asymmetry:** Large corporations use complex algorithms to maximize the price they extract from you. The average consumer uses mental math or a spreadsheet to fight back. It is an unfair fight.
3.  **The Optimization Fallacy:** When paying off multiple debts (credit cards, loans), users often rely on intuition (Snowball method) rather than mathematical proof. This results in users paying significantly more interest than mathematically necessary.
4.  **The Security Theater:** Most finance apps require users to upload sensitive unredacted bank statements to cloud storage, creating a permanent attack vector for identity theft.

**WealthGuard flips this model.** It is not a tracker; it is an **Active Defense System**.

---

## 💡 The Solution
WealthGuard is a **Financial Intelligence Platform** built on an event-driven microservices architecture. It ingests financial documents, audits expenses against real-time market data (Web Scraping), and mathematically optimizes debt allocation (Operations Research).

### Core Capabilities
* **🔒 Hybrid Security:** Uses a custom **C++ Python Extension (pybind11)** to handle AES-256 decryption and sensitive memory wiping in RAM, ensuring raw financial data is never exposed to the disk or the Python Garbage Collector.
* **🕵️ Forensics Engine:** Automatically ingests PDF/CSV bank statements, parses transaction text (OCR), and detects "Stealth Inflation" using time-series analysis (TimescaleDB).
* **🤖 Arbitrage Engine:** Triggers autonomous **Headless Browsers (Playwright)** to scrape vendor websites (e.g., Comcast, Netflix) and identify if the user is paying above the current market rate.
* **🧮 Debt Solver:** Implements a **Linear Programming (Google OR-Tools)** model to solve the mathematical inequality of debt interest, outputting the optimal payment vector to minimize total interest paid.

---

## 🏗️ System Architecture
WealthGuard operates as a distributed system with 4 orchestrated containers:

| Service | Technology | Role |
| :--- | :--- | :--- |
| **API Gateway** | FastAPI (Python) | The "Doorman". Handles Auth, Uploads, and Routing. |
| **Worker Node** | Celery + C++ | The "Muscle". Runs OCR, Decryption, and Scraping tasks. |
| **Broker** | Redis | The "Nervous System". Manages the async task queue. |
| **Database** | TimescaleDB | The "Memory". Stores time-series financial history. |

### Data Flow
1.  **Ingest:** User uploads encrypted blob $\rightarrow$ API Gateway.
2.  **Decrypt:** C++ Module decrypts in memory $\rightarrow$ Passes buffer to OCR.
3.  **Analyze:** Worker extracts text $\rightarrow$ Saves to DB $\rightarrow$ Checks for anomalies.
4.  **Alert:** If `Current_Price > Scraped_Price`, trigger WebSocket alert to User.

---

## 🛠️ Technology Stack

* **Backend:** Python 3.11, FastAPI, Celery
* **Systems Programming:** C++17, Pybind11, CMake
* **Database:** PostgreSQL 14 + TimescaleDB Extension
* **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS
* **DevOps:** Docker Compose, Nginx

---
