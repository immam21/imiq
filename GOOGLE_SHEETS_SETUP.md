"""
Google Sheets Setup Guide for IMIQ
Instructions for integrating Google Sheets as storage backend
"""

# Step-by-step Google Sheets Integration Setup

## Prerequisites
1. Google Cloud Account
2. Google Sheets document with same structure as CZ_MasterSheet.xlsx

## Setup Steps

### 1. Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Create new project or select existing one
3. Enable Google Sheets API and Google Drive API

### 2. Create Service Account
1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Give it a name like "imiq-sheets-service"
4. Grant "Editor" role
5. Click "Done"

### 3. Generate Credentials
1. Click on your service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create New Key"
4. Choose JSON format
5. Download the JSON file

### 4. Share Google Sheet
1. Open your Google Sheet
2. Click "Share" button
3. Add the service account email (from the JSON file)
4. Give "Editor" permissions

### 5. Configure Environment
1. Place the JSON file in your project directory
2. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
   ```

### 6. Enable in IMIQ Settings
1. Login as admin
2. Go to Settings page
3. Check "Enable Google Sheets Integration"
4. Enter your Google Sheet ID
5. Save settings

## Finding Google Sheet ID
From URL: https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
Copy the SHEET_ID_HERE part

## Required Sheet Structure
Your Google Sheet must have these sheets with exact column names:
- Users: user_id, email, password_hash, plain_password, role, name, created_at, is_active
- NewOrders: order_id, phone, customer_name, product, quantity, balance_to_pay, advance_paid, total, address, city, pincode, payment_method, status, timestamp, ai_order_id, tracking_id, courier_name, created_by, advance_screenshot, PICKUP LOCATION, Remarks, Last Update Date
- Customers: customer_id, phone, name, email, address, city, pincode, created_at
- ProductList: product_name, price, description, stock, category, sku, status, image_url
- ChatLogs: message_id, phone, message, direction, timestamp, assigned_user, source, message_id_dup, status, timestamp_dup, ai_attempted, ai_success, failure_reason
- ChatAssignments: phone, assigned_user, assigned_at, status

## Troubleshooting
- Check service account has access to the sheet
- Verify JSON credentials path is correct
- Ensure all required sheets exist in Google Sheets
- Check internet connectivity
- Verify Google Sheets API quota limits