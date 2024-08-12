import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const FileExplorer = () => {
    const [files, setFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);
    const [content, setContent] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Set up axios instance with authorization header
    const axiosInstance = axios.create({
        baseURL: `${process.env.REACT_APP_HTTP_HOST}/`,
    });

    axiosInstance.interceptors.request.use((config) => {
        const token = localStorage.getItem('access'); // Retrieve the token from local storage or any other storage
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    }, (error) => {
        return Promise.reject(error);
    });

    useEffect(() => {
        fetchFiles();
    }, []);

    const fetchFiles = async () => {
        try {
            setLoading(true);
            const response = await axiosInstance.get('core/prompts/');
            setFiles(response.data);
            console.log(response.data)
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    const handleFileClick = async (file) => {
        try {
            setLoading(true);
            const response = await axiosInstance.get(`core/prompts/${file.id}/`);
            setSelectedFile(file);
            setContent(response.data.text);
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        if (!selectedFile || !content) {
            alert('Please select a file and ensure content is not empty.');
            return;
        }

        try {
            setLoading(true);
            selectedFile.text = content;
            await axiosInstance.put(`core/prompts/${selectedFile.id}/`, selectedFile);
            alert('File saved successfully!');
            fetchFiles();
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    const handleBack = async () => {
        navigate("/chat")
    };
    return (
        <div className="file-explorer-container">
            <div className="file-list">
                <h2>File Explorer</h2>
                {loading && <div className="loading-spinner">Loading...</div>}
                {error && <div className="error-message">{error.message}</div>}
                {files.length > 0 ? (
                    <ul>
                        {files.map((file) => (
                            <li
                                key={file.id}
                                className={selectedFile && selectedFile.id === file.id ? 'selected' : ''}
                                onClick={() => handleFileClick(file)}
                            >
                                {file.name}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No files found.</p>
                )}
            </div>

            <div className="file-editor">
                {selectedFile ? (
                    <>
                        <div className="editor-header">
                            <h2>Editing: {selectedFile.name}</h2>
                            <div className='header-buttons'>
                                <button onClick={handleSave}>Save</button>
                                <button onClick={handleBack}>Back</button>
                            </div>
                        </div>
                        <textarea
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            rows="20"
                        ></textarea>
                    </>
                ) : (
                    <p>Select a file to start editing.</p>
                )}
            </div>
        </div>
    );
};

export default FileExplorer;