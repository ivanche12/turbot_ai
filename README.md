# TurBot – Chat Aplikacija

Interaktivna web aplikacija sa frontend-om u React-u i backend-om u FastAPI. Omogućava vođenje i čuvanje razgovora sa AI agentom.

---

## Tehnologije korišćene

- **Frontend**: React.js + Tailwind CSS  
- **Backend**: FastAPI (Python)  
- **Lokalno čuvanje sesija**: `localStorage`  
- **API komunikacija**: REST

---

## Pokretanje projekta

### 1. Backend

1. Instaliraj Python requirements-a:
   ```bash
   pip install -r requirements.txt
   ```
2. Pokreni FastAPI server iz backend/ direktorijuma:
    ```bash
    cd backend
    uvicorn app:app --reload
    ```
### 2. Frontend
1. U drugom terminalu uraditi:
    ```bash
    cd frontend
    npm install # prvi put
    npm start
    ```
---
### NAPOMENA

Backend mora biti pokrenut pre frontenda.