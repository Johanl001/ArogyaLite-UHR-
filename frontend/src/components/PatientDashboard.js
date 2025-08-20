import { useEffect, useState } from 'react'
import { getToken } from '../utils/localStorage'

export default function PatientDashboard(){
  const [patients, setPatients] = useState([])
  const [patientId, setPatientId] = useState('')
  const [patient, setPatient] = useState(null)
  const api = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  async function ensureDemoAuth(){
    const saved = getToken()
    if(saved) return saved
    // create demo user (idempotent)
    await fetch(`${api}/api/auth/register`, {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({email:'demo@uhr.local', password:'demo123'})
    }).catch(()=>{})
    const res = await fetch(`${api}/api/auth/login`,{
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({email:'demo@uhr.local', password:'demo123'})
    })
    const js = await res.json()
    localStorage.setItem('token', js.access_token)
    return js.access_token
  }

  useEffect(()=>{
    (async ()=>{
      const token = await ensureDemoAuth()
      const res = await fetch(`${api}/api/patients`, { headers: { Authorization:`Bearer ${token}` }})
      const js = await res.json()
      setPatients(js)
    })()
  },[])

  async function fetchById(){
    const t = await ensureDemoAuth()
    if(!patientId) return
    const res = await fetch(`${api}/api/patients/${patientId}`, { headers:{ Authorization:`Bearer ${t}` }})
    const js = await res.json(); setPatient(js)
  }

  return (
    <div>
      <h3>Patients</h3>
      {patients.length===0 ? <p>No patients yet.</p> :
        <ul>{patients.map(p=>(<li key={p.id}>{p.name} ({p.gender}, {p.age})</li>))}</ul>
      }
      <div style={{marginTop:12}}>
        <h4>Find Patient by ID</h4>
        <input placeholder="Patient ID" value={patientId} onChange={e=>setPatientId(e.target.value)} />
        <button onClick={fetchById} style={{marginLeft:8}}>Fetch</button>
        {patient && (
          <pre style={{whiteSpace:'pre-wrap', marginTop:8}}>{JSON.stringify(patient, null, 2)}</pre>
        )}
      </div>
    </div>
  )
}
