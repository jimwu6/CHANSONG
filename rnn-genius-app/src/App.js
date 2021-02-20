import React, { useState } from 'react'
import axios from 'axios'

import './App.css';

import Output from './components/Output'

const App = () => {

  const [outputText, setOutputText] = useState("Output text will go here.")
  const [inputText, setInputText] = useState('[Intro]')
  const [temp, setTemp] = useState("0.85")
  const [len, setLen] = useState("1000")
  const [addrtype, setAddrtype] = useState([
    ["model_17_base", "Embedded → GRU (1024) → Dense, SEQ_LEN = 200"],
    ["model_15_base", "Embedded → LSTM (1024) → Dense, SEQ_LEN = 200"],
    ["model_19_base", "Embedded → GRU (768) → GRU (768) → Dense, SEQ_LEN = 200"],
    ["model_19_base", "Embedded → GRU (768) → GRU (768) → Dense, SEQ_LEN = 300"],
    ["model_20_base", "Embedded → LSTM (768) → LSTM (768) → Dense, SEQ_LEN = 200"],
    ["model_21_base", "Embedded → LSTM (768) → LSTM (768) → Dense, SEQ_LEN = 300"]
    ])
  const [addr, setAddr] = useState(addrtype[0][0])

  const Add = addrtype.map(Add => Add)
  const handleAddrTypeChange = (e) => {
    setAddr(e.target.value)
    console.log(e.target.value)
    // console.log((addrtype[e.target.value]))
  }


  const handleSubmit = (e) => {
    e.preventDefault()

    let params =  {
      model_name: addr, 
      input_text: inputText,
      length: len,
      temperature: temp
    }
    console.log("Submitting " + addr)
    axios.get('localhost:5000/', {params})
      .then(res => setOutputText(res.data))

  }

  return (
    <div className="App">
      <div className='inputs-div'>

        <label>Base Model</label>
        <select
        onChange={e => handleAddrTypeChange(e)} >
        {
          Add.map((address, key) => <option key={key} value={address[0]}>{address[1]}</option>)
        }
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
