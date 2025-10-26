import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export const Navbar = () => {
	const navigate = useNavigate()
	const [auth, setAuth] = useState(!!sessionStorage.getItem('token'))
	const [email, setEmail] = useState(null)

	useEffect(() => {
		const onStorage = () => setAuth(!!sessionStorage.getItem('token'))
		window.addEventListener('storage', onStorage)
		return () => window.removeEventListener('storage', onStorage)
	}, [])

	useEffect(() => {
		const token = sessionStorage.getItem('token')
		if (!token) return setEmail(null)
		try {
			const payload = JSON.parse(atob(token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')))
			setEmail(payload.email || null)
		} catch (e) {
			setEmail(null)
		}
	}, [auth])

	const logout = () => {
		sessionStorage.removeItem('token')
		setAuth(false)
		navigate('/login')
	}

	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">React Boilerplate</span>
				</Link>
				<div className="ml-auto">
					{!auth && (
						<>
							<Link to="/signup"><button className="btn btn-outline-primary me-2">Signup</button></Link>
							<Link to="/login"><button className="btn btn-outline-secondary me-2">Login</button></Link>
						</>
					)}
					<Link to="/demo"><button className="btn btn-primary me-2">Demo</button></Link>
					{auth && <Link to="/private"><button className="btn btn-outline-success me-2">Private</button></Link>}
					{auth && email && <span className="me-2">{email}</span>}
					{auth && <button className="btn btn-danger" onClick={logout}>Logout</button>}
				</div>
			</div>
		</nav>
	);
};