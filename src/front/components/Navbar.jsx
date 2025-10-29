import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export const Navbar = () => {
	const navigate = useNavigate()
	const [userEmail, setUserEmail] = useState(null)

	const logout = () => {
		sessionStorage.removeItem('token')
		setUserEmail(null)
		navigate('/login')
	}

	useEffect(() => {
		const token = sessionStorage.getItem('token')
		if (!token) return
		fetch(`${import.meta.env.VITE_BACKEND_URL}/api/private`, {
			headers: { 'Authorization': 'Bearer ' + token }
		}).then(async res => {
			if (!res.ok) return
			const data = await res.json()
			setUserEmail(data.user?.email || null)
		}).catch(() => {})
	}, [])

	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">React Boilerplate</span>
				</Link>
				<div className="ml-auto d-flex align-items-center">
					{userEmail ? (
						<>
							<span className="me-3">{userEmail}</span>
							<Link to="/private"><button className="btn btn-outline-primary me-2">Private</button></Link>
							<button className="btn btn-danger" onClick={logout}>Logout</button>
						</>
					) : (
						<>
							<Link to="/signup"><button className="btn btn-outline-primary me-2">Signup</button></Link>
							<Link to="/login"><button className="btn btn-outline-secondary me-2">Login</button></Link>
							<Link to="/demo"><button className="btn btn-primary me-2">Demo</button></Link>
						</>
					)}
				</div>
			</div>
		</nav>
	);
};
