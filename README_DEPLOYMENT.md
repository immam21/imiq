# 🚀 IMIQ - Intelligent Order Management System

A comprehensive order management and e-commerce solution built with Streamlit, featuring real-time analytics, inventory management, and advanced user authentication.

## ✨ Features

- **📊 Real-time Dashboard**: Interactive KPIs and analytics
- **👥 User Management**: Secure authentication with role-based access
- **📦 Order Management**: Complete order lifecycle tracking
- **📈 Inventory Control**: Stock management with low-stock alerts
- **🚚 Shipment Tracking**: Courier integration ready
- **📱 Responsive Design**: Modern UI with dark theme
- **🔒 Security**: bcrypt password hashing and session management

## 🌟 Live Demo

**Access the app:** [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)

### Test Credentials
- **Admin Account**: `admin@test.com` / `admin123`
- **Regular User**: Create your own account via signup

## 🚀 Quick Start

### For Users
1. Visit the live app link above
2. Create a new account or use test credentials
3. Explore the dashboard, create orders, and manage inventory

### For Developers
```bash
# Clone repository
git clone https://github.com/your-username/CrazyShopperz.git
cd CrazyShopperz

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

## 📊 Dashboard Preview

- **Real-time KPIs**: Orders, revenue, growth metrics
- **Interactive Charts**: Order trends and revenue analytics
- **User Performance**: Individual user statistics
- **Inventory Alerts**: Low stock notifications

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with pandas for data processing
- **Database**: Excel-based storage with file locking
- **Authentication**: bcrypt password hashing
- **Charts**: Plotly for interactive visualizations
- **Deployment**: Streamlit Cloud

## 📁 Project Structure

```
IMIQ/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── CZ_MasterSheet.xlsx    # Data storage
├── imiq/                  # Core package
│   ├── auth.py           # Authentication
│   ├── orders.py         # Order management
│   ├── inventory.py      # Inventory control
│   ├── storage.py        # Data layer
│   └── ...              # Other modules
└── tests/                # Test suite
```

## 🔐 Security Features

- **Secure Authentication**: bcrypt password hashing
- **Role-based Access**: Admin and user permissions
- **Session Management**: Persistent login sessions
- **Data Validation**: Comprehensive input validation

## 🌐 Cloud Deployment

This app is optimized for Streamlit Cloud deployment:

1. **Fork this repository**
2. **Connect to Streamlit Cloud**
3. **Deploy with one click**
4. **Start managing your orders!**

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/CrazyShopperz/issues)
- **Documentation**: See [README_COMPLETE.md](README_COMPLETE.md)
- **Integration Guide**: See [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)

---

**Built with ❤️ using Streamlit** • **Ready for Production** • **Open Source**