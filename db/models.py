from sqlalchemy import Column, Integer, Text, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Part(Base):
    __tablename__ = "parts"

    part_id = Column(Text, primary_key=True)
    part_name = Column(Text, nullable=False)
    revision = Column(Text, nullable=False)
    material = Column(Text, nullable=False)
    weight_kg = Column(Float, nullable=False)
    drawing_number = Column(Text, nullable=False)
    cad_file_name = Column(Text, unique=True, nullable=False)
    created_at = Column(Date, nullable=False)
    status = Column(Text, nullable=False)

    children = relationship(
        "PartStructure", foreign_keys="PartStructure.parent_part_id", back_populates="parent"
    )
    parents = relationship(
        "PartStructure", foreign_keys="PartStructure.child_part_id", back_populates="child"
    )
    production_orders = relationship("ProductionOrder", back_populates="part")
    purchase_items = relationship("PurchaseItem", back_populates="part")


class PartStructure(Base):
    __tablename__ = "part_structures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_part_id = Column(Text, ForeignKey("parts.part_id"), nullable=False)
    child_part_id = Column(Text, ForeignKey("parts.part_id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    parent = relationship("Part", foreign_keys=[parent_part_id], back_populates="children")
    child = relationship("Part", foreign_keys=[child_part_id], back_populates="parents")


class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id = Column(Text, primary_key=True)
    vendor_name = Column(Text, nullable=False)
    specialty = Column(Text, nullable=False)
    country = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)
    typical_lead_time_days = Column(Integer, nullable=False)

    production_orders = relationship("ProductionOrder", back_populates="vendor")
    purchase_items = relationship("PurchaseItem", back_populates="vendor")


class ProductionOrder(Base):
    __tablename__ = "production_orders"

    order_id = Column(Text, primary_key=True)
    part_id = Column(Text, ForeignKey("parts.part_id"), nullable=False)
    production_type = Column(Text, nullable=False)
    vendor_id = Column(Text, ForeignKey("vendors.vendor_id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_cost_jpy = Column(Float, nullable=False)
    lead_time_days = Column(Integer, nullable=False)
    delivery_date = Column(Date, nullable=False)
    quality_result = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)

    part = relationship("Part", back_populates="production_orders")
    vendor = relationship("Vendor", back_populates="production_orders")


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    item_id = Column(Text, primary_key=True)
    part_id = Column(Text, ForeignKey("parts.part_id"), nullable=False)
    vendor_id = Column(Text, ForeignKey("vendors.vendor_id"), nullable=False)
    catalog_price_jpy = Column(Float, nullable=False)
    min_order_qty = Column(Integer, nullable=False)
    lead_time_days = Column(Integer, nullable=False)

    part = relationship("Part", back_populates="purchase_items")
    vendor = relationship("Vendor", back_populates="purchase_items")
