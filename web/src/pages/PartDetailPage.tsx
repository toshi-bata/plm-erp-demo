import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  fetchPart, fetchBom, fetchWhereUsed,
  fetchProductionHistory, fetchCostSummary, fetchRecommendation,
} from '../api'
import type { Part, BomItem, WhereUsedItem, ProductionOrder, CostSummaryEntry, Recommendation } from '../types'
import Spinner, { ErrorMsg } from '../components/Spinner'
import { qualityBadge, statusBadge } from '../components/Badge'

type Tab = 'info' | 'bom' | 'where-used' | 'history' | 'cost' | 'recommendation'

function TabBtn({ active, label, onClick }: { active: boolean; label: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
        active ? 'border-indigo-600 text-indigo-700' : 'border-transparent text-gray-500 hover:text-gray-800 hover:border-gray-300'
      }`}
    >
      {label}
    </button>
  )
}

function fmt(n: number) {
  return n.toLocaleString('en-US', { maximumFractionDigits: 0 })
}

export default function PartDetailPage() {
  const { partId } = useParams<{ partId: string }>()
  const [tab, setTab] = useState<Tab>('info')
  const [part, setPart] = useState<Part | null>(null)
  const [bom, setBom] = useState<BomItem[]>([])
  const [whereUsed, setWhereUsed] = useState<WhereUsedItem[]>([])
  const [orders, setOrders] = useState<ProductionOrder[]>([])
  const [costSummary, setCostSummary] = useState<Record<string, CostSummaryEntry>>({})
  const [recommendation, setRecommendation] = useState<Recommendation | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!partId) return
    setLoading(true)
    setError(null)
    Promise.all([
      fetchPart(partId),
      fetchBom(partId),
      fetchWhereUsed(partId),
      fetchProductionHistory(partId),
      fetchCostSummary(partId),
      fetchRecommendation(partId),
    ])
      .then(([p, b, wu, ph, cs, rec]) => {
        setPart(p)
        setBom(b.bom)
        setWhereUsed(wu.where_used)
        setOrders(ph.orders)
        setCostSummary(cs.cost_summary)
        setRecommendation(Object.keys(rec.recommendation).length > 0 ? rec.recommendation : null)
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false))
  }, [partId])

  if (loading) return <Spinner />
  if (error) return <ErrorMsg message={error} />
  if (!part) return null

  return (
    <div>
      {/* Breadcrumb */}
      <div className="text-sm text-gray-500 mb-4">
        <Link to="/parts" className="hover:underline text-indigo-600">Parts</Link>
        <span className="mx-2">/</span>
        <span>{part.part_name}</span>
      </div>

      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">{part.part_name}</h1>
          <p className="text-gray-500 text-sm mt-1 font-mono">{part.part_id}</p>
        </div>
        {statusBadge(part.status)}
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-gray-200 mb-6">
        {([
          ['info', 'Info'],
          ['bom', `BOM (${bom.length})`],
          ['where-used', `Where Used (${whereUsed.length})`],
          ['history', `Production History (${orders.length})`],
          ['cost', 'Cost Summary'],
          ['recommendation', 'Recommendation'],
        ] as [Tab, string][]).map(([t, label]) => (
          <TabBtn key={t} active={tab === t} label={label} onClick={() => setTab(t)} />
        ))}
      </div>

      {/* Tab: Info */}
      {tab === 'info' && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 grid grid-cols-2 gap-x-12 gap-y-4 text-sm max-w-2xl">
          {[
            ['Part ID', part.part_id],
            ['Part Name', part.part_name],
            ['Revision', part.revision],
            ['Material', part.material],
            ['Weight (kg)', part.weight_kg],
            ['Drawing Number', part.drawing_number],
            ['CAD File', part.cad_file_name],
            ['Created At', part.created_at],
            ['Status', part.status],
          ].map(([label, value]) => (
            <div key={String(label)}>
              <dt className="text-gray-500 text-xs uppercase tracking-wide mb-0.5">{label}</dt>
              <dd className="font-medium">{String(value)}</dd>
            </div>
          ))}
        </div>
      )}

      {/* Tab: BOM */}
      {tab === 'bom' && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          {bom.length === 0 ? (
            <p className="px-4 py-8 text-center text-gray-400">No child components.</p>
          ) : (
            <table className="min-w-full text-sm">
              <thead className="bg-gray-50 text-gray-600 uppercase text-xs tracking-wide">
                <tr>
                  <th className="px-4 py-3 text-left">Child Part ID</th>
                  <th className="px-4 py-3 text-left">Name</th>
                  <th className="px-4 py-3 text-left">CAD File</th>
                  <th className="px-4 py-3 text-right">Qty</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {bom.map((row) => (
                  <tr key={row.child_part_id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 font-mono text-indigo-700">
                      <Link to={`/parts/${row.child_part_id}`} className="hover:underline">{row.child_part_id}</Link>
                    </td>
                    <td className="px-4 py-3">{row.child_part_name}</td>
                    <td className="px-4 py-3 font-mono text-xs text-gray-500">{row.child_cad_file_name}</td>
                    <td className="px-4 py-3 text-right">{row.quantity}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Tab: Where Used */}
      {tab === 'where-used' && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          {whereUsed.length === 0 ? (
            <p className="px-4 py-8 text-center text-gray-400">Not used in any assembly.</p>
          ) : (
            <table className="min-w-full text-sm">
              <thead className="bg-gray-50 text-gray-600 uppercase text-xs tracking-wide">
                <tr>
                  <th className="px-4 py-3 text-left">Parent Part ID</th>
                  <th className="px-4 py-3 text-left">Name</th>
                  <th className="px-4 py-3 text-left">CAD File</th>
                  <th className="px-4 py-3 text-right">Qty</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {whereUsed.map((row) => (
                  <tr key={row.parent_part_id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 font-mono text-indigo-700">
                      <Link to={`/parts/${row.parent_part_id}`} className="hover:underline">{row.parent_part_id}</Link>
                    </td>
                    <td className="px-4 py-3">{row.parent_part_name}</td>
                    <td className="px-4 py-3 font-mono text-xs text-gray-500">{row.parent_cad_file_name}</td>
                    <td className="px-4 py-3 text-right">{row.quantity}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Tab: Production History */}
      {tab === 'history' && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-x-auto">
          {orders.length === 0 ? (
            <p className="px-4 py-8 text-center text-gray-400">No production orders.</p>
          ) : (
            <table className="min-w-full text-sm">
              <thead className="bg-gray-50 text-gray-600 uppercase text-xs tracking-wide">
                <tr>
                  <th className="px-4 py-3 text-left">Order ID</th>
                  <th className="px-4 py-3 text-left">Type</th>
                  <th className="px-4 py-3 text-left">Vendor</th>
                  <th className="px-4 py-3 text-left">Customer</th>
                  <th className="px-4 py-3 text-right">Qty</th>
                  <th className="px-4 py-3 text-right">Unit Cost (¥)</th>
                  <th className="px-4 py-3 text-right">Lead (days)</th>
                  <th className="px-4 py-3 text-left">Delivery</th>
                  <th className="px-4 py-3 text-left">Quality</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {orders.map((o) => (
                  <tr key={o.order_id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 font-mono text-xs">{o.order_id}</td>
                    <td className="px-4 py-3">{o.production_type}</td>
                    <td className="px-4 py-3">
                      {o.vendor_id ? (
                        <Link to={`/vendors/${o.vendor_id}`} className="text-indigo-700 hover:underline">{o.vendor_id}</Link>
                      ) : '—'}
                    </td>
                    <td className="px-4 py-3">
                      <Link to={`/customers/${o.customer_id}`} className="text-indigo-700 hover:underline">
                        {o.customer_name ?? o.customer_id}
                      </Link>
                    </td>
                    <td className="px-4 py-3 text-right">{o.quantity}</td>
                    <td className="px-4 py-3 text-right">{fmt(o.unit_cost_jpy)}</td>
                    <td className="px-4 py-3 text-right">{o.lead_time_days}</td>
                    <td className="px-4 py-3">{o.delivery_date}</td>
                    <td className="px-4 py-3">{qualityBadge(o.quality_result)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Tab: Cost Summary */}
      {tab === 'cost' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(costSummary).map(([type, s]) => (
            <div key={type} className="bg-white rounded-lg border border-gray-200 p-5">
              <h3 className="font-semibold text-gray-700 mb-3 capitalize">{type.replace('_', ' ')}</h3>
              <dl className="space-y-2 text-sm">
                <div className="flex justify-between"><dt className="text-gray-500">Orders</dt><dd className="font-medium">{s.order_count}</dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Avg cost</dt><dd className="font-medium">¥{fmt(s.avg_unit_cost_jpy)}</dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Min cost</dt><dd className="font-medium">¥{fmt(s.min_unit_cost_jpy)}</dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Max cost</dt><dd className="font-medium">¥{fmt(s.max_unit_cost_jpy)}</dd></div>
              </dl>
            </div>
          ))}
          {Object.keys(costSummary).length === 0 && (
            <p className="text-gray-400">No cost data available.</p>
          )}
        </div>
      )}

      {/* Tab: Recommendation */}
      {tab === 'recommendation' && (
        recommendation ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {([
              ['💰 Cheapest', recommendation.cheapest],
              ['⚡ Fastest', recommendation.fastest],
              ['⭐ Best Quality', recommendation.best_quality],
            ] as const).map(([title, rec]) => (
              <div key={title} className="bg-white rounded-lg border border-gray-200 p-5">
                <h3 className="font-semibold text-gray-700 mb-3">{title}</h3>
                <dl className="space-y-2 text-sm">
                  <div className="flex justify-between"><dt className="text-gray-500">Vendor</dt>
                    <dd className="font-medium">
                      {rec.vendor_id ? (
                        <Link to={`/vendors/${rec.vendor_id}`} className="text-indigo-700 hover:underline">{rec.vendor_name}</Link>
                      ) : rec.vendor_name}
                    </dd>
                  </div>
                  <div className="flex justify-between"><dt className="text-gray-500">Type</dt><dd className="font-medium">{rec.production_type}</dd></div>
                  <div className="flex justify-between"><dt className="text-gray-500">Avg cost</dt><dd className="font-medium">¥{fmt(rec.avg_cost_jpy)}</dd></div>
                  <div className="flex justify-between"><dt className="text-gray-500">Avg lead</dt><dd className="font-medium">{rec.avg_lead_days} days</dd></div>
                  <div className="flex justify-between"><dt className="text-gray-500">Pass rate</dt><dd className="font-medium">{(rec.pass_rate * 100).toFixed(1)}%</dd></div>
                  <div className="flex justify-between"><dt className="text-gray-500">Samples</dt><dd className="font-medium">{rec.sample_count}</dd></div>
                </dl>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400">No recommendation data available.</p>
        )
      )}
    </div>
  )
}
