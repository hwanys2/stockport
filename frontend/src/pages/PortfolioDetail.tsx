import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { portfolioAPI } from '../services/api'
import './PortfolioDetail.css'

interface Asset {
  id: number
  symbol: string
  name: string
}

interface ItemAnalysis {
  item_id: number
  asset: Asset
  target_weight: number
  current_weight: number
  weight_diff: number
  tolerance: number
  is_out_of_range: boolean
  current_quantity: number
  current_price: number
  current_value: number
  entry_price: number
  initial_quantity: number
}

interface PortfolioAnalysis {
  portfolio: {
    id: number
    name: string
    description: string | null
    initial_invest_amount: number
    created_at: string
  }
  total_value: number
  initial_invest_amount: number
  total_return: number
  total_return_pct: number
  items: ItemAnalysis[]
}

export default function PortfolioDetail() {
  const { id } = useParams<{ id: string }>()
  const [analysis, setAnalysis] = useState<PortfolioAnalysis | null>(null)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState('')
  const [editingItemId, setEditingItemId] = useState<number | null>(null)
  const [editingQuantity, setEditingQuantity] = useState('')

  const navigate = useNavigate()

  useEffect(() => {
    loadAnalysis()
  }, [id])

  const loadAnalysis = async () => {
    try {
      const response = await portfolioAPI.analyze(parseInt(id!))
      setAnalysis(response.data)
      setError('')
    } catch (err: any) {
      setError('포트폴리오를 불러오는데 실패했습니다.')
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  const handleRefresh = () => {
    setRefreshing(true)
    loadAnalysis()
  }

  const handleEditQuantity = (item: ItemAnalysis) => {
    setEditingItemId(item.item_id)
    setEditingQuantity(item.current_quantity.toString())
  }

  const handleSaveQuantity = async (itemId: number) => {
    try {
      await portfolioAPI.updateItemQuantity(
        parseInt(id!),
        itemId,
        parseFloat(editingQuantity)
      )
      setEditingItemId(null)
      loadAnalysis()
    } catch (err) {
      alert('수량 업데이트에 실패했습니다.')
    }
  }

  const handleCancelEdit = () => {
    setEditingItemId(null)
    setEditingQuantity('')
  }

  const getWeightCellClass = (item: ItemAnalysis) => {
    if (!item.is_out_of_range) return ''
    
    const diff = Math.abs(item.weight_diff)
    if (diff > item.tolerance * 1.5) return 'danger-cell'
    return 'warning-cell'
  }

  if (loading) {
    return <div className="loading">로딩 중...</div>
  }

  if (error || !analysis) {
    return (
      <div className="error-container">
        <p className="error">{error}</p>
        <Link to="/dashboard" className="btn btn-primary">
          대시보드로 돌아가기
        </Link>
      </div>
    )
  }

  const { portfolio, total_value, total_return, total_return_pct, items } = analysis

  return (
    <div className="portfolio-detail">
      {/* 헤더 */}
      <div className="detail-header">
        <div>
          <h1>{portfolio.name}</h1>
          {portfolio.description && <p className="description">{portfolio.description}</p>}
        </div>
        <div className="header-actions">
          <button
            onClick={handleRefresh}
            className="btn btn-secondary"
            disabled={refreshing}
          >
            {refreshing ? '새로고침 중...' : '🔄 새로고침'}
          </button>
          <button
            onClick={() => navigate('/dashboard')}
            className="btn btn-primary"
          >
            대시보드
          </button>
        </div>
      </div>

      {/* 요약 정보 */}
      <div className="summary-cards">
        <div className="summary-card card">
          <div className="summary-label">초기 투자금</div>
          <div className="summary-value">₩{portfolio.initial_invest_amount.toLocaleString()}</div>
        </div>
        
        <div className="summary-card card">
          <div className="summary-label">현재 평가금액</div>
          <div className="summary-value">₩{total_value.toLocaleString(undefined, { maximumFractionDigits: 0 })}</div>
        </div>
        
        <div className="summary-card card">
          <div className="summary-label">수익금</div>
          <div className={`summary-value ${total_return >= 0 ? 'positive' : 'negative'}`}>
            {total_return >= 0 ? '+' : ''}₩{total_return.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </div>
        </div>
        
        <div className="summary-card card">
          <div className="summary-label">수익률</div>
          <div className={`summary-value ${total_return_pct >= 0 ? 'positive' : 'negative'}`}>
            {total_return_pct >= 0 ? '+' : ''}{total_return_pct.toFixed(2)}%
          </div>
        </div>
      </div>

      {/* 종목별 상세 정보 */}
      <div className="card">
        <h2>포트폴리오 구성</h2>
        
        <div className="table-container">
          <table className="detail-table">
            <thead>
              <tr>
                <th>종목</th>
                <th>목표 비중</th>
                <th>현재 비중</th>
                <th>차이</th>
                <th>허용 오차</th>
                <th>현재가</th>
                <th>수량</th>
                <th>평가금액</th>
                <th>수익률</th>
                <th>액션</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => {
                const isEditing = editingItemId === item.item_id
                const itemReturn = ((item.current_price - item.entry_price) / item.entry_price) * 100
                
                return (
                  <tr key={item.item_id} className={item.is_out_of_range ? 'out-of-range-row' : ''}>
                    <td>
                      <strong>{item.asset.symbol}</strong>
                      <br />
                      <small>{item.asset.name}</small>
                    </td>
                    <td>{item.target_weight.toFixed(2)}%</td>
                    <td className={getWeightCellClass(item)}>
                      {item.current_weight.toFixed(2)}%
                    </td>
                    <td className={item.is_out_of_range ? 'danger-cell' : ''}>
                      {item.weight_diff >= 0 ? '+' : ''}{item.weight_diff.toFixed(2)}%
                    </td>
                    <td>±{item.tolerance.toFixed(1)}%</td>
                    <td>
                      ${item.current_price.toFixed(2)}
                      <br />
                      <small className="entry-price">진입: ${item.entry_price.toFixed(2)}</small>
                    </td>
                    <td>
                      {isEditing ? (
                        <input
                          type="number"
                          className="input input-sm"
                          value={editingQuantity}
                          onChange={(e) => setEditingQuantity(e.target.value)}
                          step="0.01"
                          min="0"
                          autoFocus
                        />
                      ) : (
                        <>
                          {item.current_quantity.toFixed(4)}
                          <br />
                          <small>초기: {item.initial_quantity.toFixed(4)}</small>
                        </>
                      )}
                    </td>
                    <td>₩{item.current_value.toLocaleString(undefined, { maximumFractionDigits: 0 })}</td>
                    <td className={itemReturn >= 0 ? 'positive' : 'negative'}>
                      {itemReturn >= 0 ? '+' : ''}{itemReturn.toFixed(2)}%
                    </td>
                    <td>
                      {isEditing ? (
                        <div className="edit-actions">
                          <button
                            onClick={() => handleSaveQuantity(item.item_id)}
                            className="btn btn-primary btn-sm"
                          >
                            저장
                          </button>
                          <button
                            onClick={handleCancelEdit}
                            className="btn btn-secondary btn-sm"
                          >
                            취소
                          </button>
                        </div>
                      ) : (
                        <button
                          onClick={() => handleEditQuantity(item)}
                          className="btn btn-secondary btn-sm"
                        >
                          수량 수정
                        </button>
                      )}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>

        {/* 경고 범위 설명 */}
        <div className="legend">
          <h3>경고 표시 안내</h3>
          <div className="legend-items">
            <div className="legend-item">
              <span className="legend-box warning-cell"></span>
              <span>허용 오차 범위 초과 (경고)</span>
            </div>
            <div className="legend-item">
              <span className="legend-box danger-cell"></span>
              <span>허용 오차 범위 크게 초과 (위험)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

