import React, { useEffect, useState } from 'react';
import axios from 'axios';
import socketService from '../services/socket';
import ChatInput from './ChatInput';
import ChatMessages from './ChatMessages';
import './Chat.css';
import { delay } from './delay';
import { useNavigate } from 'react-router-dom';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const token = localStorage.getItem('access');
        const response = await axios.get('http://localhost:8000/chat/chat-history/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        
        setMessages(response.data);
      } catch (error) {
        if (error.response.status == 401)
          navigate("/login");
        
        console.error('Error fetching chat history:', error);
      }
    };

    fetchChatHistory();

    socketService.connect();

    socketService.onMessage(async (message) => {
      setMessages((prevMessages) => [
        ...prevMessages, 
        { source: 'bot', text: message.msg }
      ]);
      setIsBotTyping(false);
    });
  }, []);

  const sendMessage = (message) => {
    setMessages((prevMessages) => [
      ...prevMessages, 
      { source: 'user', text: message }
    ]);
    socketService.sendMessage(message);
    setIsBotTyping(true);
  };

  const handleLogout = () => {
    // Your logout logic here
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    socketService.socket.close();
    navigate('/login'); // Redirect to login page after logout
  };

  return (
    <div className="chat-container">
      <header className="App-header">
        <div>
          <h1>🤖 ANA-Assistant 🐍</h1>
        </div>
        <div>
          <button onClick={handleLogout} className="logout-button">Logout</button>
        </div>
      </header>
      <ChatMessages messages={messages} />
      {isBotTyping && <div className="typing-indicator">Anna is thinking...</div>}
      <ChatInput sendMessage={sendMessage} isBotTyping={isBotTyping} />
    </div>
  );
};

export default Chat;
