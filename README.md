# Telegram Promoções

O projeto possui uma API Python, um monitor do Telegram e uma interface React.
Os produtos, grupos e promoções são persistidos em `data/app_data.json`.

## Configuração segura

Copie `.env.example` para `.env` e preencha as credenciais localmente. O arquivo
`.env`, as sessões do Telegram e `data/app_data.json` são ignorados pelo Git e
nunca devem ser publicados.

## Executar

Abra três terminais na pasta do projeto.

### 1. API Python

```powershell
.\venv\Scripts\python.exe main.py
```

A API ficará disponível em `http://127.0.0.1:8000`.

### 2. Monitor do Telegram

```powershell
.\venv\Scripts\python.exe -u monitor_test.py
```

O monitor usa os produtos cadastrados pelo front-end e grava no JSON as
promoções aprovadas.

### 3. Front-end React

```powershell
cd frontend
npm.cmd run dev
```

Abra o endereço exibido pelo Vite, normalmente `http://localhost:5173`.

## Endpoints

- `GET /api/health`
- `GET /api/dashboard`
- `POST /api/products`
- `DELETE /api/products/{id}`
- `POST /api/groups`
- `DELETE /api/groups/{telegram_id}`
