// ChatMessages.js

import React, { useEffect, useRef } from 'react';
import './ChatMessages.css';

const ChatMessages = ({ messages }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]); // Scroll to bottom whenever messages change

  return (
    <div className="chat-messages">
      {messages.map((message, index) => (
        <div key={index} className={`message ${message.source}`}>
          <span>{message.text}</span>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatMessages;
