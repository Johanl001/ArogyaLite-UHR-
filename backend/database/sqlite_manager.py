import sqlite3
from typing import Dict, List

class SQLiteManager:
    def __init__(self, path: str):
        self.path = path

    def _conn(self):
        return sqlite3.connect(self.path)

    def init_db(self):
        con = self._conn(); con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT, contact TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, patient_id INTEGER, note TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
        con.commit(); con.close()

    # Users
    def add_user(self, email: str, password_hash: str) -> int:
        con = self._conn(); cur = con.cursor()
        cur.execute("INSERT INTO users(email, password) VALUES(?,?)", (email, password_hash))
        con.commit(); uid = cur.lastrowid; con.close(); return uid

    def get_user(self, email: str):
        con = self._conn(); con.row_factory = sqlite3.Row; cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        row = cur.fetchone(); con.close(); return dict(row) if row else None

    # Patients
    def add_patient(self, data: Dict) -> int:
        con = self._conn(); cur = con.cursor()
        cur.execute("INSERT INTO patients(name, age, gender, contact) VALUES(?,?,?,?)",
                    (data.get("name"), data.get("age"), data.get("gender"), data.get("contact")))
        con.commit(); pid = cur.lastrowid; con.close(); return pid

    def list_patients(self) -> List[Dict]:
        con = self._conn(); con.row_factory = sqlite3.Row; cur = con.cursor()
        cur.execute("SELECT * FROM patients ORDER BY id DESC")
        rows = [dict(r) for r in cur.fetchall()]; con.close(); return rows

    # Records
    def add_record(self, data: Dict) -> int:
        con = self._conn(); cur = con.cursor()
        cur.execute("INSERT INTO records(patient_id, note) VALUES(?,?)", (data.get("patient_id"), data.get("note")))
        con.commit(); rid = cur.lastrowid; con.close(); return rid

    def get_records(self, patient_id: int) -> List[Dict]:
        con = self._conn(); con.row_factory = sqlite3.Row; cur = con.cursor()
        cur.execute("SELECT * FROM records WHERE patient_id=? ORDER BY created_at DESC", (patient_id,))
        rows = [dict(r) for r in cur.fetchall()]; con.close(); return rows
