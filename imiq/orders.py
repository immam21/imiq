"""
IMIQ Orders Service
Handles order creation, retrieval, search, and management functionality
"""

import pandas as pd
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Union
import logging

from .storage import StorageBase
from .utils import get_ist_now, generate_id

logger = logging.getLogger(__name__)

class OrderService:
    """Service for managing orders in the IMIQ system"""
    
    def __init__(self, storage: StorageBase):
        self.storage = storage
    
    def create_order(self, order_data: Dict[str, Any]) -> bool:
        """Create a new order with auto-generated ID and timestamp"""
        try:
            # Use provided order_id or generate one
            order_id = order_data.get('order_id', f"ORD{generate_id('', 6)}")
            
            # Prepare complete order data matching CZ_MasterSheet schema
            complete_order_data = {
                'order_id': order_id,
                'phone': order_data.get('phone', ''),
                'customer_name': order_data.get('customer_name', ''),
                'product': order_data.get('product', ''),
                'quantity': int(order_data.get('quantity', 1)),
                'balance_to_pay': float(order_data.get('balance_to_pay', 0)),
                'advance_paid': float(order_data.get('advance_paid', 0)),
                'total': float(order_data.get('total', 0)),
                'address': order_data.get('address', ''),
                'city': order_data.get('city', ''),
                'pincode': order_data.get('pincode', ''),
                'payment_method': order_data.get('payment_method', 'COD'),
                'status': order_data.get('status', 'Pending'),
                'timestamp': order_data.get('timestamp', get_ist_now().isoformat()),
                'ai_order_id': order_data.get('ai_order_id', ''),
                'tracking_id': order_data.get('tracking_id', ''),
                'courier_name': order_data.get('courier_name', ''),
                'created_by': order_data.get('created_by', 'system'),
                'advance_screenshot': order_data.get('advance_screenshot', 'No'),
                'PICKUP LOCATION': order_data.get('PICKUP LOCATION', ''),
                'Remarks': order_data.get('Remarks', ''),
                'Last Update Date': order_data.get('Last Update Date', get_ist_now().strftime('%Y-%m-%d %H:%M:%S'))
            }
            
            # Validate required fields
            self._validate_order_data(complete_order_data)
            
            # Save to storage
            self.storage.append_row("NewOrders", complete_order_data)
            
            logger.info(f"Order created: {order_id} for customer {complete_order_data.get('customer_name', 'Unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return False
    
    def get_order_by_id(self, order_id: str) -> Optional[pd.Series]:
        """Retrieve a specific order by ID"""
        try:
            orders_df = self.storage.read_sheet("NewOrders")
            
            if orders_df.empty:
                return None
            
            matching_orders = orders_df[orders_df['order_id'] == order_id]
            
            if matching_orders.empty:
                return None
            
            return matching_orders.iloc[0]
            
        except Exception as e:
            logger.error(f"Error retrieving order {order_id}: {e}")
            return None
    
    def get_user_orders(self, user_id: str) -> pd.DataFrame:
        """Get all orders for a specific user"""
        try:
            orders_df = self.storage.read_sheet("NewOrders")
            
            if orders_df.empty or 'created_by' not in orders_df.columns:
                return pd.DataFrame()
            
            user_orders = orders_df[orders_df['created_by'] == user_id].copy()
            
            # Sort by timestamp, newest first
            if 'timestamp' in user_orders.columns:
                user_orders['timestamp'] = pd.to_datetime(user_orders['timestamp'])
                user_orders = user_orders.sort_values('timestamp', ascending=False)
            
            return user_orders
            
        except Exception as e:
            logger.error(f"Error retrieving orders for user {user_id}: {e}")
            return pd.DataFrame()
    
    def get_all_orders(self) -> pd.DataFrame:
        """Get all orders (admin function)"""
        try:
            orders_df = self.storage.read_sheet("NewOrders")
            logger.info(f"Raw orders retrieved: {len(orders_df)} rows")
            
            if not orders_df.empty and 'timestamp' in orders_df.columns:
                # Handle different datetime formats more flexibly
                try:
                    # Parse with UTC=True to handle mixed timezones
                    orders_df['timestamp'] = pd.to_datetime(orders_df['timestamp'], format='mixed', utc=True)
                    logger.info("Timestamp parsing successful with format='mixed' and utc=True")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Mixed format with UTC failed: {e}")
                    try:
                        # Try without timezone handling first
                        orders_df['timestamp'] = pd.to_datetime(orders_df['timestamp'], errors='coerce')
                        logger.info("Timestamp parsing successful with errors='coerce'")
                        
                        # Convert to timezone-naive if needed to avoid comparison issues
                        if orders_df['timestamp'].dt.tz is not None:
                            orders_df['timestamp'] = orders_df['timestamp'].dt.tz_localize(None)
                            
                    except Exception as e2:
                        logger.error(f"All timestamp parsing failed: {e2}")
                        # Remove timestamp column to avoid sorting issues
                        orders_df = orders_df.drop(columns=['timestamp'], errors='ignore')
                
                # Sort by timestamp if parsing was successful
                if 'timestamp' in orders_df.columns and orders_df['timestamp'].notna().any():
                    try:
                        orders_df = orders_df.sort_values('timestamp', ascending=False)
                        logger.info("Orders sorted by timestamp")
                    except Exception as sort_error:
                        logger.warning(f"Sorting failed: {sort_error}, skipping sort")
            
            logger.info(f"Final orders count: {len(orders_df)}")
            return orders_df
            
        except Exception as e:
            logger.error(f"Error retrieving all orders: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return pd.DataFrame()
    
    def search_orders(self, search_term: str, search_field: str = "All", 
                     date_range: List[date] = None, user_id: Optional[str] = None) -> pd.DataFrame:
        """Search orders with flexible criteria"""
        try:
            # Get base orders dataset
            if user_id:
                orders_df = self.get_user_orders(user_id)
            else:
                orders_df = self.get_all_orders()
            
            if orders_df.empty:
                return pd.DataFrame()
            
            # Apply date filter if provided
            if date_range and len(date_range) >= 2:
                start_date, end_date = date_range[0], date_range[-1]
                orders_df['timestamp'] = pd.to_datetime(orders_df['timestamp'])
                orders_df = orders_df[
                    (orders_df['timestamp'].dt.date >= start_date) & 
                    (orders_df['timestamp'].dt.date <= end_date)
                ]
            
            # Apply text search if term provided
            if search_term:
                search_term = search_term.lower().strip()
                
                if search_field == "All":
                    # Search across all text fields
                    text_columns = ['order_id', 'customer_name', 'product', 'status', 'phone']
                    mask = pd.Series([False] * len(orders_df))
                    
                    for col in text_columns:
                        if col in orders_df.columns:
                            mask |= orders_df[col].astype(str).str.lower().str.contains(search_term, na=False)
                    
                    orders_df = orders_df[mask]
                    
                elif search_field == "order_id":
                    # Exact match for order ID
                    orders_df = orders_df[orders_df['order_id'].str.lower() == search_term]
                    
                elif search_field in orders_df.columns:
                    # Search in specific field
                    orders_df = orders_df[
                        orders_df[search_field].astype(str).str.lower().str.contains(search_term, na=False)
                    ]
                else:
                    logger.warning(f"Search field '{search_field}' not found in orders")
                    return pd.DataFrame()
            
            return orders_df
            
        except Exception as e:
            logger.error(f"Error searching orders: {e}")
            return pd.DataFrame()
    
    def update_order(self, order_id: str, update_data: Dict[str, Any]) -> bool:
        """Update an existing order"""
        try:
            def filter_fn(row):
                return row['order_id'] == order_id
            
            def update_fn(row):
                # Only update allowed fields
                allowed_fields = ['customer_name', 'customer_email', 'product', 
                                'quantity', 'price', 'status', 'lead_id', 
                                'tracking_id', 'courier_name']
                
                for field, value in update_data.items():
                    if field in allowed_fields:
                        row[field] = value
                
                return row
            
            updated_count = self.storage.update_rows("NewOrders", filter_fn, update_fn)
            
            if updated_count > 0:
                logger.info(f"Order {order_id} updated successfully")
                return True
            else:
                logger.warning(f"Order {order_id} not found for update")
                return False
            
        except Exception as e:
            logger.error(f"Error updating order {order_id}: {e}")
            raise
    
    def update_order_status(self, order_id: str, new_status: str) -> bool:
        """Update order status"""
        valid_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Returned']
        
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        
        return self.update_order(order_id, {'status': new_status})
    
    def add_tracking_info(self, order_id: str, tracking_id: str, courier_name: str) -> bool:
        """Add tracking information to an order (typically called from shipment service)"""
        try:
            update_data = {
                'tracking_id': tracking_id,
                'courier_name': courier_name,
                'status': 'Shipped'  # Automatically update status when tracking is added
            }
            
            return self.update_order(order_id, update_data)
            
        except Exception as e:
            logger.error(f"Error adding tracking info to order {order_id}: {e}")
            raise
    
    def get_orders_by_status(self, status: str, user_id: Optional[str] = None) -> pd.DataFrame:
        """Get orders filtered by status"""
        try:
            if user_id:
                orders_df = self.get_user_orders(user_id)
            else:
                orders_df = self.get_all_orders()
            
            if orders_df.empty or 'status' not in orders_df.columns:
                return pd.DataFrame()
            
            return orders_df[orders_df['status'] == status]
            
        except Exception as e:
            logger.error(f"Error retrieving orders by status {status}: {e}")
            return pd.DataFrame()
    
    def get_orders_without_tracking(self) -> pd.DataFrame:
        """Get orders that don't have tracking information yet"""
        try:
            orders_df = self.get_all_orders()
            
            if orders_df.empty:
                return pd.DataFrame()
            
            # Orders without tracking ID or with empty tracking ID
            no_tracking = orders_df[
                (orders_df['tracking_id'].isna()) | 
                (orders_df['tracking_id'] == '') |
                (orders_df['tracking_id'].str.strip() == '')
            ]
            
            # Exclude cancelled and returned orders
            if 'status' in no_tracking.columns:
                no_tracking = no_tracking[
                    ~no_tracking['status'].isin(['Cancelled', 'Returned'])
                ]
            
            return no_tracking
            
        except Exception as e:
            logger.error(f"Error retrieving orders without tracking: {e}")
            return pd.DataFrame()
    
    def delete_order(self, order_id: str) -> bool:
        """Delete an order (admin only - use with caution)"""
        try:
            orders_df = self.storage.read_sheet("NewOrders")
            
            if orders_df.empty:
                return False
            
            # Remove the order
            filtered_df = orders_df[orders_df['order_id'] != order_id]
            
            # Check if any row was actually removed
            if len(filtered_df) == len(orders_df):
                logger.warning(f"Order {order_id} not found for deletion")
                return False
            
            # Replace the sheet with filtered data
            self.storage.replace_sheet("NewOrders", filtered_df)
            
            logger.info(f"Order {order_id} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting order {order_id}: {e}")
            raise
    
    def get_order_statistics(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get statistical summary of orders"""
        try:
            if user_id:
                orders_df = self.get_user_orders(user_id)
            else:
                orders_df = self.get_all_orders()
            
            if orders_df.empty:
                return {
                    'total_orders': 0,
                    'total_revenue': 0.0,
                    'average_order_value': 0.0,
                    'status_breakdown': {},
                    'top_products': [],
                    'top_customers': []
                }
            
            # Basic statistics
            stats = {
                'total_orders': len(orders_df),
                'total_revenue': 0.0,
                'average_order_value': 0.0,
                'status_breakdown': {},
                'top_products': [],
                'top_customers': []
            }
            
            # Revenue calculations
            if 'price' in orders_df.columns:
                orders_df['price'] = pd.to_numeric(orders_df['price'], errors='coerce').fillna(0)
                stats['total_revenue'] = float(orders_df['price'].sum())
                stats['average_order_value'] = float(orders_df['price'].mean())
            
            # Status breakdown
            if 'status' in orders_df.columns:
                status_counts = orders_df['status'].value_counts().to_dict()
                stats['status_breakdown'] = {k: int(v) for k, v in status_counts.items()}
            
            # Top products
            if 'product' in orders_df.columns:
                product_counts = orders_df['product'].value_counts().head(5).to_dict()
                stats['top_products'] = [{'product': k, 'count': int(v)} for k, v in product_counts.items()]
            
            # Top customers
            if 'customer_name' in orders_df.columns:
                customer_counts = orders_df['customer_name'].value_counts().head(5).to_dict()
                stats['top_customers'] = [{'customer': k, 'count': int(v)} for k, v in customer_counts.items()]
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating order statistics: {e}")
            return {
                'total_orders': 0,
                'total_revenue': 0.0,
                'average_order_value': 0.0,
                'status_breakdown': {},
                'top_products': [],
                'top_customers': []
            }
    
    def _validate_order_data(self, order_data: Dict[str, Any]) -> None:
        """Validate order data before creation"""
        required_fields = ['order_id', 'customer_name', 'product']
        
        for field in required_fields:
            if field not in order_data or not order_data[field]:
                raise ValueError(f"Required field missing: {field}")
        
        # Validate phone format if provided
        if 'phone' in order_data and order_data['phone']:
            phone = str(order_data['phone']).strip()
            if phone and len(phone) < 10:
                raise ValueError("Phone number must be at least 10 digits")
        
        # Validate numeric fields
        if 'quantity' in order_data:
            try:
                quantity = int(order_data['quantity'])
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except (ValueError, TypeError):
                raise ValueError("Invalid quantity value")
        
        if 'total' in order_data:
            try:
                total = float(order_data['total'])
                if total < 0:
                    raise ValueError("Total cannot be negative")
            except (ValueError, TypeError):
                raise ValueError("Invalid total value")