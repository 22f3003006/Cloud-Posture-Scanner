import { useState } from 'react'
import './App.css'
import EC2 from './components/EC2'
import S3 from './components/S3'
import Results from './components/Results'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <h1 className='heading'>Cloud Posture Scanner Dashboard</h1>
      <div className='comp'>
        <EC2/>
        <S3/>
      </div>
      <div className='res'><Results/></div>
    </div>
  )
}

export default App
