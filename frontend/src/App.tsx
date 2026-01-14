import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import CreatePortfolio from './pages/CreatePortfolio'
import PortfolioDetail from './pages/PortfolioDetail'

function App() {
  const { token } = useAuthStore()

  return (
    <Router>
      <div className="app">
        <Navbar />
        <div className="container">
          <Routes>
            <Route path="/login" element={!token ? <Login /> : <Navigate to="/dashboard" />} />
            <Route path="/signup" element={!token ? <Signup /> : <Navigate to="/dashboard" />} />
            <Route path="/dashboard" element={token ? <Dashboard /> : <Navigate to="/login" />} />
            <Route path="/portfolio/create" element={token ? <CreatePortfolio /> : <Navigate to="/login" />} />
            <Route path="/portfolio/:id" element={token ? <PortfolioDetail /> : <Navigate to="/login" />} />
            <Route path="/" element={<Navigate to={token ? "/dashboard" : "/login"} />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App

