import React from 'react'
import './App.css'
import Graph from './components/Graph'

export default function App() {
  return (
    <div className="App" style={{ padding: '2rem' }}>
      <h1>Historical Price Dashboard</h1>
      <Graph />
    </div>
  )
}
