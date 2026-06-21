import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchParts } from '../api'
import type { Part } from '../types'
import Spinner, { ErrorMsg } from '../components/Spinner'
import { statusBadge } from '../components/Badge'

const PAGE_SIZE = 20

const MATERIALS = ['S45C', 'SUS304', 'A5052', 'FC250']

export default function PartsPage() {
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('')
  const [material, setMaterial] = useState('')
  const [skip, setSkip] = useState(0)
  const [parts, setParts] = useState<Part[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError(null)
    fetchParts({ search: search || undefined, status: status || undefined, material: material || undefined, skip, limit: PAGE_SIZE })
      .then((res) => {
        if (cancelled) return
        setParts(res.items)
        setTotal(res.total)
      })
      .catch((e: Error) => {
        if (!cancelled) setError(e.message)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => { cancelled = true }
  }, [search, status, material, skip])

  const totalPages = Math.ceil(total / PAGE_SIZE)
  const currentPage = Math.floor(skip / PAGE_SIZE) + 1

  const handleFilter = () => setSkip(0)

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Parts</h1>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <input
          type="text"
          placeholder="Search name or drawing no."
          value={search}
          onChange={(e) => { setSearch(e.target.value); handleFilter() }}
          className="border border-gray-300 rounded px-3 py-1.5 text-sm w-64 focus:outline-none focus:ring-2 focus:ring-indigo-300"
        />
        <select
          value={status}
          onChange={(e) => { setStatus(e.target.value); handleFilter() }}
          className="border border-gray-300 rounded px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
        >
          <option value="">All statuses</option>
          <option value="active">Active</option>
          <option value="obsolete">Obsolete</option>
        </select>
        <select
          value={material}
          onChange={(e) => { setMaterial(e.target.value); handleFilter() }}
          className="border border-gray-300 rounded px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
        >
          <option value="">All materials</option>
          {MATERIALS.map((m) => <option key={m} value={m}>{m}</option>)}
        </select>
        <span className="text-sm text-gray-500 self-center">{total} result{total !== 1 ? 's' : ''}</span>
      </div>

      {error && <ErrorMsg message={error} />}
      {loading ? <Spinner /> : (
        <>
          <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
            <table className="min-w-full text-sm">
              <thead className="bg-gray-50 text-gray-600 uppercase text-xs tracking-wide">
                <tr>
                  <th className="px-4 py-3 text-left">Part ID</th>
                  <th className="px-4 py-3 text-left">Name</th>
                  <th className="px-4 py-3 text-left">Rev</th>
                  <th className="px-4 py-3 text-left">Material</th>
                  <th className="px-4 py-3 text-left">Drawing No.</th>
                  <th className="px-4 py-3 text-left">CAD File</th>
                  <th className="px-4 py-3 text-left">Weight (kg)</th>
                  <th className="px-4 py-3 text-left">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {parts.map((p) => (
                  <tr key={p.part_id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-4 py-3 font-mono text-indigo-700">
                      <Link to={`/parts/${p.part_id}`} className="hover:underline">{p.part_id}</Link>
                    </td>
                    <td className="px-4 py-3 font-medium">
                      <Link to={`/parts/${p.part_id}`} className="hover:underline">{p.part_name}</Link>
                    </td>
                    <td className="px-4 py-3 text-gray-600">{p.revision}</td>
                    <td className="px-4 py-3">{p.material}</td>
                    <td className="px-4 py-3 font-mono text-xs">{p.drawing_number}</td>
                    <td className="px-4 py-3 font-mono text-xs text-gray-500">{p.cad_file_name}</td>
                    <td className="px-4 py-3 text-right">{p.weight_kg}</td>
                    <td className="px-4 py-3">{statusBadge(p.status)}</td>
                  </tr>
                ))}
                {parts.length === 0 && (
                  <tr><td colSpan={8} className="px-4 py-8 text-center text-gray-400">No parts found.</td></tr>
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center gap-2 mt-4 text-sm">
              <button
                onClick={() => setSkip(Math.max(0, skip - PAGE_SIZE))}
                disabled={skip === 0}
                className="px-3 py-1 rounded border border-gray-300 disabled:opacity-40 hover:bg-gray-100"
              >
                ← Prev
              </button>
              <span className="text-gray-600">Page {currentPage} / {totalPages}</span>
              <button
                onClick={() => setSkip(skip + PAGE_SIZE)}
                disabled={currentPage >= totalPages}
                className="px-3 py-1 rounded border border-gray-300 disabled:opacity-40 hover:bg-gray-100"
              >
                Next →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
