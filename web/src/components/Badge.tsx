type Variant = 'green' | 'red' | 'yellow' | 'blue' | 'gray'

const styles: Record<Variant, string> = {
  green: 'bg-green-100 text-green-800',
  red: 'bg-red-100 text-red-800',
  yellow: 'bg-yellow-100 text-yellow-800',
  blue: 'bg-blue-100 text-blue-800',
  gray: 'bg-gray-100 text-gray-700',
}

export default function Badge({ label, variant }: { label: string; variant: Variant }) {
  return (
    <span className={`inline-block text-xs font-medium px-2 py-0.5 rounded-full ${styles[variant]}`}>
      {label}
    </span>
  )
}

export function qualityBadge(result: string) {
  const map: Record<string, Variant> = { pass: 'green', conditional: 'yellow', fail: 'red' }
  return <Badge label={result} variant={map[result] ?? 'gray'} />
}

export function statusBadge(status: string) {
  return <Badge label={status} variant={status === 'active' ? 'green' : 'gray'} />
}
