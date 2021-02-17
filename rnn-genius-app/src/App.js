import React, { useState } from 'react'
import axios from 'axios'

import './App.css';

import Output from './components/Output'

const App = () => {

  const [outputText, setOutputText] = useState("Output text will go here.")
  const [inputText, setInputText] = useState('[Intro]')
  const [temp, setTemp] = useState("0.85")
  const [len, setLen] = useState("1000")
  
  const handleSubmit = (e) => {
    e.preventDefault()

    let text = "Make call here"
    setOutputText(text)
  }


  return (
    <div className="App">
      <div className='inputs-div'>
        <label>Base Model</label>
        <select name="model">
          <option value="model1">Embedded → GRU → Dense</option>
        </select>

        <label>Finetune</label>
        <select name="finetune">
          <option value="BROCKHAMPTON">BROCKHAMPTON</option>
        </select>

        <label>Temperature ((0, 1]) </label>
        <input type="number" value={temp} onChange={e => setTemp(e.target.value)}/>
        <label>Length</label>
        <input type="number" value={len} onChange={e => setLen(e.target.value)}/>
        <label>Input Text</label>
        <input type="text" value={inputText} onChange={e => setInputText(e.target.value)}/>

        <input type="submit" value="Generate Lyrics" onClick={handleSubmit} className="submit-button"/>
      </div>


      <div className="output-div">
        <Output text={outputText}></Output>
      </div>
      
    </div>
  );
}

export default App;
