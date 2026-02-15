# IMIQ - Intelligent Order Management & E-commerce Tool

**IMIQ** is a comprehensive order management and e-commerce solution built with Streamlit and Python. It provides a complete suite of tools for managing orders, inventory, shipments, and customers while offering real-time analytics and KPI dashboards.

## ✨ Key Features

### 🔐 Authentication & User Management
- **Secure Authentication**: bcrypt password hashing with role-based access control
- **Multi-user Support**: Admin and User roles with different permissions
- **Session Management**: Persistent login sessions with secure logout

### 📦 Order Management
- **Complete Order Lifecycle**: From creation to fulfillment
- **Real-time Tracking**: Order status updates and history
- **Customer Integration**: Linked customer profiles and order history
- **Advanced Search**: Filter orders by multiple criteria

### 📊 Inventory Management
- **Product Catalog**: Complete product management with SKU tracking
- **Stock Monitoring**: Real-time stock levels and low-stock alerts
- **Category Management**: Organize products by categories
- **Price Management**: Dynamic pricing and cost tracking

### 🚚 Shipment Management
- **Shipment Creation**: Link orders to shipments
- **Courier Integration**: Support for multiple courier services
- **Tracking Management**: Real-time shipment tracking
- **Delivery Analytics**: Performance metrics and delivery times

### 📈 Analytics & KPIs
- **Real-time Dashboards**: Interactive charts and visualizations
- **Revenue Analytics**: Daily, weekly, and monthly revenue tracking
- **Order Analytics**: Order trends and performance metrics
- **Inventory Analytics**: Stock movement and reorder recommendations

### 🗄️ Data Integration
- **Excel Integration**: Works seamlessly with existing CZ_MasterSheet.xlsx
- **Google Sheets Support**: Cloud-based data synchronization
- **Data Validation**: Comprehensive data integrity checks
- **File Locking**: Concurrent access protection

## 🗂️ Schema Integration

IMIQ is designed to work with your existing **CZ_MasterSheet.xlsx** file structure:

### Supported Sheets & Columns

#### Users Sheet
- `user_id`, `email`, `password_hash`, `plain_password`, `role`, `name`, `created_at`, `is_active`

#### NewOrders Sheet  
- `order_id`, `phone`, `customer_name`, `product`, `quantity`, `total`, `status`, `timestamp`, `created_by`
- Additional fields: `balance_to_pay`, `advance_paid`, `address`, `city`, `pincode`, `payment_method`, etc.

#### ProductList Sheet
- `product_name`, `price`, `description`, `stock`, `category`, `sku`, `status`, `image_url`

#### Additional Sheets
- `Customers` - Customer management
- `ChatLogs` - Communication history  
- `OrderStages` - Order workflow stages
- `AI_Prompts` - AI integration prompts
- `ChatAssignments` - Customer service assignments

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- CZ_MasterSheet.xlsx file in the project directory

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd CrazyShopperz
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

4. **Access the application:**
   - Open your browser to `http://localhost:8501`
   - Login with existing credentials or create a new account

### Test Admin Account
For testing, you can create an admin account:
```python
# Run this in Python to create a test admin
from imiq.storage import get_storage_instance
from imiq.auth import AuthService

storage = get_storage_instance()
auth = AuthService(storage)

auth.create_account('admin@test.com', 'admin_test', 'admin123', 'admin', 'Test Admin')
```

## 📁 Project Structure

```
IMIQ/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── CZ_MasterSheet.xlsx        # Data storage (Excel)
├── test_integration.py        # Integration test script
├── imiq/                      # Core IMIQ package
│   ├── __init__.py
│   ├── storage.py             # Data storage abstraction
│   ├── auth.py                # Authentication service
│   ├── orders.py              # Order management
│   ├── inventory.py           # Inventory management
│   ├── shipments.py           # Shipment tracking
│   ├── kpis.py                # Analytics and KPIs
│   ├── ui_components.py       # UI components
│   ├── settings.py            # System settings
│   └── utils.py               # Utility functions
└── tests/                     # Test suite
    ├── test_auth.py
    ├── test_orders.py
    ├── test_inventory.py
    └── test_integration.py
```

