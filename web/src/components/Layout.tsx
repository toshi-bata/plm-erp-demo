import { Link, useLocation } from 'react-router-dom'

export default function Layout({ children }: { children: React.ReactNode }) {
  const { pathname } = useLocation()
  const nav = [
    { to: '/parts', label: 'Parts' },
    { to: '/vendors', label: 'Vendors' },
    { to: '/customers', label: 'Customers' },
  ]
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center gap-8">
        <span className="font-bold text-lg tracking-tight text-indigo-700">PLM/ERP Browser</span>
        <nav className="flex gap-4">
          {nav.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              className={`text-sm font-medium px-3 py-1.5 rounded transition-colors ${
                pathname.startsWith(to)
                  ? 'bg-indigo-50 text-indigo-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              {label}
            </Link>
          ))}
        </nav>
      </header>
      <main className="max-w-7xl mx-auto px-6 py-8">{children}</main>
    </div>
  )
}
