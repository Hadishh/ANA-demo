import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css'; // Import local styles

const Login = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState('');

    const navigate = useNavigate();
    const { username: username, password } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async e => {
        e.preventDefault();
        const user = {
            username: username,
            password
        };
        try {
            const res = await axios.post('http://localhost:8000/users/login/', user);
            // console.log(res.data);
            localStorage.setItem('access', res.data.access);
            localStorage.setItem('refresh', res.data.refresh);
            navigate('/chat'); // Redirect to Chat component on successful login
        } catch (err) {
            console.error(err.response.data);
            setError(err.response.data.error); // Set error message as usual
            
        }
    };

    const goToRegister = () => {
        navigate('/register'); // Redirect to Register component
    };

    return (
        <div className="login-container"> {/* Use specific class name */}
            <h1>Login</h1>
            {error && <p className="error">{error}</p>} {/* Display error message */}
            <form onSubmit={onSubmit}>
                <input
                    type="username"
                    name="username"
                    placeholder="Username"
                    value={username}
                    onChange={onChange}
                    required
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={password}
                    onChange={onChange}
                    required
                />
                <button type="submit" className="login-button">Login</button> {/* Use specific class name */}
            </form>
            <p>
                Don't have an account?{' '}
                <span className="login-link" onClick={goToRegister}> {/* Use specific class name */}
                    Register
                </span>
            </p>
        </div>
    );
};

export default Login;
