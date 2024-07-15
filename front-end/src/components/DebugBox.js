// DebugBox.js
import React from 'react';
import './DebugBox.css';

const DebugBox = ({ debugText, isVisible, onClose }) => {
    return (
        <div className={`debug-overlay ${isVisible ? 'visible' : ''}`}>
            <div className="debug-box">
                <button className="close-button" onClick={onClose}>X</button>
                <div className="debug-message">
                    {debugText}
                </div>
            </div>
        </div>
    );
};

export default DebugBox;