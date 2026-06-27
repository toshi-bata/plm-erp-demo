import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchCustomers } from '../api'
import type { Customer } from '../types'
import Spinner, { ErrorMsg } from '../components/Spinner'

export default function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchCustomers()
      .then((res) => setCustomers(res.items))
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <Spinner />
  if (error) return <ErrorMsg message={error} />

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Customers</h1>
      <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50 text-gray-600 uppercase text-xs tracking-wide">
            <tr>
              <th className="px-4 py-3 text-left">Customer ID</th>
              <th className="px-4 py-3 text-left">Company Name</th>
              <th className="px-4 py-3 text-left">Contact</th>
              <th className="px-4 py-3 text-left">Address</th>
              <th className="px-4 py-3 text-left">Email</th>
              <th className="px-4 py-3 text-left">Phone</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {customers.map((c) => (
              <tr key={c.customer_id} className="hover:bg-gray-50 transition-colors">
                <td className="px-4 py-3 font-mono text-indigo-700">
                  <Link to={`/customers/${c.customer_id}`} className="hover:underline">{c.customer_id}</Link>
                </td>
                <td className="px-4 py-3 font-medium">
                  <Link to={`/customers/${c.customer_id}`} className="hover:underline">{c.company_name}</Link>
                </td>
                <td className="px-4 py-3">{c.contact_name}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{c.address2}</td>
                <td className="px-4 py-3 text-xs">{c.email}</td>
                <td className="px-4 py-3 text-xs">{c.phone}</td>
              </tr>
            ))}
            {customers.length === 0 && (
              <tr><td colSpan={6} className="px-4 py-8 text-center text-gray-400">No customers found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
