import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { portfolioAPI } from '../services/api'
import './Dashboard.css'

interface Portfolio {
  id: number
  name: string
  initial_invest_amount: number
  description: string | null
  created_at: string
}

export default function Dashboard() {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadPortfolios()
  }, [])

  const loadPortfolios = async () => {
    try {
      const response = await portfolioAPI.list()
      setPortfolios(response.data)
    } catch (err: any) {
      setError('포트폴리오를 불러오는데 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: number, name: string) => {
    if (!confirm(`"${name}" 포트폴리오를 삭제하시겠습니까?`)) {
      return
    }

    try {
      await portfolioAPI.delete(id)
      setPortfolios(portfolios.filter(p => p.id !== id))
      alert('포트폴리오가 삭제되었습니다.')
    } catch (err) {
      alert('포트폴리오 삭제에 실패했습니다.')
    }
  }

  if (loading) {
    return <div className="loading">로딩 중...</div>
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>내 포트폴리오</h1>
        <Link to="/portfolio/create" className="btn btn-primary">
          새 포트폴리오 만들기
        </Link>
      </div>

      {error && <div className="error">{error}</div>}

      {portfolios.length === 0 ? (
        <div className="card empty-state">
          <p>아직 생성된 포트폴리오가 없습니다.</p>
          <Link to="/portfolio/create" className="btn btn-primary">
            첫 포트폴리오 만들기
          </Link>
        </div>
      ) : (
        <div className="portfolio-grid">
          {portfolios.map((portfolio) => (
            <div key={portfolio.id} className="portfolio-card card">
              <h3>{portfolio.name}</h3>
              {portfolio.description && <p className="description">{portfolio.description}</p>}
              <div className="portfolio-info">
                <div className="info-item">
                  <span className="label">초기 투자금</span>
                  <span className="value">₩{portfolio.initial_invest_amount.toLocaleString()}</span>
                </div>
                <div className="info-item">
                  <span className="label">생성일</span>
                  <span className="value">{new Date(portfolio.created_at).toLocaleDateString()}</span>
                </div>
              </div>
              <div className="portfolio-actions">
                <Link to={`/portfolio/${portfolio.id}`} className="btn btn-primary">
                  상세보기
                </Link>
                <button 
                  onClick={() => handleDelete(portfolio.id, portfolio.name)}
                  className="btn btn-danger"
                >
                  삭제
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

