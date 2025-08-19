export default function VoiceRecorder(){
  let recognizer = null
  const start = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition
    if(!SR){ alert('Web Speech API not supported'); return }
    recognizer = new SR()
    recognizer.continuous = true
    recognizer.interimResults = true
    recognizer.lang = 'en-US'
    recognizer.onresult = (e) => {
      const text = Array.from(e.results).map(r=>r[0].transcript).join(' ')
      document.getElementById('out').value = text
    }
    recognizer.start()
  }
  const stop = () => recognizer && recognizer.stop()
  return (
    <div>
      <h3>🎙️ Voice to Text (Browser)</h3>
      <button onClick={start}>Start</button>
      <button onClick={stop} style={{marginLeft:8}}>Stop</button>
      <textarea id="out" rows={8} style={{width:'100%', marginTop:12}} placeholder="Dictation output..."></textarea>
    </div>
  )
}
