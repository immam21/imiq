"""
IMIQ Shipments Service
Handles shipment creation, tracking, and courier integration
"""

import pandas as pd
from typing import Dict, Any, List, Optional
import logging
import json

from .storage import StorageBase
from .utils import get_ist_now, generate_id

logger = logging.getLogger(__name__)

class ShipmentService:
    """Service for managing shipments and courier integrations"""
    
    def __init__(self, storage: StorageBase):
        self.storage = storage
    
    def create_shipment(self, shipment_data: Dict[str, Any]) -> str:
        """Create a new shipment and update corresponding order"""
        try:
            # Generate shipment ID
            shipment_id = f"SHIP-{generate_id()}"
            
            # Validate order exists
            order_id = shipment_data['order_id']
            orders_df = self.storage.read_sheet("NewOrders")
            
            if orders_df.empty or order_id not in orders_df['order_id'].values:
                raise ValueError(f"Order {order_id} not found")
            
            # Prepare complete shipment data
            complete_shipment_data = {
                'shipment_id': shipment_id,
                'order_id': order_id,
                'courier': shipment_data['courier'],
                'tracking_id': shipment_data['tracking_id'],
                'status': shipment_data.get('status', 'Shipped'),
                'created_at': get_ist_now().isoformat(),
                'updated_at': get_ist_now().isoformat()
            }
            
            # Validate shipment data
            self._validate_shipment_data(complete_shipment_data)
            
            # Save shipment
            self.storage.append_row("Shipments", complete_shipment_data)
            
            # Update corresponding order with tracking information
            self._update_order_with_tracking(
                order_id, 
                shipment_data['tracking_id'], 
                shipment_data['courier']
            )
            
            logger.info(f"Shipment created: {shipment_id} for order {order_id}")
            return shipment_id
            
        except Exception as e:
            logger.error(f"Error creating shipment: {e}")
            raise
    
    def get_shipment_by_id(self, shipment_id: str) -> Optional[pd.Series]:
        """Get a specific shipment by ID"""
        try:
            shipments_df = self.storage.read_sheet("Shipments")
            
            if shipments_df.empty:
                return None
            
            matching_shipments = shipments_df[shipments_df['shipment_id'] == shipment_id]
            
            if matching_shipments.empty:
                return None
            
            return matching_shipments.iloc[0]
            
        except Exception as e:
            logger.error(f"Error retrieving shipment {shipment_id}: {e}")
            return None
    
    def get_shipment_by_order(self, order_id: str) -> Optional[pd.Series]:
        """Get shipment information for a specific order"""
        try:
            shipments_df = self.storage.read_sheet("Shipments")
            
            if shipments_df.empty:
                return None
            
            matching_shipments = shipments_df[shipments_df['order_id'] == order_id]
            
            if matching_shipments.empty:
                return None
            
            # Return most recent shipment if multiple exist
            matching_shipments['created_at'] = pd.to_datetime(matching_shipments['created_at'])
            return matching_shipments.sort_values('created_at', ascending=False).iloc[0]
            
        except Exception as e:
            logger.error(f"Error retrieving shipment for order {order_id}: {e}")
            return None
    
    def get_all_shipments(self) -> pd.DataFrame:
        """Get all shipments with sorting"""
        try:
            shipments_df = self.storage.read_sheet("Shipments")
            
            if not shipments_df.empty and 'created_at' in shipments_df.columns:
                shipments_df['created_at'] = pd.to_datetime(shipments_df['created_at'])
                shipments_df = shipments_df.sort_values('created_at', ascending=False)
            
            return shipments_df
            
        except Exception as e:
            logger.error(f"Error retrieving all shipments: {e}")
            return pd.DataFrame()
    
    def get_orders_without_shipments(self) -> pd.DataFrame:
        """Get orders that don't have shipments yet"""
        try:
            orders_df = self.storage.read_sheet("NewOrders")
            shipments_df = self.storage.read_sheet("Shipments")
            
            if orders_df.empty:
                return pd.DataFrame()
            
            # Get order IDs that already have shipments
            shipped_order_ids = set()
            if not shipments_df.empty and 'order_id' in shipments_df.columns:
                shipped_order_ids = set(shipments_df['order_id'].unique())
            
            # Filter orders without shipments
            unshipped_orders = orders_df[~orders_df['order_id'].isin(shipped_order_ids)].copy()
            
            # Exclude cancelled and returned orders
            if 'status' in unshipped_orders.columns:
                unshipped_orders = unshipped_orders[
                    ~unshipped_orders['status'].isin(['Cancelled', 'Returned'])
                ]
            
            return unshipped_orders
            
        except Exception as e:
            logger.error(f"Error retrieving orders without shipments: {e}")
            return pd.DataFrame()
    
    def update_shipment_status(self, shipment_id: str, new_status: str) -> bool:
        """Update shipment status"""
        try:
            valid_statuses = ['Shipped', 'In Transit', 'Out for Delivery', 'Delivered', 'Failed Delivery', 'Returned']
            
            if new_status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
            
            def filter_fn(row):
                return row['shipment_id'] == shipment_id
            
            def update_fn(row):
                row['status'] = new_status
                row['updated_at'] = get_ist_now().isoformat()
                return row
            
            updated_count = self.storage.update_rows("Shipments", filter_fn, update_fn)
            
            if updated_count > 0:
                # Also update the corresponding order status if delivered
                if new_status == 'Delivered':
                    shipment = self.get_shipment_by_id(shipment_id)
                    if shipment is not None:
                        self._update_order_status(shipment['order_id'], 'Delivered')
                
                logger.info(f"Shipment {shipment_id} status updated to {new_status}")
                return True
            else:
                logger.warning(f"Shipment {shipment_id} not found for status update")
                return False
            
        except Exception as e:
            logger.error(f"Error updating shipment status {shipment_id}: {e}")
            raise
    
    def search_shipments(self, search_term: str, search_field: str = "All") -> pd.DataFrame:
        """Search shipments by various criteria"""
        try:
            shipments_df = self.get_all_shipments()
            
            if shipments_df.empty or not search_term:
                return shipments_df
            
            search_term = search_term.lower().strip()
            
            if search_field == "All":
                # Search across all text fields
                text_columns = ['shipment_id', 'order_id', 'courier', 'tracking_id', 'status']
                mask = pd.Series([False] * len(shipments_df))
                
                for col in text_columns:
                    if col in shipments_df.columns:
                        mask |= shipments_df[col].astype(str).str.lower().str.contains(search_term, na=False)
                
                shipments_df = shipments_df[mask]
                
            elif search_field in ['shipment_id', 'order_id', 'tracking_id']:
                # Exact match for IDs
                shipments_df = shipments_df[
                    shipments_df[search_field].astype(str).str.lower() == search_term
                ]
                
            elif search_field in shipments_df.columns:
                # Partial match for other fields
                shipments_df = shipments_df[
                    shipments_df[search_field].astype(str).str.lower().str.contains(search_term, na=False)
                ]
            
            return shipments_df
            
        except Exception as e:
            logger.error(f"Error searching shipments: {e}")
            return pd.DataFrame()
    
    def get_shipment_statistics(self) -> Dict[str, Any]:
        """Get shipment statistics and analytics"""
        try:
            shipments_df = self.get_all_shipments()
            
            if shipments_df.empty:
                return {
                    'total_shipments': 0,
                    'status_breakdown': {},
                    'courier_breakdown': {},
                    'average_delivery_time': 0.0,
                    'delivery_success_rate': 0.0
                }
            
            stats = {
                'total_shipments': len(shipments_df),
                'status_breakdown': {},
                'courier_breakdown': {},
                'average_delivery_time': 0.0,
                'delivery_success_rate': 0.0
            }
            
            # Status breakdown
            if 'status' in shipments_df.columns:
                status_counts = shipments_df['status'].value_counts().to_dict()
                stats['status_breakdown'] = {k: int(v) for k, v in status_counts.items()}
            
            # Courier breakdown
            if 'courier' in shipments_df.columns:
                courier_counts = shipments_df['courier'].value_counts().to_dict()
                stats['courier_breakdown'] = {k: int(v) for k, v in courier_counts.items()}
            
            # Delivery success rate
            total_shipments = len(shipments_df)
            delivered_shipments = len(shipments_df[shipments_df['status'] == 'Delivered']) if 'status' in shipments_df.columns else 0
            stats['delivery_success_rate'] = round((delivered_shipments / total_shipments * 100), 1) if total_shipments > 0 else 0.0
            
            # Average delivery time (placeholder - would need more detailed tracking)
            # In a real implementation, you'd calculate based on ship date vs delivery date
            stats['average_delivery_time'] = 3.5  # Placeholder: 3.5 days average
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating shipment statistics: {e}")
            return {
                'total_shipments': 0,
                'status_breakdown': {},
                'courier_breakdown': {},
                'average_delivery_time': 0.0,
                'delivery_success_rate': 0.0
            }
    
    def prepare_dtdc_api_payload(self, shipment_id: str) -> Dict[str, Any]:
        """Prepare API payload for DTDC courier integration"""
        try:
            shipment = self.get_shipment_by_id(shipment_id)
            if shipment is None:
                raise ValueError(f"Shipment {shipment_id} not found")
            
            # Get order details for shipping address
            orders_df = self.storage.read_sheet("NewOrders")
            order = orders_df[orders_df['order_id'] == shipment['order_id']].iloc[0]
            
            # Prepare DTDC API payload (example structure)
            payload = {
                "consignment_number": shipment['tracking_id'],
                "pickup_address": {
                    "name": "IMIQ Warehouse",
                    "address": "Warehouse Address Line 1",
                    "city": "City",
                    "state": "State",
                    "pincode": "123456",
                    "phone": "1234567890"
                },
                "delivery_address": {
                    "name": order['customer_name'],
                    "address": "Customer Address (to be filled)",
                    "city": "Customer City",
                    "state": "Customer State", 
                    "pincode": "000000",
                    "phone": "0000000000"
                },
                "product_details": {
                    "description": order['product'],
                    "weight": "1.0",  # Default weight in kg
                    "dimensions": {
                        "length": "10",
                        "breadth": "10", 
                        "height": "10"
                    }
                },
                "service_type": "Standard",
                "payment_mode": "PPD"  # Pre-paid
            }
            
            logger.info(f"DTDC API payload prepared for shipment {shipment_id}")
            
            # TODO: Implement actual API call
            # response = requests.post("https://api.dtdc.com/v1/shipments", json=payload, headers=headers)
            
            return payload
            
        except Exception as e:
            logger.error(f"Error preparing DTDC payload for {shipment_id}: {e}")
            raise
    
    def prepare_delhivery_api_payload(self, shipment_id: str) -> Dict[str, Any]:
        """Prepare API payload for Delhivery courier integration"""
        try:
            shipment = self.get_shipment_by_id(shipment_id)
            if shipment is None:
                raise ValueError(f"Shipment {shipment_id} not found")
            
            # Get order details
            orders_df = self.storage.read_sheet("NewOrders")
            order = orders_df[orders_df['order_id'] == shipment['order_id']].iloc[0]
            
            # Prepare Delhivery API payload (example structure)
            payload = {
                "shipments": [
                    {
                        "name": order['customer_name'],
                        "add": "Customer Address (to be filled)",
                        "pin": "000000",
                        "city": "Customer City",
                        "state": "Customer State",
                        "country": "India",
                        "phone": "0000000000",
                        "order": shipment['tracking_id'],
                        "payment_mode": "Prepaid",
                        "return_pin": "123456",
                        "return_city": "Return City",
                        "return_phone": "1234567890",
                        "return_add": "Return Address",
                        "return_state": "Return State",
                        "return_country": "India",
                        "products_desc": order['product'],
                        "hsn_code": "",
                        "cod_amount": "0",
                        "order_date": order['created_at'],
                        "total_amount": str(order['price']),
                        "seller_add": "Seller Address",
                        "seller_name": "IMIQ",
                        "seller_inv": "",
                        "quantity": str(order['quantity']),
                        "waybill": "",
                        "shipment_width": "10",
                        "shipment_height": "10",
                        "weight": "1",
                        "seller_gst_tin": "",
                        "shipping_mode": "Surface",
                        "address_type": "home"
                    }
                ]
            }
            
            logger.info(f"Delhivery API payload prepared for shipment {shipment_id}")
            
            # TODO: Implement actual API call
            # headers = {"Authorization": "Token your_delhivery_token"}
            # response = requests.post("https://track.delhivery.com/api/cmu/create.json", data={"format": "json", "data": json.dumps(payload)}, headers=headers)
            
            return payload
            
        except Exception as e:
            logger.error(f"Error preparing Delhivery payload for {shipment_id}: {e}")
            raise
    
    def get_tracking_info(self, tracking_id: str, courier: str) -> Dict[str, Any]:
        """Get tracking information from courier API (placeholder)"""
        try:
            # Placeholder tracking information
            # In a real implementation, you would call the courier's tracking API
            
            tracking_info = {
                "tracking_id": tracking_id,
                "courier": courier,
                "status": "In Transit",
                "last_updated": get_ist_now().isoformat(),
                "tracking_events": [
                    {
                        "timestamp": get_ist_now().isoformat(),
                        "status": "Shipped",
                        "location": "Origin Hub",
                        "description": "Package dispatched from origin"
                    },
                    {
                        "timestamp": get_ist_now().isoformat(),
                        "status": "In Transit",
                        "location": "Transit Hub",
                        "description": "Package in transit"
                    }
                ],
                "estimated_delivery": None
            }
            
            # TODO: Implement actual courier API calls
            # if courier.lower() == "dtdc":
            #     response = requests.get(f"https://api.dtdc.com/v1/tracking/{tracking_id}")
            # elif courier.lower() == "delhivery":
            #     response = requests.get(f"https://track.delhivery.com/api/v1/packages/json/?waybill={tracking_id}")
            
            logger.info(f"Tracking info retrieved for {tracking_id} via {courier}")
            return tracking_info
            
        except Exception as e:
            logger.error(f"Error retrieving tracking info for {tracking_id}: {e}")
            return {
                "tracking_id": tracking_id,
                "courier": courier,
                "status": "Unknown",
                "error": str(e)
            }
    
    def _update_order_with_tracking(self, order_id: str, tracking_id: str, courier_name: str) -> None:
        """Update order with tracking information"""
        try:
            def filter_fn(row):
                return row['order_id'] == order_id
            
            def update_fn(row):
                row['tracking_id'] = tracking_id
                row['courier_name'] = courier_name
                row['status'] = 'Shipped'
                return row
            
            self.storage.update_rows("NewOrders", filter_fn, update_fn)
            logger.info(f"Order {order_id} updated with tracking info")
            
        except Exception as e:
            logger.error(f"Error updating order {order_id} with tracking: {e}")
            raise
    
    def _update_order_status(self, order_id: str, status: str) -> None:
        """Update order status"""
        try:
            def filter_fn(row):
                return row['order_id'] == order_id
            
            def update_fn(row):
                row['status'] = status
                return row
            
            self.storage.update_rows("NewOrders", filter_fn, update_fn)
            logger.info(f"Order {order_id} status updated to {status}")
            
        except Exception as e:
            logger.error(f"Error updating order {order_id} status: {e}")
    
    def _validate_shipment_data(self, shipment_data: Dict[str, Any]) -> None:
        """Validate shipment data"""
        required_fields = ['shipment_id', 'order_id', 'courier', 'tracking_id', 'status']
        
        for field in required_fields:
            if field not in shipment_data or not shipment_data[field]:
                raise ValueError(f"Required field missing: {field}")
        
        # Validate courier
        valid_couriers = ['DTDC', 'Delhivery', 'Blue Dart', 'Other']
        if shipment_data['courier'] not in valid_couriers:
            logger.warning(f"Courier '{shipment_data['courier']}' not in standard list: {valid_couriers}")
        
        # Validate status
        valid_statuses = ['Shipped', 'In Transit', 'Out for Delivery', 'Delivered', 'Failed Delivery', 'Returned']
        if shipment_data['status'] not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        
        # Validate tracking ID format (basic check)
        tracking_id = str(shipment_data['tracking_id']).strip()
        if len(tracking_id) < 5:
            raise ValueError("Tracking ID must be at least 5 characters long")