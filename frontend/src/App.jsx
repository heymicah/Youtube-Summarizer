import React from 'react';
import { useState } from 'react';
import ReactDOM from 'react-dom/client';
import './App.css';

function App() {
  const [userInput, setUserInput] = useState('')
  const [summary, setSummary] = useState('')
  const handleInputChange = (event) => {
    setUserInput(event.target.value)
  }
  const handleSubmit = (async() => {
    const response = await fetch('http://127.0.0.1:5000/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({link: userInput})
    })
    if(response.ok) {
      const data = await response.json()
      console.log(data.summary)
      setSummary(data.summary)
    }
  }
  )
  return (
    <div className="App">
      <header className="App-header">
        <div>
          <input onChange={handleInputChange} value={userInput}></input>
          <button onClick={handleSubmit}>Submit</button>
        </div>
      </header>
    </div>
  );
}

export default App;
