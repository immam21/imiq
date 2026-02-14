# 🚀 IMIQ - Intelligent Order Management System

> **Live Demo**: [Deploy to Streamlit Cloud](https://share.streamlit.io) | **Status**: ✅ Ready for Deployment

A comprehensive order management and e-commerce solution with real-time analytics, inventory management, and secure user authentication.

## ✨ Key Features

- **📊 Real-time Dashboard**: Interactive KPIs and business analytics
- **👥 Secure Authentication**: Role-based access with bcrypt encryption  
- **📦 Order Management**: Complete order lifecycle tracking
- **📈 Inventory Control**: Stock management with automated alerts
- **🚚 Shipment Tracking**: Courier integration ready
- **📱 Modern UI**: Responsive design with dark theme
- **☁️ Cloud Ready**: Optimized for Streamlit Cloud deployment

## 🌟 Live Demo & Test Accounts

**Test the app locally**:
```bash
streamlit run app.py
```

**Test Credentials**:
- **Admin**: `admin@test.com` / `admin123` 
- **User**: Create new account via signup form

## 🚀 One-Click Cloud Deployment

### Deploy to Streamlit Cloud:

1. **Fork this repository**
2. **Visit** [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub** and select this repository
4. **Main file**: `app.py`
5. **Click Deploy!**

Your app will be live at: `https://your-app-name.streamlit.app`

## 📊 Dashboard Highlights

| Feature | Description |
|---------|-------------|
| 📈 KPI Analytics | Real-time orders, revenue, growth metrics |
| 📋 Order Management | Create, track, and manage orders |
| 📦 Inventory Control | Stock levels with low-stock alerts |
| 👥 User Management | Secure authentication & role-based access |
| 📊 Interactive Charts | Plotly visualizations for business insights |
| 🔒 Security | bcrypt hashing, session management |

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run app.py
   ```

3. **Initial Setup**
   - On first run, IMIQ will create `data/db.xlsx` with required sheets
   - Default admin account: email=`admin@imiq.com`, password=`admin123`
   - Create additional user accounts through the signup page

## Data Schemas

### Users Sheet
- email, userid, password_hash, role, created_at

### NewOrders Sheet  
- order_id, created_at, user_id, customer_name, customer_email, product, quantity, price, status, lead_id, tracking_id, courier_name

### Shipments Sheet
- shipment_id, order_id, courier, tracking_id, status, created_at, updated_at

### Inventory Sheet
- sku, name, quantity, reorder_level, price

## Features

- **Role-Based Access**: Admin and User roles with different permissions
- **Order Management**: Complete CRUD operations for orders
- **Inventory Tracking**: Stock management with reorder alerts
- **Shipment Tracking**: Integration-ready courier management
- **KPI Dashboards**: Real-time analytics and performance metrics
- **Employee Performance**: Per-user metrics and rankings
- **Google Sheets Integration**: Toggle-able cloud storage (requires setup)

## Google Sheets Setup (Optional)

1. Create a Google Cloud project and enable Sheets API
2. Create a service account and download credentials JSON
3. Share your Google Sheet with the service account email
4. Set environment variable `GOOGLE_APPLICATION_CREDENTIALS` or place JSON in project root
5. Enable Google Sheets mode in Settings page

## Architecture Notes

- Excel storage uses file locking for concurrency safety
- All timestamps use Asia/Kolkata timezone
- Password security via bcrypt hashing
- Modular design for easy migration to SQL databases
- Production deployment requires proper database backend

## Development

Run tests: `python -m pytest tests/`

**Note**: Excel storage is suitable for prototyping. For production use, migrate to PostgreSQL or similar database.