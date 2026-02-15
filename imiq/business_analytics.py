#!/usr/bin/env python3
"""
Date-wise Business Analytics Module for CrazyShopperz

This module provides comprehensive date-wise business analytics by fetching data from:
- NewOrders sheet: Order count, amounts, product details
- Revenue sheet: Ad spend, courier expenses
- ProductList sheet: SKU, cost price, selling price details
"""

import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
from imiq.storage import StorageBase


class DateWiseBusinessAnalytics:
    """Comprehensive date-wise business analytics for CrazyShopperz"""
    
    def __init__(self, storage: StorageBase):
        self.storage = storage
    
    def get_orders_by_date(self, target_date: date) -> Dict:
        """
        Get order details for a specific date from NewOrders sheet
        
        Args:
            target_date: Date to fetch orders for
            
        Returns:
            Dict containing order count, total amount, and order details
        """
        try:
            from .performance import get_cached_sheet_data
            orders_df = get_cached_sheet_data(self.storage, "NewOrders")
            
            if orders_df.empty:
                return {
                    'date': target_date.strftime('%Y-%m-%d'),
                    'order_count': 0,
                    'total_amount': 0.0,
                    'orders': []
                }
            
            # Convert timestamp to date for filtering
            orders_df['date'] = pd.to_datetime(orders_df['timestamp'], format='mixed', errors='coerce').dt.date
            
            # Filter orders for target date
            date_orders = orders_df[orders_df['date'] == target_date].copy()
            
            if date_orders.empty:
                return {
                    'date': target_date.strftime('%Y-%m-%d'),
                    'order_count': 0,
                    'total_amount': 0.0,
                    'orders': []
                }
            
            # Calculate metrics
            order_count = len(date_orders)
            total_amount = pd.to_numeric(date_orders['total'], errors='coerce').fillna(0).sum()
            
            # Prepare order details
            order_details = []
            for _, order in date_orders.iterrows():
                order_details.append({
                    'order_id': order.get('order_id', ''),
                    'customer_name': order.get('customer_name', ''),
                    'product': order.get('product', ''),
                    'quantity': pd.to_numeric(order.get('quantity', 0), errors='coerce'),
                    'total': pd.to_numeric(order.get('total', 0), errors='coerce'),
                    'status': order.get('status', ''),
                    'payment_method': order.get('payment_method', ''),
                    'timestamp': order.get('timestamp', '')
                })
            
            return {
                'date': target_date.strftime('%Y-%m-%d'),
                'order_count': order_count,
                'total_amount': round(float(total_amount), 2),
                'orders': order_details
            }
            
        except Exception as e:
            print(f"Error fetching orders for {target_date}: {e}")
            return {
                'date': target_date.strftime('%Y-%m-%d'),
                'order_count': 0,
                'total_amount': 0.0,
                'orders': [],
                'error': str(e)
            }
    
    def get_revenue_data_by_date(self, target_date: date) -> Dict:
        """
        Get revenue data (ad spend, courier expenses) for a specific date
        
        Args:
            target_date: Date to fetch revenue data for
            
        Returns:
            Dict containing ad spend and courier expenses
        """
        try:
            from .performance import get_cached_sheet_data
            revenue_df = get_cached_sheet_data(self.storage, "Revenue")
            
            if revenue_df.empty:
                return {
                    'date': target_date.strftime('%Y-%m-%d'),
                    'ad_spend': 0.0,
                    'courier_expenses': 0.0,
                    'other_expenses': 0.0,
                    'total_expenses': 0.0,
                    'notes': ''
                }
            
            # Convert date column for filtering
            revenue_df['date'] = pd.to_datetime(revenue_df['date'], format='mixed', errors='coerce').dt.date
            
            # Filter for target date
            date_revenue = revenue_df[revenue_df['date'] == target_date]
            
            if date_revenue.empty:
                return {
                    'date': target_date.strftime('%Y-%m-%d'),
                    'ad_spend': 0.0,
                    'courier_expenses': 0.0,
                    'other_expenses': 0.0,
                    'total_expenses': 0.0,
                    'notes': ''
                }
            
            # Sum expenses for the date (in case multiple entries)
            ad_spend = pd.to_numeric(date_revenue['ad_spend'], errors='coerce').fillna(0).sum()
            courier_expenses = pd.to_numeric(date_revenue['courier_expenses'], errors='coerce').fillna(0).sum()
            other_expenses = pd.to_numeric(date_revenue['other_expenses'], errors='coerce').fillna(0).sum()
            total_expenses = ad_spend + courier_expenses + other_expenses
            
            # Get notes (combine if multiple entries)
            notes = ' | '.join(date_revenue['notes'].fillna('').astype(str))
            
            return {
                'date': target_date.strftime('%Y-%m-%d'),
                'ad_spend': round(float(ad_spend), 2),
                'courier_expenses': round(float(courier_expenses), 2),
                'other_expenses': round(float(other_expenses), 2),
                'total_expenses': round(float(total_expenses), 2),
                'notes': notes
            }
            
        except Exception as e:
            print(f"Error fetching revenue data for {target_date}: {e}")
            return {
                'date': target_date.strftime('%Y-%m-%d'),
                'ad_spend': 0.0,
                'courier_expenses': 0.0,
                'other_expenses': 0.0,
                'total_expenses': 0.0,
                'notes': '',
                'error': str(e)
            }
    
    def get_product_details(self) -> Dict[str, Dict]:
        """
        Get product details (SKU, cost price, selling price) from ProductList sheet
        
        Returns:
            Dict with product_name as key and product details as value
        """
        try:
            from .performance import get_cached_sheet_data
            products_df = get_cached_sheet_data(self.storage, "ProductList")
            
            if products_df.empty:
                return {}
            
            product_details = {}
            for _, product in products_df.iterrows():
                product_name = product.get('product_name', '')
                if product_name:
                    product_details[product_name] = {
                        'sku': product.get('sku', ''),
                        'price': pd.to_numeric(product.get('price', 0), errors='coerce'),
                        'description': product.get('description', ''),
                        'stock': pd.to_numeric(product.get('stock', 0), errors='coerce'),
                        'category': product.get('category', ''),
                        'status': product.get('status', ''),
                        'cost_price': pd.to_numeric(product.get('price', 0) * 0.6, errors='coerce')  # Estimated cost price as 60% of selling price
                    }
            
            return product_details
            
        except Exception as e:
            print(f"Error fetching product details: {e}")
            return {}
    
    def get_comprehensive_date_analytics(self, target_date: date) -> Dict:
        """
        Get comprehensive business analytics for a specific date
        
        Args:
            target_date: Date to analyze
            
        Returns:
            Dict containing all business metrics for the date
        """
        try:
            # Get orders data
            orders_data = self.get_orders_by_date(target_date)
            
            # Get revenue data
            revenue_data = self.get_revenue_data_by_date(target_date)
            
            # Get product details
            product_details = self.get_product_details()
            
            # Calculate enhanced metrics
            gross_profit = 0.0
            total_cost = 0.0
            
            for order in orders_data.get('orders', []):
                product_name = order.get('product', '')
                quantity = order.get('quantity', 0)
                
                if product_name in product_details:
                    cost_price = product_details[product_name]['cost_price']
                    total_cost += cost_price * quantity
            
            gross_profit = orders_data['total_amount'] - total_cost
            
            # Calculate net metrics
            net_profit_before_expenses = gross_profit
            net_profit_after_expenses = gross_profit - revenue_data['total_expenses']
            
            # Calculate efficiency metrics
            avg_order_value = (
                orders_data['total_amount'] / orders_data['order_count'] 
                if orders_data['order_count'] > 0 else 0
            )
            
            cost_per_acquisition = (
                revenue_data['ad_spend'] / orders_data['order_count'] 
                if orders_data['order_count'] > 0 else 0
            )
            
            return {
                'date': target_date.strftime('%Y-%m-%d'),
                'orders': orders_data,
                'revenue': revenue_data,
                'product_details': product_details,
                'analytics': {
                    'gross_profit': round(gross_profit, 2),
                    'total_product_cost': round(total_cost, 2),
                    'net_profit_before_expenses': round(net_profit_before_expenses, 2),
                    'net_profit_after_expenses': round(net_profit_after_expenses, 2),
                    'profit_margin_percentage': round(
                        (net_profit_after_expenses / orders_data['total_amount'] * 100) 
                        if orders_data['total_amount'] > 0 else 0, 2
                    ),
                    'avg_order_value': round(avg_order_value, 2),
                    'cost_per_acquisition': round(cost_per_acquisition, 2),
                    'expense_ratio': round(
                        (revenue_data['total_expenses'] / orders_data['total_amount'] * 100)
                        if orders_data['total_amount'] > 0 else 0, 2
                    )
                }
            }
            
        except Exception as e:
            print(f"Error generating comprehensive analytics for {target_date}: {e}")
            return {
                'date': target_date.strftime('%Y-%m-%d'),
                'error': str(e)
            }
    
    def get_date_range_analytics(self, start_date: date, end_date: date) -> Dict:
        """
        Get business analytics for a date range
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            Dict containing aggregated business metrics for the date range
        """
        try:
            analytics_data = []
            current_date = start_date
            
            while current_date <= end_date:
                daily_analytics = self.get_comprehensive_date_analytics(current_date)
                if 'error' not in daily_analytics:
                    analytics_data.append(daily_analytics)
                current_date += timedelta(days=1)
            
            if not analytics_data:
                return {
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d'),
                    'total_days': 0,
                    'analytics': {}
                }
            
            # Aggregate metrics
            total_orders = sum(day['orders']['order_count'] for day in analytics_data)
            total_revenue = sum(day['orders']['total_amount'] for day in analytics_data)
            total_ad_spend = sum(day['revenue']['ad_spend'] for day in analytics_data)
            total_courier_expenses = sum(day['revenue']['courier_expenses'] for day in analytics_data)
            total_other_expenses = sum(day['revenue']['other_expenses'] for day in analytics_data)
            total_expenses = sum(day['revenue']['total_expenses'] for day in analytics_data)
            total_gross_profit = sum(day['analytics']['gross_profit'] for day in analytics_data)
            total_net_profit = sum(day['analytics']['net_profit_after_expenses'] for day in analytics_data)
            
            days_count = len(analytics_data)
            
            return {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'total_days': days_count,
                'daily_data': analytics_data,
                'summary': {
                    'total_orders': total_orders,
                    'total_revenue': round(total_revenue, 2),
                    'total_ad_spend': round(total_ad_spend, 2),
                    'total_courier_expenses': round(total_courier_expenses, 2),
                    'total_other_expenses': round(total_other_expenses, 2),
                    'total_expenses': round(total_expenses, 2),
                    'gross_profit': round(total_gross_profit, 2),
                    'net_profit': round(total_net_profit, 2),
                    'avg_orders_per_day': round(total_orders / days_count, 2) if days_count > 0 else 0,
                    'avg_revenue_per_day': round(total_revenue / days_count, 2) if days_count > 0 else 0,
                    'avg_order_value': round(total_revenue / total_orders, 2) if total_orders > 0 else 0,
                    'overall_cpa': round(total_ad_spend / total_orders, 2) if total_orders > 0 else 0,
                    'profit_margin': round((total_net_profit / total_revenue * 100), 2) if total_revenue > 0 else 0
                }
            }
            
        except Exception as e:
            print(f"Error generating date range analytics: {e}")
            return {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'error': str(e)
            }
    
    def add_revenue_entry(self, target_date: date, ad_spend: float, courier_expenses: float, 
                         other_expenses: float = 0.0, notes: str = "", created_by: str = "") -> bool:
        """
        Add a revenue entry to the Revenue sheet
        
        Args:
            target_date: Date for the revenue entry
            ad_spend: Ad spend amount
            courier_expenses: Courier expenses amount
            other_expenses: Other expenses amount
            notes: Optional notes
            created_by: User who created the entry
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            revenue_entry = {
                'date': target_date.strftime('%Y-%m-%d'),
                'ad_spend': round(float(ad_spend), 2),
                'courier_expenses': round(float(courier_expenses), 2),
                'other_expenses': round(float(other_expenses), 2),
                'notes': notes,
                'created_by': created_by,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.storage.append_row("Revenue", revenue_entry)
            return True
            
        except Exception as e:
            print(f"Error adding revenue entry: {e}")
            return False


def get_business_analytics_instance(storage: StorageBase) -> DateWiseBusinessAnalytics:
    """Factory function to create DateWiseBusinessAnalytics instance"""
    return DateWiseBusinessAnalytics(storage)