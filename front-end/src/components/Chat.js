import React, { useEffect, useState } from 'react';
import axios from 'axios';
import socketService from '../services/socket';
import ChatInput from './ChatInput';
import ChatMessages from './ChatMessages';
import DebugBox from './DebugBox';
import './Chat.css';
import { delay } from './delay';
import { useNavigate } from 'react-router-dom';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [showDebug, setShowDebug] = useState(false);
  const [debugText, setDebugText] = useState(''); // This will contain the debug string
  const [isBotTyping, setIsBotTyping] = useState(false);
  const [selectedVersion, setSelectedVersion] = useState('v1');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const token = localStorage.getItem('access');
        const response = await axios.get(`${process.env.REACT_APP_HTTP_HOST}/chat/chat-history/`, {
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
        { source: 'bot', text: message.text.msg }
      ]);
      console.log(message)
      setDebugText((prev_text) => message.text.debug);
      setIsBotTyping(false);
    });
  }, []);

  const sendMessage = (message) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { source: 'user', text: message, version: selectedVersion }
    ]);
    socketService.sendMessage({ source: 'user', text: message, version: selectedVersion });
    setIsBotTyping(true);
  };

  const handleLogout = () => {
    // Your logout logic here
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    socketService.socket.close();
    navigate('/login'); // Redirect to login page after logout
  };

  const handleVersionChange = (event) => {
    setSelectedVersion(event.target.value);
  };

  const handleEdit = () => {
    navigate("/editor")
  };

  const toggleDebugBox = () => {
    setShowDebug(!showDebug);
  };

  return (
    <div className="chat-container">

      <header className="App-header">
        <div>
          <h1>🤖 ANA-Assistant 🤖</h1>
        </div>
        <div className="header-buttons">
          <button onClick={handleEdit} className="logout-button">Prompt Editor</button>
          <button onClick={toggleDebugBox} className="toggle-debug-button">
            {showDebug ? 'Hide Debug' : 'Show Debug'}
          </button>
          <button onClick={handleLogout} className="logout-button">Logout</button>
          <select value={selectedVersion} onChange={handleVersionChange} className="version-select">
            <option value="v1">Version 1</option>
            <option value="v2">Version 2</option>
          </select>
        </div>
      </header>

      <DebugBox debugText={debugText} isVisible={showDebug} onClose={toggleDebugBox} />

      <ChatMessages messages={messages} />
      {isBotTyping && <div className="typing-indicator">Anna is thinking...</div>}
      <ChatInput sendMessage={sendMessage} isBotTyping={isBotTyping} />
    </div>
  );
};

export default Chat;
