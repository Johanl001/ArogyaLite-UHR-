# API (Base: /api)

## Auth
- `POST /auth/register` {email, password}
- `POST /auth/login` {email, password} → {access_token}

Use header: `Authorization: Bearer <token>`

## Patients
- `POST /patients` {name, age, gender, contact} → {id}
- `GET /patients` → list

## Records
- `POST /records` {patient_id, note} → {id}
- `GET /records/{patient_id}` → list
