> Register User


`POST /users`
  - Registers user
  - Returns API key that can authenticate all subsequent requests for this user

Request:

`POST /users`

```json
{
    "username": "user_name",
    "password": "password"
}
```

Success:

HTTP 201
```json
{
  "user": {
    "API_key": "27b4f218-1cc2-4694-b131-ad481dc08901",
    "username": "user_name",
    "password": "password"
  }
}
```

Fail:

HTTP 409
```json
{
  "error": {
    "message": "User already exists."
  }
}
```
-------------------------------------------------------------------------------------------------

> Create Wallet

`POST /wallets`
  - Requires API key
  - Create BTC wallet 
  - Deposits 1 BTC (or 100000000 satoshi) automatically to the new wallet
  - User may register up to 3 wallets
  - Returns wallet address and balance in BTC and USD


Request:

`POST /wallets`

```json
{
    "API_key": "27b4f218-1cc2-4694-b131-ad481dc08901"
}
```

Success:

HTTP 201
```json
{
  "wallet": {
    "address": "27b4f218-1cc2-4694-b131-ad481dc08902",
    "balance_in_BTC": 1,
    "balance_in_USD": 100
  }
}
```

Fail User:

HTTP 404
```json
{
  "error": {
    "message": "User does not exists."
  }
}
```

Fail Create:

HTTP 403
```json
{
  "error": {
    "message": "User has reached the maximum capacity of wallets."
  }
}
```

-------------------------------------------------------------------------------------------------

> Get Wallet

`GET /wallets/{address}`
  - Requires API key
  - Returns wallet address and balance in BTC and USD

Request:
`GET /wallets/27b4f218-1cc2-4694-b131-ad481dc08901`

```json
{
    "API_key": "27b4f218-1cc2-4694-b131-ad481dc08902"
}
```

Success:

HTTP 200
```json
{
  "wallet": {
    "address": "27b4f218-1cc2-4694-b131-ad481dc08902",
    "balance in BTC": "1 BTC",
    "balance in USD": "100 USD"
  }
}  
```

Fail:

HTTP 404
```json
{
  "error": {
    "message": "Wallet does not exist."
  }
}
```

-------------------------------------------------------------------------------------------------
> Make transaction

`POST /transactions`
  - Requires API key
  - Makes a transaction from one wallet to another
  - Transaction is free if the same user is the owner of both wallets
  - System takes a 1.5% (of the transferred amount) fee for transfers to the foreign wallets

Request:
`POST /transactions`

```json
{
    "API_key": "27b4f218-1cc2-4694-b131-ad481dc08901",
    "wallet_from": "27b4f218-1cc2-4694-b131-ad481dc08902",
    "wallet_to": "27b4f218-1cc2-4694-b131-ad481dc08903",
    "amount_in_satoshi": 100
}
```

Success:

HTTP 201
```json
{
    
}
```

Fail:

HTTP 404
```json
{
  "error": {
    "message": "Wallet does not exist."
  }
}
```

Same Wallet:
HTTP 400
```json
{
  "error": {
    "message": "Transaction within the same wallet is not allowed."
  }
}
```

Fail Not enough balance:

HTTP 400
```json
{
  "error": {
    "message": "Not enough balance to complete the transaction."
  }
}
```

-------------------------------------------------------------------------------------------------
> Get user transactions

`GET /transactions`
  - Requires API key
  - Returns list of transactions

Request:
`GET /transactions`

```json
{
    "API_key": "27b4f218-1cc2-4694-b131-ad481dc08901"
}
```

Success:

HTTP 200
```json
{
  "transactions": [
    {
    "wallet from": "27b4f218-1cc2-4694-b131-ad481dc08902",
    "wallet to": "27b4f218-1cc2-4694-b131-ad481dc08903",
    "amount in satoshi": 100
    }
  ]
}  
```

Fail User:

HTTP 404
```json
{
  "error": {
    "message": "User does not exist."
  }
}
```

-------------------------------------------------------------------------------------------------
> Get wallet transactions

`GET /wallets/{address}/transactions`
  - Requires API key
  - returns transactions related to the wallet

Request:
`GET /wallets/{address}/transactions`

```json
{
    "API_key": "27b4f218-1cc2-4694-b131-ad481dc08901"
}
```

Success:

HTTP 200
```json
{
  "transactions": [
    {
    "wallet from": "27b4f218-1cc2-4694-b131-ad481dc08902",
    "wallet to": "27b4f218-1cc2-4694-b131-ad481dc08903",
    "amount in satoshi": 100
    }
  ]
}  
```

Fail:

HTTP 404
```json
{
  "error": {
    "message": "Wallet does not exist."
  }
}
```


-------------------------------------------------------------------------------------------------
> Get statistics

`GET /statistics`
  - Requires pre-set (hard coded) Admin API key
  - Returns the total number of transactions and platform profit

Request:
`GET /statistics`

```json
{
    "API_key": "27b4f218-1cc2-4694-b131-ad481dc08901"
}
```

Success:

HTTP 200
```json
{
  "statistics": {
    "transaction_number": 100,
    "profit_in_satoshi": 100
    }
}  
```

Fail Admin API_key:

HTTP 403
```json
{
  "error": {
    "message": "User does not have access to statistics."
  }
}
```