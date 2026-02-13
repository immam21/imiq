#!/usr/bin/env python3
"""Test the KPI calculator function"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import compute_kpis

def test_kpi_calculator():
    """Test the KPI calculator with sample data"""
    print("🧮 Testing KPI Calculator...")
    
    # Test data
    test_data = {
        'days': 4,
        'ad_spend_per_day': 1750.0,
        'courier_per_day': 1000.0,
        'sourcing_payment': 40000.0,
        'salary_per_person_per_week': 1500.0,
        'num_employees': 2,
        'orders': 58,
        'total_order_value': 56313.0,
        'cod_return_rate': 0.2,
        'sku_mix': [
            {'sku': 'A', 'units': 30, 'product_cost': 800.0, 'selling_price': 1299.0},
            {'sku': 'B', 'units': 28, 'product_cost': 400.0, 'selling_price': 899.0}
        ]
    }
    
    try:
        result = compute_kpis(test_data)
        print("✅ KPI Calculation Successful!")
        print(f"📈 Total Revenue: ₹{result['total_revenue']:,.2f}")
        print(f"💰 Net Profit: ₹{result['net_profit_after_sourcing']:,.2f}")
        print(f"📊 Gross Margin: {result['gross_margin_percentage']:.1f}%")
        print(f"🎯 CPA: ₹{result['cpa']:,.2f}")
        print(f"📦 Delivered Orders: {result['delivered_orders']}")
        print(f"📅 Monthly Projected Revenue: ₹{result['monthly_projected_revenue']:,.2f}")
        print(f"⚖️ Break-even Orders: {result['break_even_orders']}")
        return True
    except Exception as e:
        print(f"❌ KPI Calculation Failed: {e}")
        return False

if __name__ == "__main__":
    test_kpi_calculator()