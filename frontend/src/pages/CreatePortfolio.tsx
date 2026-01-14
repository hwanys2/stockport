import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { assetAPI, portfolioAPI } from '../services/api'
import './CreatePortfolio.css'

interface AssetSearchResult {
  symbol: string
  name: string
  exchange?: string
  current_price?: number
}

interface SelectedAsset {
  asset_id?: number
  symbol: string
  name: string
  target_weight: number
  tolerance: number
}

export default function CreatePortfolio() {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [initialInvestAmount, setInitialInvestAmount] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<AssetSearchResult[]>([])
  const [selectedAssets, setSelectedAssets] = useState<SelectedAsset[]>([])
  const [searching, setSearching] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const navigate = useNavigate()

  const handleSearch = async () => {
    if (!searchQuery.trim()) return

    console.log('검색 시작:', searchQuery)
    setSearching(true)
    try {
      const response = await assetAPI.search(searchQuery)
      console.log('검색 결과:', response.data)
      setSearchResults(response.data)
      if (response.data.length === 0) {
        alert('검색 결과가 없습니다. 다른 종목명이나 티커를 시도해보세요.')
      }
    } catch (err: any) {
      console.error('검색 오류:', err)
      alert(`종목 검색에 실패했습니다: ${err.response?.data?.detail || err.message}`)
    } finally {
      setSearching(false)
    }
  }

  const handleAddAsset = async (asset: AssetSearchResult) => {
    // 종목을 DB에 추가
    try {
      const response = await assetAPI.create({
        symbol: asset.symbol,
        name: asset.name,
        exchange: asset.exchange,
        currency: 'USD',
        asset_type: 'stock'
      })

      const newAsset: SelectedAsset = {
        asset_id: response.data.id,
        symbol: asset.symbol,
        name: asset.name,
        target_weight: 0,
        tolerance: 5
      }

      setSelectedAssets([...selectedAssets, newAsset])
      setSearchResults([])
      setSearchQuery('')
    } catch (err) {
      alert('종목 추가에 실패했습니다.')
    }
  }

  const handleRemoveAsset = (index: number) => {
    setSelectedAssets(selectedAssets.filter((_, i) => i !== index))
  }

  const handleWeightChange = (index: number, value: string) => {
    const newAssets = [...selectedAssets]
    newAssets[index].target_weight = parseFloat(value) || 0
    setSelectedAssets(newAssets)
  }

  const handleToleranceChange = (index: number, value: string) => {
    const newAssets = [...selectedAssets]
    newAssets[index].tolerance = parseFloat(value) || 0
    setSelectedAssets(newAssets)
  }

  const getTotalWeight = () => {
    return selectedAssets.reduce((sum, asset) => sum + asset.target_weight, 0)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    console.log('포트폴리오 생성 시도')
    setError('')

    // 검증
    if (selectedAssets.length === 0) {
      setError('최소 1개 이상의 종목을 추가해주세요.')
      alert('최소 1개 이상의 종목을 추가해주세요.')
      return
    }

    const totalWeight = getTotalWeight()
    if (Math.abs(totalWeight - 100) > 0.01) {
      const errorMsg = `목표 비중의 합이 100%가 되어야 합니다. (현재: ${totalWeight.toFixed(2)}%)`
      setError(errorMsg)
      alert(errorMsg)
      return
    }

    setLoading(true)

    try {
      const portfolioData = {
        name,
        description: description || null,
        initial_invest_amount: parseFloat(initialInvestAmount),
        items: selectedAssets.map(asset => ({
          asset_id: asset.asset_id!,
          target_weight: asset.target_weight,
          tolerance: asset.tolerance
        }))
      }

      console.log('포트폴리오 데이터:', portfolioData)
      const response = await portfolioAPI.create(portfolioData)
      console.log('생성 완료:', response.data)
      alert('포트폴리오가 생성되었습니다!')
      navigate(`/portfolio/${response.data.id}`)
    } catch (err: any) {
      console.error('생성 오류:', err)
      const errorMsg = err.response?.data?.detail || '포트폴리오 생성에 실패했습니다.'
      setError(errorMsg)
      alert(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  const totalWeight = getTotalWeight()
  const isValidWeight = Math.abs(totalWeight - 100) < 0.01

  return (
    <div className="create-portfolio">
      <h1>새 포트폴리오 만들기</h1>

      <form onSubmit={handleSubmit}>
        {/* 기본 정보 */}
        <div className="card">
          <h2>기본 정보</h2>
          
          <div className="form-group">
            <label className="label">포트폴리오 이름 *</label>
            <input
              type="text"
              className="input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              placeholder="예: 장기 투자 포트폴리오"
            />
          </div>

          <div className="form-group">
            <label className="label">설명</label>
            <textarea
              className="input"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="포트폴리오에 대한 간단한 설명 (선택)"
              rows={3}
            />
          </div>

          <div className="form-group">
            <label className="label">초기 투자금액 (₩) *</label>
            <input
              type="number"
              className="input"
              value={initialInvestAmount}
              onChange={(e) => setInitialInvestAmount(e.target.value)}
              required
              min="0"
              step="1000"
              placeholder="10000000"
            />
          </div>
        </div>

        {/* 종목 선택 */}
        <div className="card">
          <h2>종목 선택</h2>
          
          <div className="search-box">
            <input
              type="text"
              className="input"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleSearch())}
              placeholder="종목명 또는 티커 검색 (예: AAPL, 삼성전자)"
            />
            <button 
              type="button"
              onClick={handleSearch}
              className="btn btn-secondary"
              disabled={searching}
            >
              {searching ? '검색 중...' : '검색'}
            </button>
          </div>

          {searchResults.length > 0 && (
            <div className="search-results">
              <h3>검색 결과</h3>
              {searchResults.map((asset, index) => (
                <div key={index} className="search-result-item">
                  <div>
                    <strong>{asset.symbol}</strong> - {asset.name}
                    {asset.exchange && <span className="exchange"> ({asset.exchange})</span>}
                    {asset.current_price && <span className="price"> - ${asset.current_price}</span>}
                  </div>
                  <button
                    type="button"
                    onClick={() => handleAddAsset(asset)}
                    className="btn btn-primary btn-sm"
                  >
                    추가
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 선택된 종목 및 비중 설정 */}
        {selectedAssets.length > 0 && (
          <div className="card">
            <h2>목표 비중 설정</h2>
            <p className="hint">각 종목의 목표 비중과 허용 오차폭을 설정해주세요.</p>

            <table className="assets-table">
              <thead>
                <tr>
                  <th>종목</th>
                  <th>목표 비중 (%)</th>
                  <th>허용 오차폭 (%)</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {selectedAssets.map((asset, index) => (
                  <tr key={index}>
                    <td>
                      <strong>{asset.symbol}</strong>
                      <br />
                      <small>{asset.name}</small>
                    </td>
                    <td>
                      <input
                        type="number"
                        className="input input-sm"
                        value={asset.target_weight || ''}
                        onChange={(e) => handleWeightChange(index, e.target.value)}
                        min="0"
                        max="100"
                        step="0.1"
                        placeholder="0.0"
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        className="input input-sm"
                        value={asset.tolerance || ''}
                        onChange={(e) => handleToleranceChange(index, e.target.value)}
                        min="0"
                        max="50"
                        step="0.1"
                        placeholder="5.0"
                      />
                    </td>
                    <td>
                      <button
                        type="button"
                        onClick={() => handleRemoveAsset(index)}
                        className="btn btn-danger btn-sm"
                      >
                        제거
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr>
                  <td><strong>합계</strong></td>
                  <td>
                    <strong className={isValidWeight ? 'success-cell' : 'danger-cell'}>
                      {totalWeight.toFixed(2)}%
                    </strong>
                  </td>
                  <td colSpan={2}>
                    {!isValidWeight && (
                      <span className="error">합계가 100%가 되어야 합니다</span>
                    )}
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        )}

        {error && <div className="error">{error}</div>}

        <div className="form-actions">
          <button
            type="button"
            onClick={() => navigate('/dashboard')}
            className="btn btn-secondary"
          >
            취소
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !isValidWeight || selectedAssets.length === 0}
          >
            {loading ? '생성 중...' : '포트폴리오 생성'}
          </button>
        </div>
      </form>
    </div>
  )
}

