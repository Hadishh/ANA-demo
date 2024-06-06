// ChatInput.js

import React, { useState } from 'react';
import './ChatInput.css';

const ChatInput = ({ sendMessage, isBotTyping }) => {
  const [message, setMessage] = useState('');

  const handleChange = (event) => {
    setMessage(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (message.trim()) {
      sendMessage(message);
      setMessage('');
    }
  };

  return (
    <form className="chat-input-form" onSubmit={handleSubmit}>
      <textarea
        className="chat-input"
        value={message}
        onChange={handleChange}
        rows="3"
        placeholder="Type a message..."
      />
      <button type="submit" className="send-button" disabled={isBotTyping}>Send</button>
    </form>
  );
};

export default ChatInput;
