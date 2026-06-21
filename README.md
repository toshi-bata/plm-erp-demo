# PLM/ERP Manufacturing Demo

A self-contained PLM + ERP data service that lets **Claude** look up manufacturing records
using CAD file names supplied by an external HOOPS AI MCP server.
It provides a FastAPI REST API (port 8010) and an MCP server (port 8011) backed by a
seeded SQLite database containing 20 sample parts, 6 vendors, and ~80 production orders
representing a realistic discrete-manufacturing environment (turned parts, sheet metal, castings).

---

## Setup

### 1. Install dependencies

```bash
cd plm-erp-demo
pip install -r requirements.txt
```

### 2. Create and seed the database

```bash
python init_db.py
```

This creates `plm_erp.db` in the project root and populates all tables.

### 3. Start the FastAPI server (port 8010)

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8010 --reload
```

Interactive docs: http://localhost:8010/docs

### 4. Start the MCP server (port 8011)

```bash
python mcp_server.py
```

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/plm/parts/{part_id}` | Fetch part by ID |
| GET | `/plm/parts/by-cad-file/{cad_file_name}` | Fetch part by CAD filename |
| GET | `/plm/parts/{part_id}/bom` | Bill of Materials |
| GET | `/erp/parts/{part_id}/production-history` | All production orders |
| GET | `/erp/parts/{part_id}/cost-summary` | Avg/min/max cost by production type |
| GET | `/erp/parts/{part_id}/recommendation` | Cheapest / fastest / best-quality option |
| GET | `/erp/vendors/{vendor_id}` | Vendor details |
| POST | `/query/by-cad-files` | **Bulk lookup** — primary endpoint for Claude |

### Bulk query example

```bash
curl -X POST http://localhost:8010/query/by-cad-files \
  -H "Content-Type: application/json" \
  -d '{"cad_file_names": ["shaft_001.stp", "flange_003.stp", "housing_001.stp"]}'
```

---

## MCP Tools (port 8011)

| Tool | Description |
|------|-------------|
| `get_part_by_cad_file(cad_file_name)` | Look up a single part |
| `get_production_history(part_id)` | Full order history |
| `get_cost_summary(part_id)` | Cost stats by production type |
| `get_recommendation(part_id)` | Cheapest / fastest / best-quality |
| `query_by_cad_files(cad_file_names)` | **Main tool** — bulk lookup |

---

## How Claude Uses This Alongside HOOPS AI MCP

1. **HOOPS AI MCP** analyzes a set of CAD files and returns a ranked list of file names
   (e.g. `["shaft_001.stp", "housing_001.stp", "bracket_002.stp"]`).
2. Claude calls **`query_by_cad_files`** on this MCP server (port 8011) with that list.
3. The server returns structured PLM/ERP data: part metadata, full production history,
   cost breakdown by production type, and a sourcing recommendation.
4. Claude reasons over the combined HOOPS AI geometry insights and ERP cost/quality data
   to answer questions like:
   - *"Which parts are cheapest to outsource vs. make in-house?"*
   - *"Has this casting had any quality failures in the past three years?"*
   - *"What is the fastest sourcing option for this shaft assembly?"*

No HOOPS AI integration code lives in this repository — it is a pure data service.

---

## Database Overview

| Table | Rows (seed) |
|-------|-------------|
| `parts` | 20 |
| `part_structures` | 9 (BOM links) |
| `vendors` | 6 |
| `production_orders` | ~80 |
| `purchase_items` | 6 |

Materials used: `S45C`, `SUS304`, `A5052`, `FC250`  
Production types: `in_house`, `outsource`, `purchase`  
Quality results: `pass`, `conditional`, `fail`
