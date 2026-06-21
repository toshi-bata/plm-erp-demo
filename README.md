# PLM/ERP Manufacturing Demo

A self-contained PLM + ERP data service that lets **Claude** look up manufacturing records
using CAD file names supplied by an external HOOPS AI MCP server.
It provides a FastAPI REST API (port 8010), an MCP server, and a **React web browser UI** (port 5173)
backed by a seeded SQLite database containing 20 sample parts, 6 vendors, and ~80 production orders
representing a realistic discrete-manufacturing environment (turned parts, sheet metal, castings).

---

## Setup

### 0. Install uv (first time only)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then **restart your terminal** to make the `uv` command available.

### 1. Install dependencies (backend)

```bash
cd plm-erp-demo
uv sync
```

### 2. Create and seed the database

```bash
uv run python -m db.init_db
```

This creates `plm_erp.db` in the project root and populates all tables.

### 3. Start the FastAPI server (port 8010)

```bash
uv run uvicorn api.main:app --host 0.0.0.0 --port 8010 --reload
```

Interactive docs: http://localhost:8010/docs

### 4. Start the Web Browser UI (port 5173)

```bash
cd web
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

The UI connects to the FastAPI backend at `http://localhost:8010` by default.
To change the URL, edit `web/.env`:

```
VITE_API_BASE_URL=http://localhost:8010
```

### 5. Register the MCP server with Claude Desktop

Claude Desktop manages the MCP server process automatically via stdio  E**no manual server startup required.**

In Claude Desktop, go to **Settings ↁEDeveloper ↁEEdit Config** to open the config file.

Add the following entry (adjust the directory path as needed):

```json
{
  "mcpServers": {
    "plm-erp-demo": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "D:\\git\\plm-erp-demo",
        "mcp_server/server.py"
      ]
    }
  }
}
```

> **Windows の注意事頁E*  
> Claude Desktop はシスチE��の `PATH` を継承しなぁE��め、`uv` が見つからずエラーになることがあります、E 
> そ�E場合�E `command` に `uv` のフルパスを指定してください、E 
> `uv` のパスは PowerShell で `where.exe uv` を実行すると確認できます（侁E `C:\Users\username\.local\bin\uv.exe`�E�、E
>
> ```json
> {
>   "mcpServers": {
>     "plm-erp-demo": {
>       "command": "C:\\Users\\username\\.local\\bin\\uv.exe",
>       "args": [
>         "run",
>         "--directory",
>         "D:\\git\\plm-erp-demo",
>         "mcp_server/server.py"
>       ]
>     }
>   }
> }
> ```

Restart Claude Desktop. The MCP server will appear under **Settings ↁEDeveloper**.

#### HTTP mode (optional)

To run the MCP server manually as an HTTP server on port 8011:

```bash
uv run mcp_server/server.py --http
```

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/plm/parts` | List parts (filters: `search`, `status`, `material`, `skip`, `limit`) |
| GET | `/plm/parts/{part_id}` | Fetch part by ID |
| GET | `/plm/parts/by-cad-file/{cad_file_name}` | Fetch part by CAD filename |
| GET | `/plm/parts/{part_id}/bom` | Bill of Materials (child components) |
| GET | `/plm/parts/{part_id}/where-used` | Reverse BOM (parent assemblies) |
| GET | `/erp/vendors` | List all vendors |
| GET | `/erp/vendors/{vendor_id}` | Vendor details |
| GET | `/erp/vendors/{vendor_id}/production-history` | Orders handled by vendor |
| GET | `/erp/vendors/{vendor_id}/purchase-items` | Purchase catalog items for vendor |
| GET | `/erp/parts/{part_id}/production-history` | All production orders for a part |
| GET | `/erp/parts/{part_id}/cost-summary` | Avg/min/max cost by production type |
| GET | `/erp/parts/{part_id}/recommendation` | Cheapest / fastest / best-quality option |
| POST | `/query/by-cad-files` | **Bulk lookup**  Eprimary endpoint for Claude |

### Bulk query example

```bash
curl -X POST http://localhost:8010/query/by-cad-files \
  -H "Content-Type: application/json" \
  -d '{"cad_file_names": ["shaft_001.stp", "flange_003.stp", "housing_001.stp"]}'
```

---

## MCP Tools

| Tool | Description |
|------|-------------|
| `get_part_by_cad_file(cad_file_name)` | Look up a single part |
| `get_production_history(part_id)` | Full order history |
| `get_cost_summary(part_id)` | Cost stats by production type |
| `get_recommendation(part_id)` | Cheapest / fastest / best-quality |
| `query_by_cad_files(cad_file_names)` | **Main tool**  Ebulk lookup |

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

No HOOPS AI integration code lives in this repository  Eit is a pure data service.

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
