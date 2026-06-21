"""
Run this script once to create and seed the PLM/ERP SQLite database.
    uv run python -m db.init_db
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date
from db.database import engine, SessionLocal
from db.models import Base, Part, PartStructure, Vendor, ProductionOrder, PurchaseItem


def create_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def seed(db):
    # ------------------------------------------------------------------
    # Vendors (6 total: 3 JP, 1 CN, 1 DE, 1 TH)
    # ------------------------------------------------------------------
    vendors = [
        Vendor(vendor_id="VND-001", vendor_name="Apex Precision Turning",
               specialty="turning", country="JP", rating=4.7, typical_lead_time_days=14),
        Vendor(vendor_id="VND-002", vendor_name="Sunrise Machine Works",
               specialty="turning", country="JP", rating=4.3, typical_lead_time_days=18),
        Vendor(vendor_id="VND-003", vendor_name="Fuji Sheet Metal Fabrication",
               specialty="sheet_metal", country="JP", rating=4.5, typical_lead_time_days=10),
        Vendor(vendor_id="VND-004", vendor_name="Hengda Casting Co.",
               specialty="casting", country="CN", rating=3.8, typical_lead_time_days=30),
        Vendor(vendor_id="VND-005", vendor_name="Kronberg Precision GmbH",
               specialty="grinding", country="DE", rating=4.9, typical_lead_time_days=28),
        Vendor(vendor_id="VND-006", vendor_name="Thai Star Manufacturing",
               specialty="turning", country="TH", rating=4.0, typical_lead_time_days=22),
    ]
    db.add_all(vendors)
    db.flush()

    # ------------------------------------------------------------------
    # Parts (20 total)
    # ------------------------------------------------------------------
    parts = [
        # Turned parts
        Part(part_id="PRT-0001", part_name="Main Drive Shaft", revision="C",
             material="S45C", weight_kg=2.40, drawing_number="DWG-S-0001",
             cad_file_name="shaft_001.stp", created_at=date(2021, 3, 10), status="active"),
        Part(part_id="PRT-0002", part_name="Secondary Output Shaft", revision="B",
             material="S45C", weight_kg=1.85, drawing_number="DWG-S-0002",
             cad_file_name="shaft_002.stp", created_at=date(2021, 5, 20), status="active"),
        Part(part_id="PRT-0003", part_name="Idler Shaft", revision="A",
             material="SUS304", weight_kg=0.95, drawing_number="DWG-S-0003",
             cad_file_name="shaft_003.stp", created_at=date(2022, 1, 15), status="active"),
        Part(part_id="PRT-0004", part_name="Shaft Spacer Ring", revision="A",
             material="S45C", weight_kg=0.12, drawing_number="DWG-S-0004",
             cad_file_name="spacer_001.stp", created_at=date(2022, 2, 8), status="active"),
        Part(part_id="PRT-0005", part_name="Drive Collar", revision="B",
             material="SUS304", weight_kg=0.28, drawing_number="DWG-S-0005",
             cad_file_name="collar_001.stp", created_at=date(2021, 11, 3), status="active"),
        # Sheet metal parts
        Part(part_id="PRT-0006", part_name="Motor Mounting Bracket", revision="C",
             material="A5052", weight_kg=0.65, drawing_number="DWG-M-0006",
             cad_file_name="bracket_001.stp", created_at=date(2021, 4, 22), status="active"),
        Part(part_id="PRT-0007", part_name="Cable Management Bracket", revision="A",
             material="A5052", weight_kg=0.22, drawing_number="DWG-M-0007",
             cad_file_name="bracket_002.stp", created_at=date(2022, 6, 14), status="active"),
        Part(part_id="PRT-0008", part_name="Sensor Support Bracket", revision="B",
             material="A5052", weight_kg=0.18, drawing_number="DWG-M-0008",
             cad_file_name="bracket_003.stp", created_at=date(2022, 8, 30), status="active"),
        Part(part_id="PRT-0009", part_name="Base Mounting Plate", revision="D",
             material="A5052", weight_kg=3.10, drawing_number="DWG-M-0009",
             cad_file_name="plate_001.stp", created_at=date(2020, 9, 5), status="active"),
        Part(part_id="PRT-0010", part_name="Side Cover Plate", revision="B",
             material="A5052", weight_kg=1.30, drawing_number="DWG-M-0010",
             cad_file_name="plate_002.stp", created_at=date(2021, 7, 17), status="active"),
        Part(part_id="PRT-0011", part_name="Inspection Access Lid", revision="A",
             material="A5052", weight_kg=0.48, drawing_number="DWG-M-0011",
             cad_file_name="lid_001.stp", created_at=date(2022, 3, 28), status="active"),
        # Castings / heavier components
        Part(part_id="PRT-0012", part_name="Gear Housing Body", revision="B",
             material="FC250", weight_kg=8.60, drawing_number="DWG-C-0012",
             cad_file_name="housing_001.stp", created_at=date(2020, 6, 1), status="active"),
        Part(part_id="PRT-0013", part_name="Bearing Housing", revision="C",
             material="FC250", weight_kg=4.20, drawing_number="DWG-C-0013",
             cad_file_name="housing_002.stp", created_at=date(2020, 8, 19), status="active"),
        Part(part_id="PRT-0014", part_name="End Cover Casting", revision="A",
             material="FC250", weight_kg=2.75, drawing_number="DWG-C-0014",
             cad_file_name="cover_001.stp", created_at=date(2021, 1, 12), status="active"),
        Part(part_id="PRT-0015", part_name="Cylinder Block", revision="B",
             material="FC250", weight_kg=12.40, drawing_number="DWG-C-0015",
             cad_file_name="block_001.stp", created_at=date(2020, 4, 7), status="active"),
        # Flanges
        Part(part_id="PRT-0016", part_name="Input Mounting Flange", revision="C",
             material="SUS304", weight_kg=1.05, drawing_number="DWG-F-0016",
             cad_file_name="flange_001.stp", created_at=date(2021, 2, 25), status="active"),
        Part(part_id="PRT-0017", part_name="Output Coupling Flange", revision="B",
             material="SUS304", weight_kg=0.88, drawing_number="DWG-F-0017",
             cad_file_name="flange_002.stp", created_at=date(2021, 6, 9), status="active"),
        Part(part_id="PRT-0018", part_name="Blind Flange", revision="A",
             material="S45C", weight_kg=0.72, drawing_number="DWG-F-0018",
             cad_file_name="flange_003.stp", created_at=date(2022, 4, 4), status="active"),
        # Misc turned / purchased
        Part(part_id="PRT-0019", part_name="Drive Pulley", revision="B",
             material="S45C", weight_kg=1.55, drawing_number="DWG-P-0019",
             cad_file_name="pulley_001.stp", created_at=date(2021, 9, 11), status="active"),
        Part(part_id="PRT-0020", part_name="Swing Arm", revision="A",
             material="SUS304", weight_kg=0.78, drawing_number="DWG-A-0020",
             cad_file_name="arm_001.stp", created_at=date(2022, 11, 2), status="obsolete"),
    ]
    db.add_all(parts)
    db.flush()

    # ------------------------------------------------------------------
    # Part Structures (BOM)
    # ------------------------------------------------------------------
    bom = [
        # Gear Housing assembly
        PartStructure(parent_part_id="PRT-0012", child_part_id="PRT-0001", quantity=1),
        PartStructure(parent_part_id="PRT-0012", child_part_id="PRT-0013", quantity=2),
        PartStructure(parent_part_id="PRT-0012", child_part_id="PRT-0016", quantity=1),
        PartStructure(parent_part_id="PRT-0012", child_part_id="PRT-0014", quantity=1),
        # Cylinder Block assembly
        PartStructure(parent_part_id="PRT-0015", child_part_id="PRT-0002", quantity=1),
        PartStructure(parent_part_id="PRT-0015", child_part_id="PRT-0009", quantity=1),
        PartStructure(parent_part_id="PRT-0015", child_part_id="PRT-0017", quantity=2),
        # Drive shaft sub-assembly
        PartStructure(parent_part_id="PRT-0001", child_part_id="PRT-0004", quantity=2),
        PartStructure(parent_part_id="PRT-0001", child_part_id="PRT-0005", quantity=1),
    ]
    db.add_all(bom)
    db.flush()

    # ------------------------------------------------------------------
    # Production Orders  (3–5 per part)
    # ------------------------------------------------------------------
    orders = [
        # PRT-0001  Main Drive Shaft
        ProductionOrder(order_id="PO-2021-0001", part_id="PRT-0001", production_type="outsource",
                        vendor_id="VND-001", quantity=50, unit_cost_jpy=220.0, lead_time_days=16,
                        delivery_date=date(2021, 5, 10), quality_result="pass",
                        notes="Initial production run"),
        ProductionOrder(order_id="PO-2022-0001", part_id="PRT-0001", production_type="outsource",
                        vendor_id="VND-001", quantity=100, unit_cost_jpy=205.0, lead_time_days=14,
                        delivery_date=date(2022, 3, 15), quality_result="pass",
                        notes="Volume discount applied"),
        ProductionOrder(order_id="PO-2022-0031", part_id="PRT-0001", production_type="outsource",
                        vendor_id="VND-006", quantity=80, unit_cost_jpy=175.0, lead_time_days=24,
                        delivery_date=date(2022, 9, 20), quality_result="conditional",
                        notes="Surface finish rework required"),
        ProductionOrder(order_id="PO-2023-0001", part_id="PRT-0001", production_type="in_house",
                        vendor_id=None, quantity=30, unit_cost_jpy=260.0, lead_time_days=10,
                        delivery_date=date(2023, 2, 28), quality_result="pass",
                        notes="Urgent order, in-house machining"),
        ProductionOrder(order_id="PO-2024-0001", part_id="PRT-0001", production_type="outsource",
                        vendor_id="VND-001", quantity=120, unit_cost_jpy=198.0, lead_time_days=14,
                        delivery_date=date(2024, 1, 20), quality_result="pass",
                        notes="Annual contract order"),

        # PRT-0002  Secondary Output Shaft
        ProductionOrder(order_id="PO-2021-0010", part_id="PRT-0002", production_type="outsource",
                        vendor_id="VND-002", quantity=60, unit_cost_jpy=185.0, lead_time_days=20,
                        delivery_date=date(2021, 7, 5), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2022-0010", part_id="PRT-0002", production_type="outsource",
                        vendor_id="VND-006", quantity=60, unit_cost_jpy=155.0, lead_time_days=25,
                        delivery_date=date(2022, 5, 12), quality_result="pass", notes="Cost reduction trial"),
        ProductionOrder(order_id="PO-2023-0010", part_id="PRT-0002", production_type="outsource",
                        vendor_id="VND-002", quantity=80, unit_cost_jpy=180.0, lead_time_days=18,
                        delivery_date=date(2023, 4, 22), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2024-0010", part_id="PRT-0002", production_type="in_house",
                        vendor_id=None, quantity=20, unit_cost_jpy=230.0, lead_time_days=8,
                        delivery_date=date(2024, 3, 10), quality_result="pass", notes="Prototype batch"),

        # PRT-0003  Idler Shaft
        ProductionOrder(order_id="PO-2022-0020", part_id="PRT-0003", production_type="outsource",
                        vendor_id="VND-001", quantity=100, unit_cost_jpy=98.0, lead_time_days=14,
                        delivery_date=date(2022, 4, 18), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0020", part_id="PRT-0003", production_type="outsource",
                        vendor_id="VND-002", quantity=100, unit_cost_jpy=92.0, lead_time_days=20,
                        delivery_date=date(2023, 1, 30), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2024-0020", part_id="PRT-0003", production_type="outsource",
                        vendor_id="VND-006", quantity=150, unit_cost_jpy=78.0, lead_time_days=22,
                        delivery_date=date(2024, 2, 15), quality_result="conditional",
                        notes="Minor dimensional deviation"),

        # PRT-0004  Shaft Spacer Ring
        ProductionOrder(order_id="PO-2022-0030", part_id="PRT-0004", production_type="purchase",
                        vendor_id="VND-001", quantity=500, unit_cost_jpy=12.0, lead_time_days=10,
                        delivery_date=date(2022, 3, 5), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0030", part_id="PRT-0004", production_type="purchase",
                        vendor_id="VND-001", quantity=500, unit_cost_jpy=11.5, lead_time_days=10,
                        delivery_date=date(2023, 3, 1), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2024-0030", part_id="PRT-0004", production_type="purchase",
                        vendor_id="VND-006", quantity=1000, unit_cost_jpy=9.0, lead_time_days=20,
                        delivery_date=date(2024, 1, 25), quality_result="pass", notes="Bulk purchase"),

        # PRT-0005  Drive Collar
        ProductionOrder(order_id="PO-2021-0040", part_id="PRT-0005", production_type="outsource",
                        vendor_id="VND-001", quantity=200, unit_cost_jpy=35.0, lead_time_days=14,
                        delivery_date=date(2021, 12, 20), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2022-0040", part_id="PRT-0005", production_type="outsource",
                        vendor_id="VND-002", quantity=200, unit_cost_jpy=32.0, lead_time_days=18,
                        delivery_date=date(2022, 11, 8), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0040", part_id="PRT-0005", production_type="in_house",
                        vendor_id=None, quantity=50, unit_cost_jpy=48.0, lead_time_days=7,
                        delivery_date=date(2023, 6, 14), quality_result="pass",
                        notes="Urgent replacement batch"),
        ProductionOrder(order_id="PO-2024-0040", part_id="PRT-0005", production_type="outsource",
                        vendor_id="VND-001", quantity=300, unit_cost_jpy=30.0, lead_time_days=14,
                        delivery_date=date(2024, 4, 3), quality_result="pass", notes="Annual order"),

        # PRT-0006  Motor Mounting Bracket
        ProductionOrder(order_id="PO-2021-0050", part_id="PRT-0006", production_type="outsource",
                        vendor_id="VND-003", quantity=80, unit_cost_jpy=55.0, lead_time_days=12,
                        delivery_date=date(2021, 6, 25), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2022-0050", part_id="PRT-0006", production_type="outsource",
                        vendor_id="VND-003", quantity=120, unit_cost_jpy=50.0, lead_time_days=10,
                        delivery_date=date(2022, 7, 14), quality_result="pass",
                        notes="New powder coat finish"),
        ProductionOrder(order_id="PO-2023-0050", part_id="PRT-0006", production_type="outsource",
                        vendor_id="VND-004", quantity=200, unit_cost_jpy=38.0, lead_time_days=35,
                        delivery_date=date(2023, 5, 20), quality_result="fail",
                        notes="Hole pattern out of tolerance; rejected"),
        ProductionOrder(order_id="PO-2023-0051", part_id="PRT-0006", production_type="outsource",
                        vendor_id="VND-003", quantity=200, unit_cost_jpy=52.0, lead_time_days=10,
                        delivery_date=date(2023, 7, 8), quality_result="pass",
                        notes="Re-order after VND-004 rejection"),
        ProductionOrder(order_id="PO-2024-0050", part_id="PRT-0006", production_type="outsource",
                        vendor_id="VND-003", quantity=150, unit_cost_jpy=49.0, lead_time_days=10,
                        delivery_date=date(2024, 2, 28), quality_result="pass", notes=None),

        # PRT-0007  Cable Management Bracket
        ProductionOrder(order_id="PO-2022-0060", part_id="PRT-0007", production_type="outsource",
                        vendor_id="VND-003", quantity=300, unit_cost_jpy=18.0, lead_time_days=10,
                        delivery_date=date(2022, 8, 10), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0060", part_id="PRT-0007", production_type="outsource",
                        vendor_id="VND-003", quantity=400, unit_cost_jpy=17.0, lead_time_days=10,
                        delivery_date=date(2023, 8, 22), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2024-0060", part_id="PRT-0007", production_type="in_house",
                        vendor_id=None, quantity=100, unit_cost_jpy=25.0, lead_time_days=5,
                        delivery_date=date(2024, 4, 15), quality_result="pass",
                        notes="In-house to meet tight deadline"),

        # PRT-0008  Sensor Support Bracket
        ProductionOrder(order_id="PO-2022-0070", part_id="PRT-0008", production_type="outsource",
                        vendor_id="VND-003", quantity=150, unit_cost_jpy=22.0, lead_time_days=10,
                        delivery_date=date(2022, 10, 5), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0070", part_id="PRT-0008", production_type="outsource",
                        vendor_id="VND-004", quantity=300, unit_cost_jpy=15.0, lead_time_days=32,
                        delivery_date=date(2023, 9, 18), quality_result="conditional",
                        notes="Slight burr on edge; accepted with rework"),
        ProductionOrder(order_id="PO-2024-0070", part_id="PRT-0008", production_type="outsource",
                        vendor_id="VND-003", quantity=200, unit_cost_jpy=21.0, lead_time_days=10,
                        delivery_date=date(2024, 3, 25), quality_result="pass", notes=None),

        # PRT-0009  Base Mounting Plate
        ProductionOrder(order_id="PO-2020-0080", part_id="PRT-0009", production_type="outsource",
                        vendor_id="VND-003", quantity=40, unit_cost_jpy=185.0, lead_time_days=14,
                        delivery_date=date(2020, 11, 20), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2021-0080", part_id="PRT-0009", production_type="outsource",
                        vendor_id="VND-003", quantity=60, unit_cost_jpy=175.0, lead_time_days=12,
                        delivery_date=date(2021, 10, 15), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2022-0080", part_id="PRT-0009", production_type="outsource",
                        vendor_id="VND-004", quantity=100, unit_cost_jpy=130.0, lead_time_days=35,
                        delivery_date=date(2022, 12, 5), quality_result="pass",
                        notes="Overseas sourcing for cost reduction"),
        ProductionOrder(order_id="PO-2024-0080", part_id="PRT-0009", production_type="outsource",
                        vendor_id="VND-003", quantity=80, unit_cost_jpy=170.0, lead_time_days=12,
                        delivery_date=date(2024, 1, 10), quality_result="pass", notes=None),

        # PRT-0010  Side Cover Plate
        ProductionOrder(order_id="PO-2021-0090", part_id="PRT-0010", production_type="outsource",
                        vendor_id="VND-003", quantity=80, unit_cost_jpy=95.0, lead_time_days=10,
                        delivery_date=date(2021, 8, 20), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2022-0090", part_id="PRT-0010", production_type="outsource",
                        vendor_id="VND-003", quantity=120, unit_cost_jpy=90.0, lead_time_days=10,
                        delivery_date=date(2022, 6, 30), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0090", part_id="PRT-0010", production_type="outsource",
                        vendor_id="VND-004", quantity=200, unit_cost_jpy=68.0, lead_time_days=32,
                        delivery_date=date(2023, 10, 14), quality_result="conditional",
                        notes="Powder coat adhesion issue on 5%"),
        ProductionOrder(order_id="PO-2024-0090", part_id="PRT-0010", production_type="outsource",
                        vendor_id="VND-003", quantity=100, unit_cost_jpy=88.0, lead_time_days=10,
                        delivery_date=date(2024, 2, 12), quality_result="pass", notes=None),

        # PRT-0011  Inspection Access Lid
        ProductionOrder(order_id="PO-2022-0100", part_id="PRT-0011", production_type="outsource",
                        vendor_id="VND-003", quantity=200, unit_cost_jpy=28.0, lead_time_days=10,
                        delivery_date=date(2022, 5, 22), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0100", part_id="PRT-0011", production_type="outsource",
                        vendor_id="VND-003", quantity=300, unit_cost_jpy=26.0, lead_time_days=10,
                        delivery_date=date(2023, 4, 10), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2024-0100", part_id="PRT-0011", production_type="in_house",
                        vendor_id=None, quantity=50, unit_cost_jpy=38.0, lead_time_days=5,
                        delivery_date=date(2024, 5, 8), quality_result="pass", notes="Prototype revision"),

        # PRT-0012  Gear Housing Body
        ProductionOrder(order_id="PO-2020-0110", part_id="PRT-0012", production_type="outsource",
                        vendor_id="VND-004", quantity=20, unit_cost_jpy=680.0, lead_time_days=45,
                        delivery_date=date(2020, 10, 1), quality_result="pass", notes="Casting + rough machining"),
        ProductionOrder(order_id="PO-2021-0110", part_id="PRT-0012", production_type="outsource",
                        vendor_id="VND-004", quantity=30, unit_cost_jpy=650.0, lead_time_days=42,
                        delivery_date=date(2021, 9, 15), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2022-0110", part_id="PRT-0012", production_type="outsource",
                        vendor_id="VND-004", quantity=40, unit_cost_jpy=620.0, lead_time_days=40,
                        delivery_date=date(2022, 8, 28), quality_result="conditional",
                        notes="Porosity in two castings; accepted after inspection"),
        ProductionOrder(order_id="PO-2023-0110", part_id="PRT-0012", production_type="outsource",
                        vendor_id="VND-004", quantity=50, unit_cost_jpy=600.0, lead_time_days=38,
                        delivery_date=date(2023, 11, 5), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2024-0110", part_id="PRT-0012", production_type="outsource",
                        vendor_id="VND-004", quantity=60, unit_cost_jpy=580.0, lead_time_days=35,
                        delivery_date=date(2024, 3, 18), quality_result="pass", notes=None),

        # PRT-0013  Bearing Housing
        ProductionOrder(order_id="PO-2020-0120", part_id="PRT-0013", production_type="outsource",
                        vendor_id="VND-004", quantity=40, unit_cost_jpy=320.0, lead_time_days=35,
                        delivery_date=date(2020, 12, 10), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2021-0120", part_id="PRT-0013", production_type="outsource",
                        vendor_id="VND-004", quantity=60, unit_cost_jpy=305.0, lead_time_days=32,
                        delivery_date=date(2021, 11, 25), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2022-0120", part_id="PRT-0013", production_type="in_house",
                        vendor_id=None, quantity=10, unit_cost_jpy=420.0, lead_time_days=12,
                        delivery_date=date(2022, 2, 18), quality_result="pass",
                        notes="Prototype for new design"),
        ProductionOrder(order_id="PO-2023-0120", part_id="PRT-0013", production_type="outsource",
                        vendor_id="VND-004", quantity=80, unit_cost_jpy=295.0, lead_time_days=30,
                        delivery_date=date(2023, 7, 14), quality_result="pass", notes=None),

        # PRT-0014  End Cover Casting
        ProductionOrder(order_id="PO-2021-0130", part_id="PRT-0014", production_type="outsource",
                        vendor_id="VND-004", quantity=50, unit_cost_jpy=210.0, lead_time_days=38,
                        delivery_date=date(2021, 4, 12), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2022-0130", part_id="PRT-0014", production_type="outsource",
                        vendor_id="VND-004", quantity=80, unit_cost_jpy=198.0, lead_time_days=35,
                        delivery_date=date(2022, 4, 25), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0130", part_id="PRT-0014", production_type="outsource",
                        vendor_id="VND-004", quantity=100, unit_cost_jpy=188.0, lead_time_days=33,
                        delivery_date=date(2023, 6, 8), quality_result="pass", notes=None),

        # PRT-0015  Cylinder Block
        ProductionOrder(order_id="PO-2020-0140", part_id="PRT-0015", production_type="outsource",
                        vendor_id="VND-004", quantity=10, unit_cost_jpy=1250.0, lead_time_days=55,
                        delivery_date=date(2020, 8, 20), quality_result="pass", notes="Large casting order"),
        ProductionOrder(order_id="PO-2021-0140", part_id="PRT-0015", production_type="outsource",
                        vendor_id="VND-004", quantity=15, unit_cost_jpy=1180.0, lead_time_days=50,
                        delivery_date=date(2021, 10, 5), quality_result="conditional",
                        notes="Surface porosity; machined away"),
        ProductionOrder(order_id="PO-2022-0140", part_id="PRT-0015", production_type="outsource",
                        vendor_id="VND-004", quantity=20, unit_cost_jpy=1120.0, lead_time_days=48,
                        delivery_date=date(2022, 10, 12), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0140", part_id="PRT-0015", production_type="outsource",
                        vendor_id="VND-004", quantity=25, unit_cost_jpy=1080.0, lead_time_days=45,
                        delivery_date=date(2023, 12, 20), quality_result="pass", notes=None),

        # PRT-0016  Input Mounting Flange
        ProductionOrder(order_id="PO-2021-0150", part_id="PRT-0016", production_type="outsource",
                        vendor_id="VND-001", quantity=80, unit_cost_jpy=88.0, lead_time_days=16,
                        delivery_date=date(2021, 4, 8), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2022-0150", part_id="PRT-0016", production_type="outsource",
                        vendor_id="VND-001", quantity=100, unit_cost_jpy=82.0, lead_time_days=14,
                        delivery_date=date(2022, 3, 22), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0150", part_id="PRT-0016", production_type="outsource",
                        vendor_id="VND-005", quantity=50, unit_cost_jpy=115.0, lead_time_days=30,
                        delivery_date=date(2023, 8, 10), quality_result="pass",
                        notes="High-precision trial with Kronberg"),
        ProductionOrder(order_id="PO-2024-0150", part_id="PRT-0016", production_type="outsource",
                        vendor_id="VND-001", quantity=120, unit_cost_jpy=80.0, lead_time_days=14,
                        delivery_date=date(2024, 2, 5), quality_result="pass", notes=None),

        # PRT-0017  Output Coupling Flange
        ProductionOrder(order_id="PO-2021-0160", part_id="PRT-0017", production_type="outsource",
                        vendor_id="VND-002", quantity=80, unit_cost_jpy=78.0, lead_time_days=20,
                        delivery_date=date(2021, 7, 28), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2022-0160", part_id="PRT-0017", production_type="outsource",
                        vendor_id="VND-001", quantity=100, unit_cost_jpy=72.0, lead_time_days=14,
                        delivery_date=date(2022, 6, 10), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0160", part_id="PRT-0017", production_type="outsource",
                        vendor_id="VND-006", quantity=150, unit_cost_jpy=58.0, lead_time_days=24,
                        delivery_date=date(2023, 5, 18), quality_result="pass", notes="Overseas sourcing trial"),
        ProductionOrder(order_id="PO-2024-0160", part_id="PRT-0017", production_type="outsource",
                        vendor_id="VND-001", quantity=120, unit_cost_jpy=70.0, lead_time_days=14,
                        delivery_date=date(2024, 3, 1), quality_result="pass", notes=None),

        # PRT-0018  Blind Flange
        ProductionOrder(order_id="PO-2022-0170", part_id="PRT-0018", production_type="purchase",
                        vendor_id="VND-002", quantity=200, unit_cost_jpy=42.0, lead_time_days=18,
                        delivery_date=date(2022, 5, 30), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0170", part_id="PRT-0018", production_type="purchase",
                        vendor_id="VND-006", quantity=300, unit_cost_jpy=32.0, lead_time_days=22,
                        delivery_date=date(2023, 4, 15), quality_result="pass",
                        notes="Lower-cost overseas option"),
        ProductionOrder(order_id="PO-2024-0170", part_id="PRT-0018", production_type="purchase",
                        vendor_id="VND-002", quantity=200, unit_cost_jpy=40.0, lead_time_days=18,
                        delivery_date=date(2024, 4, 10), quality_result="pass", notes=None),

        # PRT-0019  Drive Pulley
        ProductionOrder(order_id="PO-2021-0180", part_id="PRT-0019", production_type="outsource",
                        vendor_id="VND-001", quantity=60, unit_cost_jpy=128.0, lead_time_days=16,
                        delivery_date=date(2021, 10, 22), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2022-0180", part_id="PRT-0019", production_type="outsource",
                        vendor_id="VND-002", quantity=80, unit_cost_jpy=118.0, lead_time_days=20,
                        delivery_date=date(2022, 9, 5), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0180", part_id="PRT-0019", production_type="outsource",
                        vendor_id="VND-006", quantity=100, unit_cost_jpy=95.0, lead_time_days=24,
                        delivery_date=date(2023, 9, 30), quality_result="conditional",
                        notes="Keyway tolerance borderline"),
        ProductionOrder(order_id="PO-2024-0180", part_id="PRT-0019", production_type="outsource",
                        vendor_id="VND-001", quantity=100, unit_cost_jpy=122.0, lead_time_days=14,
                        delivery_date=date(2024, 4, 20), quality_result="pass", notes=None),

        # PRT-0020  Swing Arm (obsolete)
        ProductionOrder(order_id="PO-2022-0190", part_id="PRT-0020", production_type="outsource",
                        vendor_id="VND-001", quantity=40, unit_cost_jpy=68.0, lead_time_days=16,
                        delivery_date=date(2022, 11, 18), quality_result="pass", notes=None),
        ProductionOrder(order_id="PO-2023-0190", part_id="PRT-0020", production_type="outsource",
                        vendor_id="VND-006", quantity=60, unit_cost_jpy=52.0, lead_time_days=24,
                        delivery_date=date(2023, 3, 25), quality_result="fail",
                        notes="Weld crack detected; design obsoleted after failure"),
    ]
    db.add_all(orders)
    db.flush()

    # ------------------------------------------------------------------
    # Purchase Items
    # ------------------------------------------------------------------
    purchase_items = [
        PurchaseItem(item_id="ITM-0001", part_id="PRT-0004", vendor_id="VND-001",
                     catalog_price_jpy=12.5, min_order_qty=100, lead_time_days=10),
        PurchaseItem(item_id="ITM-0002", part_id="PRT-0004", vendor_id="VND-006",
                     catalog_price_jpy=9.5, min_order_qty=500, lead_time_days=20),
        PurchaseItem(item_id="ITM-0003", part_id="PRT-0018", vendor_id="VND-002",
                     catalog_price_jpy=43.0, min_order_qty=50, lead_time_days=18),
        PurchaseItem(item_id="ITM-0004", part_id="PRT-0018", vendor_id="VND-006",
                     catalog_price_jpy=33.0, min_order_qty=100, lead_time_days=22),
        PurchaseItem(item_id="ITM-0005", part_id="PRT-0005", vendor_id="VND-001",
                     catalog_price_jpy=31.0, min_order_qty=50, lead_time_days=14),
        PurchaseItem(item_id="ITM-0006", part_id="PRT-0007", vendor_id="VND-003",
                     catalog_price_jpy=17.5, min_order_qty=100, lead_time_days=10),
    ]
    db.add_all(purchase_items)
    db.commit()
    print(f"Seeded: {len(vendors)} vendors, {len(parts)} parts, "
          f"{len(bom)} BOM rows, {len(orders)} production orders, "
          f"{len(purchase_items)} purchase items.")


if __name__ == "__main__":
    print("Creating tables...")
    create_tables()
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
    print("Database ready: plm_erp.db")
