from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    r = client.get('/')
    assert r.status_code == 200

def test_auth_and_patient_flow():
    client.post('/api/auth/register', json={'email':'t@t.com','password':'x'})
    token = client.post('/api/auth/login', json={'email':'t@t.com','password':'x'}).json()['access_token']
    h = {'Authorization': f'Bearer {token}'}
    r = client.post('/api/patients', json={'name':'Test','age':30,'gender':'Male','contact':'-'} , headers=h)
    assert r.status_code == 200
    pid = r.json()['id']
    r2 = client.post('/api/records', json={'patient_id':pid,'note':'fever and cough'}, headers=h)
    assert r2.status_code == 200
    r3 = client.get(f'/api/records/{pid}', headers=h)
    assert r3.status_code == 200
