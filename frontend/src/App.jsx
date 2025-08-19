import React from 'react'
import VoiceRecorder from './components/VoiceRecorder'
import PatientDashboard from './components/PatientDashboard'
import DoctorInterface from './components/DoctorInterface'
import { Link, Routes, Route } from 'react-router-dom'

export default function App(){
  return (
    <div style={{fontFamily:'system-ui', padding:16}}>
      <h2>🏥 ArogyaLite-UHR</h2>
      <nav style={{display:'flex', gap:12, marginBottom:16}}>
        <Link to="/">Dashboard</Link>
        <Link to="/doctor">Doctor</Link>
        <Link to="/voice">Voice</Link>
      </nav>
      <Routes>
        <Route path="/" element={<PatientDashboard/>}/>
        <Route path="/doctor" element={<DoctorInterface/>}/>
        <Route path="/voice" element={<VoiceRecorder/>}/>
      </Routes>
    </div>
  )
}
