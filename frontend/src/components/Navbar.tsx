import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import './Navbar.css'

export default function Navbar() {
  const { token, email, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          📊 Portfolio Manager
        </Link>
        
        <div className="navbar-menu">
          {token ? (
            <>
              <Link to="/dashboard" className="navbar-link">
                대시보드
              </Link>
              <Link to="/portfolio/create" className="navbar-link">
                포트폴리오 생성
              </Link>
              <span className="navbar-user">{email}</span>
              <button onClick={handleLogout} className="btn btn-secondary">
                로그아웃
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-link">
                로그인
              </Link>
              <Link to="/signup" className="navbar-link">
                회원가입
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

