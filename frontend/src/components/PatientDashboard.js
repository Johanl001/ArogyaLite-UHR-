import { useEffect, useState } from 'react'
import { getToken } from '../utils/localStorage'

export default function PatientDashboard(){
  const [patients, setPatients] = useState([])
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

  return (
    <div>
      <h3>Patients</h3>
      {patients.length===0 ? <p>No patients yet.</p> :
        <ul>{patients.map(p=>(<li key={p.id}>{p.name} ({p.gender}, {p.age})</li>))}</ul>
      }
    </div>
  )
}
