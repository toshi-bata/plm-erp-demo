import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchVendors } from '../api'
import type { Vendor } from '../types'
import Spinner, { ErrorMsg } from '../components/Spinner'

function Stars({ rating }: { rating: number }) {
  return (
    <span className="text-yellow-500 text-xs">
      {'★'.repeat(Math.round(rating))}{'☆'.repeat(5 - Math.round(rating))}
      <span className="text-gray-500 ml-1">{rating.toFixed(1)}</span>
    </span>
  )
}

export default function VendorsPage() {
  const [vendors, setVendors] = useState<Vendor[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchVendors()
      .then((res) => setVendors(res.items))
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <Spinner />
  if (error) return <ErrorMsg message={error} />

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Vendors</h1>
      <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50 text-gray-600 uppercase text-xs tracking-wide">
            <tr>
              <th className="px-4 py-3 text-left">Vendor ID</th>
              <th className="px-4 py-3 text-left">Name</th>
              <th className="px-4 py-3 text-left">Specialty</th>
              <th className="px-4 py-3 text-left">Country</th>
              <th className="px-4 py-3 text-left">Rating</th>
              <th className="px-4 py-3 text-right">Typical Lead (days)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {vendors.map((v) => (
              <tr key={v.vendor_id} className="hover:bg-gray-50 transition-colors">
                <td className="px-4 py-3 font-mono text-indigo-700">
                  <Link to={`/vendors/${v.vendor_id}`} className="hover:underline">{v.vendor_id}</Link>
                </td>
                <td className="px-4 py-3 font-medium">
                  <Link to={`/vendors/${v.vendor_id}`} className="hover:underline">{v.vendor_name}</Link>
                </td>
                <td className="px-4 py-3">{v.specialty}</td>
                <td className="px-4 py-3">{v.country}</td>
                <td className="px-4 py-3"><Stars rating={v.rating} /></td>
                <td className="px-4 py-3 text-right">{v.typical_lead_time_days}</td>
              </tr>
            ))}
            {vendors.length === 0 && (
              <tr><td colSpan={6} className="px-4 py-8 text-center text-gray-400">No vendors found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
