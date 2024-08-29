import React, { useEffect, useState } from 'react';
import axios from 'axios';
import socketService from '../services/socket';
import ChatInput from './ChatInput';
import ChatMessages from './ChatMessages';
import DebugBox from './DebugBox';
import './Chat.css';
import { useNavigate } from 'react-router-dom';


const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [showDebug, setShowDebug] = useState(false);
  const [debugText, setDebugText] = useState(''); // This will contain the debug string
  const [isBotTyping, setIsBotTyping] = useState(false);
  const [isVoiceEnabled, setIsVoiceEnabled] = useState(true);
  const [selectedVersion, setSelectedVersion] = useState('v2');
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

  }, [navigate]);

  useEffect(() => {
    socketService.onMessage(async (message) => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { source: 'bot', text: message.text.msg }
      ]);
      console.log(message)
      setDebugText((prev_text) => message.text.debug);
      if (isVoiceEnabled) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(message.text.msg);
        window.speechSynthesis.speak(utterance);
      }
      setIsBotTyping(false);
    });
  }, [navigate, isVoiceEnabled]);

  const sendMessage = (message) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { source: 'user', text: message, version: selectedVersion }
    ]);
    socketService.sendMessage({ source: 'user', text: message, version: selectedVersion });
    setIsBotTyping(true);
  };

  const handleDeleteAll = async () => {
    try {
      const token = localStorage.getItem('access');
      await axios.delete(`${process.env.REACT_APP_HTTP_HOST}/chat/chat-history/`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      setMessages([]);  // Clear messages from the state
      console.log('All messages deleted.');
    } catch (error) {
      if (error.response.status === 401) navigate("/login");

      console.error('Error deleting all messages:', error);
    }
  };

  const handleLogout = () => {
    // Your logout logic here
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    socketService.socket.close();
    window.speechSynthesis.cancel();

    navigate('/login'); // Redirect to login page after logout
  };

  const handleVersionChange = (event) => {
    setSelectedVersion(event.target.value);
  };

  const handleEdit = () => {
    window.open("/editor", "_blank");
  };

  const toggleDebugBox = () => {
    setShowDebug(!showDebug);
  };

  const toggleVoice = () => {
    if (isVoiceEnabled) {
      window.speechSynthesis.cancel(); // Stop current speech if toggling off
    }
    setIsVoiceEnabled(prevState => !prevState);
  };

  return (
    <div className="chat-container">

      <header className="App-header">
        <div>
          <h1>🤖 ANA-Assistant 🤖</h1>
        </div>
        <div className="header-buttons">
          <button onClick={handleEdit} className="logout-button">Editor</button>
          <button onClick={toggleDebugBox} className="toggle-debug-button">
            {showDebug ? 'Hide Debug' : 'Show Debug'}
          </button>
          <button onClick={handleLogout} className="logout-button">Logout</button>
          <button onClick={handleDeleteAll} className="logout-button">Clear History</button>
          <button onClick={toggleVoice} className="logout-button">
            {isVoiceEnabled ? 'Disable Voice' : 'Enable Voice'}
          </button>
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
