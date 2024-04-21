// src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    axios.get('http://localhost/api/message')
      // console.log("message")
      .then(response => {
        console.log("message", response)
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('Error fetching message:', error);
      });
  }, []);

  const handleMessageChange = (event) => {
    setNewMessage(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.post('http://localhost/api/message', { newMessage })
      .then(response => {
        setMessage(response.data.message);
        setNewMessage('');
      })
      .catch(error => {
        console.error('Error setting message:', error);
      });
  };

  return (
    <div className="App">
      <h1>Simple React App</h1>
      <p>Current Message: {message}</p>
      <form onSubmit={handleSubmit}>
        <input type="text" value={newMessage} onChange={handleMessageChange} />
        <button type="submit">Set Message</button>
      </form>
    </div>
  );
}

export default App;
