import type {
  PartsListResponse,
  Part,
  BomItem,
  WhereUsedItem,
  ProductionOrder,
  CostSummaryEntry,
  Recommendation,
  Vendor,
  PurchaseItem,
} from './types'

const BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8010'

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} — ${path}`)
  return res.json() as Promise<T>
}

// Parts
export const fetchParts = (params: {
  search?: string
  status?: string
  material?: string
  skip?: number
  limit?: number
}) => {
  const q = new URLSearchParams()
  if (params.search) q.set('search', params.search)
  if (params.status) q.set('status', params.status)
  if (params.material) q.set('material', params.material)
  if (params.skip != null) q.set('skip', String(params.skip))
  if (params.limit != null) q.set('limit', String(params.limit))
  return get<PartsListResponse>(`/plm/parts?${q}`)
}

export const fetchPart = (partId: string) =>
  get<Part>(`/plm/parts/${partId}`)

export const fetchBom = (partId: string) =>
  get<{ part_id: string; bom: BomItem[] }>(`/plm/parts/${partId}/bom`)

export const fetchWhereUsed = (partId: string) =>
  get<{ part_id: string; where_used: WhereUsedItem[] }>(`/plm/parts/${partId}/where-used`)

export const fetchProductionHistory = (partId: string) =>
  get<{ part_id: string; orders: ProductionOrder[] }>(`/erp/parts/${partId}/production-history`)

export const fetchCostSummary = (partId: string) =>
  get<{ part_id: string; cost_summary: Record<string, CostSummaryEntry> }>(`/erp/parts/${partId}/cost-summary`)

export const fetchRecommendation = (partId: string) =>
  get<{ part_id: string; recommendation: Recommendation }>(`/erp/parts/${partId}/recommendation`)

// Vendors
export const fetchVendors = () =>
  get<{ items: Vendor[] }>('/erp/vendors')

export const fetchVendor = (vendorId: string) =>
  get<Vendor>(`/erp/vendors/${vendorId}`)

export const fetchVendorProductionHistory = (vendorId: string) =>
  get<{ vendor_id: string; orders: ProductionOrder[] }>(`/erp/vendors/${vendorId}/production-history`)

export const fetchVendorPurchaseItems = (vendorId: string) =>
  get<{ vendor_id: string; items: PurchaseItem[] }>(`/erp/vendors/${vendorId}/purchase-items`)
