import { useState } from 'react'
import { getToken } from '../utils/localStorage'

export default function DoctorInterface(){
  const [pid, setPid] = useState(1)
  const [name, setName] = useState('')
  const [age, setAge] = useState(30)
  const [gender, setGender] = useState('Male')
  const [contact, setContact] = useState('')
  const [note, setNote] = useState('')
  const [msg, setMsg] = useState('')
  const [ai, setAi] = useState(null)
  const api = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  async function token(){ return getToken() }

  const addPatient = async () => {
    const t = await token()
    const res = await fetch(`${api}/api/patients`, { method:'POST',
      headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${t}` },
      body: JSON.stringify({ name, age:Number(age), gender, contact })
    })
    const js = await res.json(); setMsg(`Created patient id ${js.id}`)
  }

  const addRecord = async () => {
    const t = await token()
    const res = await fetch(`${api}/api/records`, { method:'POST',
      headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${t}` },
      body: JSON.stringify({ patient_id:Number(pid), note })
    })
    const js = await res.json(); setMsg(`Added record id ${js.id}`)
  }

  const analyzeNote = async () => {
    const t = await token()
    const res = await fetch(`${api}/api/ai/analyze`, { method:'POST',
      headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${t}` },
      body: JSON.stringify({ note })
    })
    const js = await res.json(); setAi(js)
  }

  return (
    <div>
      <h3>Doctor Interface</h3>
      <div style={{display:'grid', gap:8, maxWidth:480}}>
        <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
        <input placeholder="Age" value={age} onChange={e=>setAge(e.target.value)} />
        <select value={gender} onChange={e=>setGender(e.target.value)}>
          <option>Male</option><option>Female</option><option>Other</option>
        </select>
        <input placeholder="Contact" value={contact} onChange={e=>setContact(e.target.value)} />
        <button onClick={addPatient}>Create Patient</button>
      </div>
      <hr/>
      <div style={{display:'grid', gap:8, maxWidth:480}}>
        <input placeholder="Patient ID" value={pid} onChange={e=>setPid(e.target.value)} />
        <textarea rows={5} placeholder="Clinical Note" value={note} onChange={e=>setNote(e.target.value)} />
        <div style={{display:'flex', gap:8}}>
          <button onClick={addRecord}>Add Record</button>
          <button onClick={analyzeNote}>AI Analyze</button>
        </div>
      </div>
      <p>{msg}</p>
      {ai && (
        <div style={{marginTop:12}}>
          <h4>AI Assistant</h4>
          <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(ai, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
