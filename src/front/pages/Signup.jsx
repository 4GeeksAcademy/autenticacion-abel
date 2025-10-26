import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export const Signup = () => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        })
        if (res.ok) {
            navigate('/login')
        } else {
            const data = await res.json()
            alert(data.message || 'error')
        }
    }

    return (
        <div className="container mt-5">
            <h3>Signup</h3>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <input className="form-control" placeholder="email" value={email} onChange={e => setEmail(e.target.value)} />
                </div>
                <div className="mb-3">
                    <input type="password" className="form-control" placeholder="password" value={password} onChange={e => setPassword(e.target.value)} />
                </div>
                <button className="btn btn-primary">Signup</button>
            </form>
        </div>
    )
}
