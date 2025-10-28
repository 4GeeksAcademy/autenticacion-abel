import { Link, useNavigate } from "react-router-dom";

export const Navbar = () => {
	const navigate = useNavigate()
	const logout = () => {
		sessionStorage.removeItem('token')
		navigate('/login')
	}
	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">React Boilerplate</span>
				</Link>
				<div className="ml-auto">
					<Link to="/signup"><button className="btn btn-outline-primary me-2">Signup</button></Link>
					<Link to="/login"><button className="btn btn-outline-secondary me-2">Login</button></Link>
					<Link to="/demo"><button className="btn btn-primary me-2">Demo</button></Link>
					<button className="btn btn-danger" onClick={logout}>Logout</button>
				</div>
			</div>
		</nav>
	);
};