## 🛠️ Core Services

### StorageService
- **Excel Backend**: Primary data storage using openpyxl
- **Google Sheets**: Optional cloud synchronization
- **File Locking**: Prevents data corruption during concurrent access
- **Schema Validation**: Ensures data integrity

### AuthService
- **User Registration**: Create new user accounts with secure password hashing
- **Authentication**: Login verification with bcrypt
- **Session Management**: Handle user sessions in Streamlit
- **Role Management**: Admin and user permission levels

### OrderService
- **Order Creation**: Complete order processing workflow
- **Order Updates**: Status changes and modifications
- **Search & Filter**: Advanced order search capabilities
- **Order Analytics**: Performance metrics and insights

### InventoryService
- **Product Management**: Add, update, and remove products from ProductList
- **Stock Tracking**: Real-time inventory levels
- **Low Stock Alerts**: Automated reorder notifications (stock ≤ 5)
- **Category Management**: Product organization and filtering

### ShipmentService
- **Shipment Creation**: Link orders to shipments
- **Courier Integration**: Support for multiple shipping providers
- **Tracking Updates**: Real-time delivery status
- **Performance Analytics**: Shipping efficiency metrics

### KPIService
- **Revenue Metrics**: Sales performance tracking using 'total' column
- **Order Analytics**: Order volume and trends using 'timestamp'
- **Inventory Insights**: Stock movement analysis
- **Growth Metrics**: Period-over-period comparisons

## 🎯 Feature Highlights

### Dashboard
- **Real-time KPIs**: Orders, revenue, growth metrics
- **Interactive Charts**: Order trends and revenue analytics using Plotly
- **Quick Actions**: Recent orders and inventory alerts
- **Performance Overview**: Daily, weekly, monthly statistics

### Order Management
- **Order Creation**: Full order capture with customer phone and details
- **Order Processing**: Status workflow and updates
- **Order Search**: Multi-criteria search and filtering
- **Order Analytics**: Performance insights and trends

### Inventory Management
- **Product Catalog**: Complete product information management
- **Stock Control**: Real-time inventory tracking
- **Low Stock Alerts**: Items with stock ≤ 5 highlighted in red
- **Category Organization**: Product grouping and management

### User Management
- **Role-based Access**: Admin and user permissions
- **Secure Registration**: Self-service account creation
- **Profile Management**: User information updates
- **Activity Tracking**: User action logging

## 🧪 Testing & Validation

### Run Integration Tests
```bash
python test_integration.py
```

### Manual Testing
```bash
# Test storage connection
python -c "from imiq.storage import get_storage_instance; print('✅ Storage OK')"

# Test authentication
python -c "
from imiq.storage import get_storage_instance
from imiq.auth import AuthService
auth = AuthService(get_storage_instance())
auth.create_account('test@example.com', 'test_user', 'test123', 'user', 'Test User')
print('✅ Auth OK')
"

# Test order creation
python -c "
from imiq.storage import get_storage_instance
from imiq.orders import OrderService
orders = OrderService(get_storage_instance())
order_id = orders.create_order({
    'user_id': 'test_user',
    'phone': '9876543210',
    'customer_name': 'Test Customer',
    'product': 'Test Product',
    'quantity': 1,
    'total': 100.0,
    'status': 'Pending'
})
print(f'✅ Order created: {order_id}')
"
```

## 🔧 Configuration

### Storage Configuration
The system automatically detects and uses `CZ_MasterSheet.xlsx` with the following configuration:

```python
# Excel file configuration
EXCEL_FILE = "CZ_MasterSheet.xlsx"
SHEETS = {
    "Users": ["user_id", "email", "password_hash", "plain_password", "role", "name", "created_at", "is_active"],
    "NewOrders": ["order_id", "phone", "customer_name", "product", "quantity", "total", "status", "timestamp", "created_by"],
    "ProductList": ["product_name", "price", "description", "stock", "category", "sku", "status", "image_url"],
    "Customers": ["customer_id", "name", "email", "phone", "address"],
    "ChatLogs": ["log_id", "customer_id", "message", "timestamp", "sender"],
    "OrderStages": ["stage_id", "order_id", "stage", "timestamp", "notes"],
    "AI_Prompts": ["prompt_id", "prompt_text", "category", "created_at"],
    "ChatAssignments": ["assignment_id", "customer_id", "agent_id", "timestamp", "status"]
}
```

