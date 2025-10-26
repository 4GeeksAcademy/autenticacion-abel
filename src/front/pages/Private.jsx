import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

export const Private = () => {
    const [user, setUser] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        const token = sessionStorage.getItem('token')
        if (!token) return navigate('/login')
        fetch(`${import.meta.env.VITE_BACKEND_URL}/api/private`, {
            headers: { 'Authorization': 'Bearer ' + token }
        }).then(async res => {
            if (!res.ok) return navigate('/login')
            const data = await res.json()
            setUser(data.user)
        })
    }, [])

    return (
        <div className="container mt-5">
            <h3>Private Area</h3>
            {user ? <div><p>Welcome {user.email}</p></div> : <p>loading...</p>}
        </div>
    )
}
