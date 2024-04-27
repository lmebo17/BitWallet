# Bitcoin Wallet HTTP API

## Introduction

The goal of this project is to develop an HTTP API for managing Bitcoin wallets. Unlike traditional blockchain operations, we'll be utilizing SQLite for data persistence. This design choice provides flexibility, allowing for future extension to other database systems like Postgres, MySQL, or even integration with real blockchain networks.

While this project won't address the complexities of blockchain concurrency, developers are encouraged to consider solutions for issues like "double spending."

## API Specifications

### User Registration

- **Endpoint:** `POST /users`
- Registers a new user and provides an API key for authentication.

### Wallet Operations

- **Endpoint:** `POST /wallets`
  - Requires API key
  - Creates a new Bitcoin wallet
  - Automatically deposits 1 BTC (or 100,000,000 satoshis)
  - Users can register up to 3 wallets
  - Returns wallet address and balance in BTC and USD

- **Endpoint:** `GET /wallets/{address}`
  - Requires API key
  - Retrieves wallet information including balance in BTC and USD

### Transaction Management

- **Endpoint:** `POST /transactions`
  - Requires API key
  - Facilitates transactions between wallets
  - Transactions between wallets owned by the same user are free
  - A 1.5% fee is charged for transactions to foreign wallets

- **Endpoint:** `GET /transactions`
  - Requires API key
  - Returns a list of transactions

- **Endpoint:** `GET /wallets/{address}/transactions`
  - Requires API key
  - Retrieves transactions related to a specific wallet

### Statistics

- **Endpoint:** `GET /statistics`
  - Requires pre-set Admin API key
  - Provides total transaction count and platform profit

## Technical Requirements

- Python 3.11
- FastAPI as the web framework
- SQLite for data persistence
- Use of a publicly available API for BTC to USD conversion
- Implementation of API key authentication using the "X-API-KEY" HTTP header
- Implementation of API endpoints (no UI)
- Concurrency considerations are out of scope

## Testing

Automated tests should be provided to ensure software correctness and detect regressions in behavior.

## Disclaimer

Ambiguous requirements may be clarified at the discretion of project stakeholders. Developers are encouraged to seek clarification as needed to ensure understanding.
