# 🚀 Local Setup Guide for IMIQ

## Quick Start (2 minutes)

### 1. **Install Python Dependencies**

Make sure you have Python 3.8+ installed. Then run:

```bash
# Navigate to the project directory
cd /Users/i0s04a6/Downloads/imiq-main

# Install dependencies
pip install -r requirements.txt
```

### 2. **Run the Application**

```bash
streamlit run app.py
```

The app will start at: **http://localhost:8501**

---

## Test Credentials

Use these accounts to test the application:

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@test.com` | `admin123` |
| Regular User | Create via signup | Your choice |

---

## 📋 Feature Checklist

- ✅ **Dashboard**: Real-time KPIs and analytics
- ✅ **Orders**: Create and manage orders
- ✅ **Inventory**: Stock management
- ✅ **Users**: Role-based authentication
- ✅ **Settings**: Configuration management
- ✅ **Excel Storage**: Local data persistence (no Google Sheets needed)

---

## 🔧 Optional: Google Sheets Integration

To enable Google Sheets integration locally:

### Step 1: Create Google Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Sheets API
4. Create a Service Account
5. Download the JSON key file

### Step 2: Add Credentials to Streamlit Secrets
1. Edit `.streamlit/secrets.toml`:
```toml
[google]
service_account = """
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
"""

[sheets]
spreadsheet_id = "your-google-sheets-id"
```

2. Restart the app: `streamlit run app.py`

---

## 📂 Project Structure

```
imiq-main/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── imiq/                     # Core modules
│   ├── auth.py              # Authentication & user management
│   ├── orders.py            # Order management
│   ├── inventory.py         # Inventory management
│   ├── kpis.py              # KPI calculations
│   ├── storage.py           # Data storage (Excel/Sheets)
│   └── ...                  # Other modules
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml         # Local secrets (DO NOT commit)
└── tests/                   # Test suite
```

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'imiq'`
**Solution**: Make sure you're running the command from the project root directory.

### Issue: `streamlit: command not found`
**Solution**: Install Streamlit:
```bash
pip install streamlit>=1.32.0
```

### Issue: `FileNotFoundError` for Excel files
**Solution**: The app will automatically create Excel files in the local directory. Make sure you have write permissions.

### Issue: Port 8501 already in use
**Solution**: Use a different port:
```bash
streamlit run app.py --server.port 8502
```

---

## 📊 Data Storage

### Local Development
- **Default**: Uses Excel files (`.xlsx`) stored locally
- **Location**: Project root directory
- **Automatic**: Files are created on first run

### Optional: Google Sheets
- Set up credentials in `.streamlit/secrets.toml`
- The app will automatically use Google Sheets if configured
- No additional setup needed

---

## 🚀 Next Steps

1. **Explore the Dashboard**: Check out analytics and KPIs
2. **Test Orders**: Create sample orders
3. **Manage Inventory**: Add products and track stock
4. **User Management**: Test role-based access
5. **Deploy**: See [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment

---

## 📞 Support

For issues or questions:
1. Check the test files in `tests/` directory
2. Review the documentation in `DEPLOYMENT.md`
3. Check `imiq/` modules for implementation details

---

## ✅ You're All Set!

Your IMIQ application is now running locally. Enjoy! 🎉
