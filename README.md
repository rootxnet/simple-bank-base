# Installation
### Build and run docker containers
```shell
docker compose up --build
```

### Run migrations, import fixtures
```shell
docker compose exec -ti api python manage.py migrate
docker compose exec -ti api python manage.py loaddata ./fixtures/accounts.json ./fixtures/transactions.json
```

### Run tests
```shell
docker compose exec -ti api python manage.py test
```

### Start Jupyter Notebook

Jupyter Notebook: http://127.0.0.1:8888/


```shell
docker compose exec -e DJANGO_ALLOW_ASYNC_UNSAFE=1 -ti api python manage.py shell_plus --notebook
```

### Access to demo admin:

Admin: http://127.0.0.1:8000/admin/

```
login: admin
password: 123qwe
```

Transaction list: http://127.0.0.1:8000/admin/transactions/transaction/

Accounts with balances: http://127.0.0.1:8000/admin/transactions/financialaccount/

## API Endpoints
### Create Auth Token
```shell
curl --location --request POST '127.0.0.1:8000/api/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "admin",
    "password": "123qwe"
}'
```

### Retrieve all transactions for user (FinancialAccount)

```shell
curl --location --request GET '127.0.0.1:8000/api/account/<FINANCIAL_ACCOUNT_ID>/transactions/' \
--header 'Authorization: Bearer <ACCESS_TOKEN>'
```

### Get Account summary (FinancialAccount)

This includes user datails and balance
```shell
curl --location --request GET '127.0.0.1:8000/api/account/<FINANCIAL_ACCOUNT_ID>/' \
--header 'Authorization: Bearer <ACCESS_TOKEN>'
```