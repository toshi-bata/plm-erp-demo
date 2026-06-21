import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { fetchVendor, fetchVendorProductionHistory, fetchVendorPurchaseItems } from '../api'
import type { Vendor, ProductionOrder, PurchaseItem } from '../types'
import Spinner, { ErrorMsg } from '../components/Spinner'
import { qualityBadge } from '../components/Badge'

type Tab = 'info' | 'history' | 'purchase'

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

export default function VendorDetailPage() {
  const { vendorId } = useParams<{ vendorId: string }>()
  const [tab, setTab] = useState<Tab>('info')
  const [vendor, setVendor] = useState<Vendor | null>(null)
  const [orders, setOrders] = useState<ProductionOrder[]>([])
  const [purchaseItems, setPurchaseItems] = useState<PurchaseItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!vendorId) return
    setLoading(true)
    setError(null)
    Promise.all([
      fetchVendor(vendorId),
      fetchVendorProductionHistory(vendorId),
      fetchVendorPurchaseItems(vendorId),
    ])
      .then(([v, ph, pi]) => {
        setVendor(v)
        setOrders(ph.orders)
        setPurchaseItems(pi.items)
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false))
  }, [vendorId])

  if (loading) return <Spinner />
  if (error) return <ErrorMsg message={error} />
  if (!vendor) return null

  return (
    <div>
      {/* Breadcrumb */}
      <div className="text-sm text-gray-500 mb-4">
        <Link to="/vendors" className="hover:underline text-indigo-600">Vendors</Link>
        <span className="mx-2">/</span>
        <span>{vendor.vendor_name}</span>
      </div>

      <div className="mb-6">
        <h1 className="text-2xl font-bold">{vendor.vendor_name}</h1>
        <p className="text-gray-500 text-sm mt-1 font-mono">{vendor.vendor_id}</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-gray-200 mb-6">
        <TabBtn active={tab === 'info'} label="Info" onClick={() => setTab('info')} />
        <TabBtn active={tab === 'history'} label={`Production History (${orders.length})`} onClick={() => setTab('history')} />
        <TabBtn active={tab === 'purchase'} label={`Purchase Items (${purchaseItems.length})`} onClick={() => setTab('purchase')} />
      </div>

      {/* Tab: Info */}
      {tab === 'info' && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 grid grid-cols-2 gap-x-12 gap-y-4 text-sm max-w-xl">
          {[
            ['Vendor ID', vendor.vendor_id],
            ['Name', vendor.vendor_name],
            ['Specialty', vendor.specialty],
            ['Country', vendor.country],
            ['Rating', `${vendor.rating} / 5`],
            ['Typical Lead Time', `${vendor.typical_lead_time_days} days`],
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
            <p className="px-4 py-8 text-center text-gray-400">No production orders for this vendor.</p>
          ) : (
            <table className="min-w-full text-sm">
              <thead className="bg-gray-50 text-gray-600 uppercase text-xs tracking-wide">
                <tr>
                  <th className="px-4 py-3 text-left">Order ID</th>
                  <th className="px-4 py-3 text-left">Part</th>
                  <th className="px-4 py-3 text-left">Type</th>
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

      {/* Tab: Purchase Items */}
      {tab === 'purchase' && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-x-auto">
          {purchaseItems.length === 0 ? (
            <p className="px-4 py-8 text-center text-gray-400">No purchase items for this vendor.</p>
          ) : (
            <table className="min-w-full text-sm">
              <thead className="bg-gray-50 text-gray-600 uppercase text-xs tracking-wide">
                <tr>
                  <th className="px-4 py-3 text-left">Item ID</th>
                  <th className="px-4 py-3 text-left">Part</th>
                  <th className="px-4 py-3 text-right">Catalog Price (¥)</th>
                  <th className="px-4 py-3 text-right">Min Order Qty</th>
                  <th className="px-4 py-3 text-right">Lead Time (days)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {purchaseItems.map((item) => (
                  <tr key={item.item_id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 font-mono text-xs">{item.item_id}</td>
                    <td className="px-4 py-3 text-indigo-700">
                      <Link to={`/parts/${item.part_id}`} className="hover:underline">{item.part_id}</Link>
                    </td>
                    <td className="px-4 py-3 text-right">{fmt(item.catalog_price_jpy)}</td>
                    <td className="px-4 py-3 text-right">{item.min_order_qty}</td>
                    <td className="px-4 py-3 text-right">{item.lead_time_days}</td>
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
