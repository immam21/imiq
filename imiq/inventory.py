"""
IMIQ Inventory Service
Handles inventory management, stock tracking, and low stock alerts
"""

import pandas as pd
from typing import Dict, Any, List, Optional
import logging

from .storage import StorageBase
from .utils import get_ist_now

logger = logging.getLogger(__name__)

class InventoryService:
    """Service for managing inventory using ProductList sheet from CZ_MasterSheet"""
    
    def __init__(self, storage: StorageBase):
        self.storage = storage
    
    def get_all_inventory(self) -> pd.DataFrame:
        """Get all products from ProductList sheet"""
        try:
            from .performance import get_cached_sheet_data
            inventory_df = get_cached_sheet_data(self.storage, "ProductList")
            
            if not inventory_df.empty:
                # Ensure numeric columns are properly typed
                numeric_columns = ['stock', 'price']
                for col in numeric_columns:
                    if col in inventory_df.columns:
                        inventory_df[col] = pd.to_numeric(inventory_df[col], errors='coerce').fillna(0)
                
                # Sort by product name
                inventory_df = inventory_df.sort_values('product_name', ascending=True)
            
            return inventory_df
            
        except Exception as e:
            logger.error(f"Error retrieving inventory: {e}")
            return pd.DataFrame()
    
    def get_item_by_sku(self, sku: str) -> Optional[pd.Series]:
        """Get a specific product by SKU"""
        try:
            inventory_df = self.get_all_inventory()
            
            if inventory_df.empty or 'sku' not in inventory_df.columns:
                return None
            
            matching_items = inventory_df[inventory_df['sku'] == sku]
            
            if matching_items.empty:
                return None
            
            return matching_items.iloc[0]
            
        except Exception as e:
            logger.error(f"Error retrieving item {sku}: {e}")
            return None
    
    def get_item_by_name(self, product_name: str) -> Optional[pd.Series]:
        """Get a specific product by name"""
        try:
            inventory_df = self.get_all_inventory()
            
            if inventory_df.empty or 'product_name' not in inventory_df.columns:
                return None
            
            matching_items = inventory_df[inventory_df['product_name'].str.lower() == product_name.lower()]
            
            if matching_items.empty:
                return None
            
            return matching_items.iloc[0]
            
        except Exception as e:
            logger.error(f"Error retrieving item {product_name}: {e}")
            return None
    
    def add_item(self, item_data: Dict[str, Any]) -> bool:
        """Add a new product to ProductList"""
        try:
            # Validate item data
            self._validate_item_data(item_data)
            
            # Check if SKU already exists
            existing_item = self.get_item_by_sku(item_data['sku'])
            if existing_item is not None:
                raise ValueError(f"Item with SKU {item_data['sku']} already exists")
            
            # Prepare complete item data matching ProductList schema
            complete_item_data = {
                'product_name': item_data['product_name'],
                'price': float(item_data['price']),
                'description': item_data.get('description', ''),
                'stock': int(item_data.get('stock', 0)),
                'category': item_data.get('category', 'General'),
                'sku': item_data['sku'],
                'status': item_data.get('status', 'active'),
                'image_url': item_data.get('image_url', '')
            }
            
            # Add to storage
            self.storage.append_row("ProductList", complete_item_data)
            
            logger.info(f"Product added: {item_data['sku']}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding product: {e}")
            raise
    
    def update_item(self, sku: str, update_data: Dict[str, Any]) -> bool:
        """Update an existing product"""
        try:
            def filter_fn(row):
                return row['sku'] == sku
            
            def update_fn(row):
                # Only update allowed fields
                allowed_fields = ['product_name', 'price', 'description', 'stock', 'category', 'status', 'image_url']
                
                for field, value in update_data.items():
                    if field in allowed_fields:
                        if field in ['stock']:
                            row[field] = int(value)
                        elif field == 'price':
                            row[field] = float(value)
                        else:
                            row[field] = value
                
                return row
            
            updated_count = self.storage.update_rows("ProductList", filter_fn, update_fn)
            
            if updated_count > 0:
                logger.info(f"Product {sku} updated successfully")
                return True
            else:
                logger.warning(f"Product {sku} not found for update")
                return False
            
        except Exception as e:
            logger.error(f"Error updating product {sku}: {e}")
            raise
    
    def upsert_item(self, item_data: Dict[str, Any]) -> bool:
        """Add or update a product (upsert operation)"""
        try:
            sku = item_data['sku']
            existing_item = self.get_item_by_sku(sku)
            
            if existing_item is not None:
                # Update existing item
                return self.update_item(sku, item_data)
            else:
                # Add new item
                return self.add_item(item_data)
                
        except Exception as e:
            logger.error(f"Error upserting product: {e}")
            raise
    
    def adjust_stock(self, sku: str, quantity_change: int, reason: str = "") -> bool:
        """Adjust stock quantity for an item (positive or negative)"""
        try:
            item = self.get_item_by_sku(sku)
            if item is None:
                raise ValueError(f"Item with SKU {sku} not found")
            
            current_quantity = int(item['quantity'])
            new_quantity = max(0, current_quantity + quantity_change)  # Prevent negative stock
            
            update_data = {'quantity': new_quantity}
            success = self.update_item(sku, update_data)
            
            if success:
                logger.info(f"Stock adjusted for {sku}: {current_quantity} → {new_quantity} (change: {quantity_change}, reason: {reason})")
            
            return success
            
        except Exception as e:
            logger.error(f"Error adjusting stock for {sku}: {e}")
            raise
    
    def reduce_stock(self, sku: str, quantity: int) -> bool:
        """Reduce stock quantity (typically when order is placed)"""
        return self.adjust_stock(sku, -quantity, "Order fulfillment")
    
    def increase_stock(self, sku: str, quantity: int) -> bool:
        """Increase stock quantity (typically when stock arrives)"""
        return self.adjust_stock(sku, quantity, "Stock replenishment")
    
    def get_low_stock_alerts(self) -> pd.DataFrame:
        """Get products that are low on stock"""
        try:
            inventory_df = self.get_all_inventory()
            
            if inventory_df.empty:
                return pd.DataFrame()
            
            # Consider items with stock <= 5 as low stock
            low_stock_threshold = 5
            low_stock = inventory_df[
                inventory_df['stock'] <= low_stock_threshold
            ].copy()
            
            if not low_stock.empty:
                # Add urgency indicator
                low_stock['urgency'] = low_stock.apply(
                    lambda row: 'Critical' if row['stock'] == 0 else 
                               'High' if row['stock'] <= 2 else 'Medium', 
                    axis=1
                )
                
                # Sort by urgency and stock level
                urgency_order = {'Critical': 0, 'High': 1, 'Medium': 2}
                low_stock['urgency_order'] = low_stock['urgency'].map(urgency_order)
                low_stock = low_stock.sort_values(['urgency_order', 'stock'])
                low_stock = low_stock.drop('urgency_order', axis=1)
            
            return low_stock
            
        except Exception as e:
            logger.error(f"Error getting low stock alerts: {e}")
            return pd.DataFrame()
    
    def search_inventory(self, search_term: str, search_field: str = "All") -> pd.DataFrame:
        """Search inventory items"""
        try:
            inventory_df = self.get_all_inventory()
            
            if inventory_df.empty or not search_term:
                return inventory_df
            
            search_term = search_term.lower().strip()
            
            if search_field == "All":
                # Search across all text fields
                text_columns = ['sku', 'name']
                mask = pd.Series([False] * len(inventory_df))
                
                for col in text_columns:
                    if col in inventory_df.columns:
                        mask |= inventory_df[col].astype(str).str.lower().str.contains(search_term, na=False)
                
                inventory_df = inventory_df[mask]
                
            elif search_field == "sku":
                # Exact or partial match for SKU
                inventory_df = inventory_df[
                    inventory_df['sku'].astype(str).str.lower().str.contains(search_term, na=False)
                ]
                
            elif search_field == "name":
                # Search in product name
                inventory_df = inventory_df[
                    inventory_df['name'].astype(str).str.lower().str.contains(search_term, na=False)
                ]
            
            return inventory_df
            
        except Exception as e:
            logger.error(f"Error searching inventory: {e}")
            return pd.DataFrame()
    
    def delete_item(self, sku: str) -> bool:
        """Delete an inventory item (use with caution)"""
        try:
            from .performance import get_cached_sheet_data
            inventory_df = get_cached_sheet_data(self.storage, "Inventory")
            
            if inventory_df.empty:
                return False
            
            # Remove the item
            filtered_df = inventory_df[inventory_df['sku'] != sku]
            
            # Check if any row was actually removed
            if len(filtered_df) == len(inventory_df):
                logger.warning(f"Inventory item {sku} not found for deletion")
                return False
            
            # Replace the sheet with filtered data
            self.storage.replace_sheet("Inventory", filtered_df)
            
            logger.info(f"Inventory item {sku} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting inventory item {sku}: {e}")
            raise
    
    def get_inventory_value(self) -> Dict[str, float]:
        """Calculate total inventory value and related metrics"""
        try:
            inventory_df = self.get_all_inventory()
            
            if inventory_df.empty:
                return {
                    'total_value': 0.0,
                    'total_items': 0,
                    'total_stock_units': 0,
                    'average_item_value': 0.0,
                    'low_stock_value': 0.0
                }
            
            # Calculate values
            inventory_df['total_value'] = inventory_df['quantity'] * inventory_df['price']
            
            total_value = float(inventory_df['total_value'].sum())
            total_items = len(inventory_df)
            total_stock_units = int(inventory_df['quantity'].sum())
            average_item_value = float(inventory_df['total_value'].mean()) if total_items > 0 else 0.0
            
            # Calculate value of low stock items
            low_stock_items = inventory_df[inventory_df['quantity'] <= inventory_df['reorder_level']]
            low_stock_value = float(low_stock_items['total_value'].sum()) if not low_stock_items.empty else 0.0
            
            return {
                'total_value': total_value,
                'total_items': total_items,
                'total_stock_units': total_stock_units,
                'average_item_value': average_item_value,
                'low_stock_value': low_stock_value
            }
            
        except Exception as e:
            logger.error(f"Error calculating inventory value: {e}")
            return {
                'total_value': 0.0,
                'total_items': 0,
                'total_stock_units': 0,
                'average_item_value': 0.0,
                'low_stock_value': 0.0
            }
    
    def get_inventory_turnover_data(self) -> pd.DataFrame:
        """Get inventory turnover data (placeholder - would need sales data)"""
        try:
            # This is a placeholder implementation
            # In a real system, you would:
            # 1. Join with order/sales data to calculate turnover
            # 2. Calculate how fast each item sells
            # 3. Identify fast/slow moving items
            
            inventory_df = self.get_all_inventory()
            
            if inventory_df.empty:
                return pd.DataFrame()
            
            # For now, return inventory with placeholder turnover metrics
            turnover_df = inventory_df.copy()
            
            # Placeholder calculations (replace with real sales data analysis)
            turnover_df['days_of_stock'] = (turnover_df['quantity'] / 1).round(0)  # Assume 1 unit/day sales rate
            turnover_df['turnover_category'] = turnover_df['days_of_stock'].apply(
                lambda x: 'Fast' if x < 30 else 'Medium' if x < 90 else 'Slow'
            )
            
            return turnover_df
            
        except Exception as e:
            logger.error(f"Error calculating inventory turnover: {e}")
            return pd.DataFrame()
    
    def generate_reorder_report(self) -> Dict[str, Any]:
        """Generate a comprehensive reorder report"""
        try:
            low_stock_items = self.get_low_stock_alerts()
            inventory_value = self.get_inventory_value()
            
            report = {
                'report_date': get_ist_now().isoformat(),
                'total_items_to_reorder': len(low_stock_items),
                'critical_items': len(low_stock_items[low_stock_items['urgency'] == 'Critical']) if not low_stock_items.empty else 0,
                'high_priority_items': len(low_stock_items[low_stock_items['urgency'] == 'High']) if not low_stock_items.empty else 0,
                'medium_priority_items': len(low_stock_items[low_stock_items['urgency'] == 'Medium']) if not low_stock_items.empty else 0,
                'estimated_reorder_cost': 0.0,
                'inventory_health_score': 0.0,
                'recommendations': []
            }
            
            # Calculate estimated reorder cost
            if not low_stock_items.empty:
                # Estimate cost to bring each item to reorder level * 2
                low_stock_items['reorder_quantity'] = (low_stock_items['reorder_level'] * 2) - low_stock_items['quantity']
                low_stock_items['reorder_cost'] = low_stock_items['reorder_quantity'] * low_stock_items['price']
                report['estimated_reorder_cost'] = float(low_stock_items['reorder_cost'].sum())
            
            # Calculate inventory health score (0-100)
            total_items = inventory_value['total_items']
            items_needing_reorder = len(low_stock_items)
            
            if total_items > 0:
                health_score = max(0, 100 - (items_needing_reorder / total_items * 100))
                report['inventory_health_score'] = round(health_score, 1)
            
            # Generate recommendations
            if report['critical_items'] > 0:
                report['recommendations'].append("Immediate action required: Critical items are out of stock!")
            
            if report['high_priority_items'] > 0:
                report['recommendations'].append("High priority: Several items are below safety stock levels.")
            
            if report['inventory_health_score'] < 70:
                report['recommendations'].append("Consider reviewing reorder levels and procurement processes.")
            
            if report['estimated_reorder_cost'] > inventory_value['total_value'] * 0.3:
                report['recommendations'].append("High reorder cost detected. Consider optimizing inventory levels.")
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating reorder report: {e}")
            return {
                'report_date': get_ist_now().isoformat(),
                'total_items_to_reorder': 0,
                'critical_items': 0,
                'high_priority_items': 0,
                'medium_priority_items': 0,
                'estimated_reorder_cost': 0.0,
                'inventory_health_score': 0.0,
                'recommendations': ["Unable to generate report due to data error."]
            }
    
    def _validate_item_data(self, item_data: Dict[str, Any]) -> None:
        """Validate inventory item data"""
        required_fields = ['sku', 'name', 'quantity', 'reorder_level', 'price']
        
        for field in required_fields:
            if field not in item_data or item_data[field] is None:
                raise ValueError(f"Required field missing: {field}")
        
        # Validate SKU format (basic check)
        sku = str(item_data['sku']).strip()
        if not sku or len(sku) < 2:
            raise ValueError("SKU must be at least 2 characters long")
        
        # Validate numeric fields
        try:
            quantity = int(item_data['quantity'])
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")
        except (ValueError, TypeError):
            raise ValueError("Invalid quantity value")
        
        try:
            reorder_level = int(item_data['reorder_level'])
            if reorder_level < 0:
                raise ValueError("Reorder level cannot be negative")
        except (ValueError, TypeError):
            raise ValueError("Invalid reorder level value")
        
        try:
            price = float(item_data['price'])
            if price < 0:
                raise ValueError("Price cannot be negative")
        except (ValueError, TypeError):
            raise ValueError("Invalid price value")
        
        # Validate name
        name = str(item_data['name']).strip()
        if not name or len(name) < 2:
            raise ValueError("Product name must be at least 2 characters long")