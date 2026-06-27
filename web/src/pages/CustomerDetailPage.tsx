import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { fetchCustomer, fetchCustomerProductionHistory } from '../api'
import type { Customer, ProductionOrder } from '../types'
import Spinner, { ErrorMsg } from '../components/Spinner'
import { qualityBadge } from '../components/Badge'

type Tab = 'info' | 'history'

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

export default function CustomerDetailPage() {
  const { customerId } = useParams<{ customerId: string }>()
  const [tab, setTab] = useState<Tab>('info')
  const [customer, setCustomer] = useState<Customer | null>(null)
  const [orders, setOrders] = useState<ProductionOrder[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!customerId) return
    setLoading(true)
    setError(null)
    Promise.all([
      fetchCustomer(customerId),
      fetchCustomerProductionHistory(customerId),
    ])
      .then(([c, ph]) => {
        setCustomer(c)
        setOrders(ph.orders)
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false))
  }, [customerId])

  if (loading) return <Spinner />
  if (error) return <ErrorMsg message={error} />
  if (!customer) return null

  return (
    <div>
      {/* Breadcrumb */}
      <div className="text-sm text-gray-500 mb-4">
        <Link to="/customers" className="hover:underline text-indigo-600">Customers</Link>
        <span className="mx-2">/</span>
        <span>{customer.company_name}</span>
      </div>

      <div className="mb-6">
        <h1 className="text-2xl font-bold">{customer.company_name}</h1>
        <p className="text-gray-500 text-sm mt-1 font-mono">{customer.customer_id}</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-gray-200 mb-6">
        <TabBtn active={tab === 'info'} label="Info" onClick={() => setTab('info')} />
        <TabBtn active={tab === 'history'} label={`Production History (${orders.length})`} onClick={() => setTab('history')} />
      </div>

      {/* Tab: Info */}
      {tab === 'info' && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 grid grid-cols-2 gap-x-12 gap-y-4 text-sm max-w-xl">
          {[
            ['Customer ID', customer.customer_id],
            ['Company Name', customer.company_name],
            ['Contact', customer.contact_name],
            ['Address 1', customer.address1],
            ['Address 2', customer.address2],
            ['Email', customer.email],
            ['Phone', customer.phone],
          ].map(([label, value]) => (
            <div key={String(label)}>
              <dt className="text-gray-500 text-xs uppercase tracking-wide mb-0.5">{label}</dt>
              <dd className="font-medium">{String(value)}</dd>
            </div>
          ))}
        </div>
      )}

      {/* Tab: Production History */}
      {tab === 'history' && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-x-auto">
          {orders.length === 0 ? (
            <p className="px-4 py-8 text-center text-gray-400">No production orders for this customer.</p>
          ) : (
            <table className="min-w-full text-sm">
              <thead className="bg-gray-50 text-gray-600 uppercase text-xs tracking-wide">
                <tr>
                  <th className="px-4 py-3 text-left">Order ID</th>
                  <th className="px-4 py-3 text-left">Part</th>
                  <th className="px-4 py-3 text-left">Type</th>
                  <th className="px-4 py-3 text-left">Vendor</th>
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
                    <td className="px-4 py-3 text-indigo-700">
                      <Link to={`/parts/${o.part_id}`} className="hover:underline">{o.part_id}</Link>
                    </td>
                    <td className="px-4 py-3">{o.production_type}</td>
                    <td className="px-4 py-3">
                      {o.vendor_id ? (
                        <Link to={`/vendors/${o.vendor_id}`} className="text-indigo-700 hover:underline">{o.vendor_id}</Link>
                      ) : '—'}
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
    </div>
  )
}
