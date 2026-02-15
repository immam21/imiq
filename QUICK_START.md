# 🏃 Quick Start Guide - Running IMIQ Locally

## One-Minute Setup

### Option 1: Automated Setup (Recommended)

```bash
# Make setup script executable and run it
bash setup.sh

# Then start the app
bash run.sh
```

### Option 2: Manual Setup

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## ✨ What You'll Get

The IMIQ application running at **http://localhost:8501** with:

- ✅ **Real-time Dashboard** with KPIs
- ✅ **Order Management System**
- ✅ **Inventory Tracking**
- ✅ **User Authentication** (role-based)
- ✅ **Data Analytics** with visualizations
- ✅ **Local Data Storage** (Excel-based)

---

## 🔐 Default Login Credentials

| Account Type | Email | Password |
|---|---|---|
| **Admin** | `admin@test.com` | `admin123` |
| **New User** | Create via signup | Your choice |

---

## 🛠️ System Requirements

- **Python**: 3.8 or higher
- **OS**: macOS, Linux, or Windows
- **Disk Space**: ~500MB (for dependencies)
- **RAM**: 2GB minimum (4GB recommended)

---

## 📊 What Happens on First Run

When you run the app for the first time:

1. ✅ Creates local Excel files for data storage
2. ✅ Initializes the database
3. ✅ Creates default admin user
4. ✅ Sets up session management
5. ✅ Loads all modules and features

**No internet required** (unless using Google Sheets integration)

---

## 🚀 Next Steps After Running

1. **Login** with `admin@test.com` / `admin123`
2. **Explore Dashboard** - View KPIs and analytics
3. **Create Orders** - Add sample orders
4. **Manage Inventory** - Add products
5. **Test Features** - Try all modules

---

## 🔧 Advanced Options

### Use Different Port

```bash
streamlit run app.py --server.port 8502
```

### Enable Google Sheets (Optional)

1. Add your credentials to `.streamlit/secrets.toml`
2. Restart the app
3. The app will automatically use Google Sheets

### Run in Production Mode

```bash
streamlit run app.py --logger.level=warning
```

---

## 📁 Project Structure

```
imiq-main/
├── app.py                 # Main application (START HERE)
├── requirements.txt       # Dependencies
├── setup.sh              # Setup script
├── run.sh                # Quick start script
├── .streamlit/           # Streamlit config
│   ├── config.toml       # Settings
│   └── secrets.toml      # Local secrets
├── imiq/                 # Core modules
│   ├── auth.py          # Authentication
│   ├── orders.py        # Orders
│   ├── inventory.py     # Inventory
│   ├── storage.py       # Data storage
│   └── ...
└── tests/               # Test suite
```

---

## 🆘 Troubleshooting

### Problem: `command not found: streamlit`
```bash
# Solution: Reinstall dependencies
pip3 install -r requirements.txt
```

### Problem: Port 8501 is busy
```bash
# Solution: Use a different port
streamlit run app.py --server.port 8502
```

### Problem: Import errors
```bash
# Solution: Upgrade pip and reinstall
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### Problem: Excel files not found
```bash
# Solution: The app creates them automatically on first run
# Just wait a moment and refresh the page
```

---

## 📞 Need Help?

Check these files for more info:
- `LOCAL_SETUP.md` - Detailed setup guide
- `DEPLOYMENT.md` - Cloud deployment options
- `README.md` - Project overview
- `tests/` - Test files with usage examples

---

## 🎉 You're Ready!

Your IMIQ application is now set up and running locally.

**Happy coding!** 🚀