## 📊 Analytics & Reporting

### Key Performance Indicators
- **Total Orders**: Real-time order count from NewOrders sheet
- **Revenue Tracking**: Daily, weekly, monthly revenue using 'total' column
- **Growth Metrics**: Period-over-period growth rates
- **Average Order Value**: Revenue per order analysis

### Charts & Visualizations
- **Order Trends**: Time-series order volume using 'timestamp'
- **Revenue Analytics**: Revenue breakdown and trends
- **Status Distribution**: Order status pie charts
- **Inventory Levels**: Stock level monitoring from ProductList

## 🔒 Security Features

### Data Protection
- **bcrypt Hashing**: Secure password storage with salt
- **Session Security**: Streamlit session management
- **Input Validation**: Comprehensive data validation
- **File Locking**: Concurrent access protection using filelock

### Access Control
- **Role-based Permissions**: Admin vs User access levels
- **Authentication Required**: Protected routes and actions
- **Session Management**: Automatic logout and security
- **Admin-only Features**: Inventory management, user creation

## 🚀 Performance Optimization

### Efficiency Features
- **Pandas Optimization**: Efficient data operations
- **Streamlit Caching**: Built-in caching for better performance
- **File Locking**: Prevents data corruption during concurrent access
- **Error Handling**: Comprehensive exception management

### Best Practices
- **Data Loading**: Optimized sheet reading with column selection
- **Memory Management**: Efficient DataFrame operations
- **Connection Pooling**: Reused storage connections
- **Lazy Loading**: Data loaded only when needed

## 🤝 Integration Guide

### Adding New Features
1. **Create Service Module**: Add new service in `imiq/` directory
2. **Update Storage**: Add new sheet configuration if needed
3. **Add UI Components**: Create Streamlit interface in `app.py`
4. **Write Tests**: Add comprehensive tests

### Customization
- **UI Theming**: Modify colors and styles in `ui_components.py`
- **Business Logic**: Extend services with custom methods
- **Data Schema**: Add new columns to existing sheets
- **Integrations**: Add external API connections

## 📝 API Reference

### Core Classes

#### `StorageBase`
- `read_sheet(sheet_name: str) -> pd.DataFrame`
- `write_sheet(sheet_name: str, data: pd.DataFrame)`
- `append_row(sheet_name: str, data: Dict)`

#### `AuthService`
- `create_account(email: str, user_id: str, password: str, role: str, name: str) -> bool`
- `authenticate(email: str, password: str) -> Optional[Dict]`
- `login(email: str, password: str) -> bool`

#### `OrderService`
- `create_order(order_data: Dict) -> str`
- `get_all_orders() -> pd.DataFrame`
- `update_order_status(order_id: str, status: str) -> bool`

#### `InventoryService`
- `get_all_inventory() -> pd.DataFrame`
- `upsert_item(item_data: Dict) -> bool`
- `get_low_stock_alerts() -> pd.DataFrame`

## 🆘 Support & Troubleshooting

### Common Issues

1. **Excel File Locked**
   - Close Excel if open
   - Check for .xlsx~ temporary files
   - Restart the application

2. **Authentication Errors**
   - Verify email format
   - Check password requirements (min 6 chars)
   - Ensure user exists in Users sheet

3. **Data Not Updating**
   - Check file permissions
   - Verify sheet names match exactly
   - Ensure data types are correct

### Logging
The application provides detailed logging for debugging:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Getting Help
- Check the integration tests: `python test_integration.py`
- Review error logs in the Streamlit interface
- Validate your CZ_MasterSheet.xlsx structure

---

**IMIQ** - Empowering your e-commerce operations with intelligent order management! 🚀📦✨