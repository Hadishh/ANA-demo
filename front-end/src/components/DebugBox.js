// DebugBox.js
import React, { useEffect, useRef } from 'react';

import './DebugBox.css';

const DebugBox = ({ debugText, isVisible, onClose }) => {

    const boxRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (boxRef.current && !boxRef.current.contains(event.target)) {
                onClose();
            }
        };

        if (isVisible) {
            document.addEventListener('mousedown', handleClickOutside);
        } else {
            document.removeEventListener('mousedown', handleClickOutside);
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [isVisible, onClose]);

    return (
        <div className={`debug-overlay ${isVisible ? 'visible' : ''}`}>
            <div className="debug-box" ref={boxRef}>
                <button className="close-button" onClick={onClose}>X</button>
                <div className="debug-message">
                    {debugText}
                </div>
            </div>
        </div>
    );
};

export default DebugBox;