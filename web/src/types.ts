export interface Part {
  part_id: string
  part_name: string
  revision: string
  material: string
  weight_kg: number
  drawing_number: string
  cad_file_name: string
  created_at: string
  status: 'active' | 'obsolete'
}

export interface PartsListResponse {
  total: number
  skip: number
  limit: number
  items: Part[]
}

export interface BomItem {
  child_part_id: string
  child_part_name: string | null
  child_cad_file_name: string | null
  quantity: number
}

export interface WhereUsedItem {
  parent_part_id: string
  parent_part_name: string | null
  parent_cad_file_name: string | null
  quantity: number
}

export interface ProductionOrder {
  order_id: string
  part_id: string
  production_type: 'in_house' | 'outsource' | 'purchase'
  vendor_id: string | null
  customer_id: string
  customer_name: string | null
  quantity: number
  unit_cost_jpy: number
  lead_time_days: number
  delivery_date: string
  quality_result: 'pass' | 'conditional' | 'fail'
  notes: string | null
}

export interface Customer {
  customer_id: string
  company_name: string
  contact_name: string
  address1: string
  address2: string
  email: string
  phone: string
}

export interface CostSummaryEntry {
  avg_unit_cost_jpy: number
  min_unit_cost_jpy: number
  max_unit_cost_jpy: number
  order_count: number
}

export interface RecommendationEntry {
  vendor_id: string | null
  vendor_name: string
  production_type: string
  avg_cost_jpy: number
  avg_lead_days: number
  pass_rate: number
  sample_count: number
}

export interface Recommendation {
  cheapest: RecommendationEntry
  fastest: RecommendationEntry
  best_quality: RecommendationEntry
}

export interface Vendor {
  vendor_id: string
  vendor_name: string
  specialty: string
  country: string
  rating: number
  typical_lead_time_days: number
}

export interface PurchaseItem {
  item_id: string
  part_id: string
  vendor_id: string
  catalog_price_jpy: number
  min_order_qty: number
  lead_time_days: number
}
