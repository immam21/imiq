# 🛍️ CrazyShopperz - Deployment Guide

## 🚀 Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account with this repository
- Google Sheets API credentials (optional, Excel fallback available)

### Deployment Steps

1. **Fork this repository** to your GitHub account

2. **Set up Google Sheets (Optional)**
   - Create a Google Sheets service account
   - Download the service account JSON
   - Upload to Streamlit Secrets as `GOOGLE_SERVICE_ACCOUNT_JSON`

3. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository
   - Set main file path: `app.py`
   - Click "Deploy!"

### Environment Variables (Streamlit Secrets)

```toml
# .streamlit/secrets.toml (for Streamlit Cloud)

[google]
# Paste your service account JSON content here
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

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t crazyshopperz .
```

### Run Container
```bash
docker run -p 8501:8501 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/service_account.json \
  -v /path/to/service_account.json:/app/service_account.json:ro \
  crazyshopperz
```

## 🌐 Other Platform Deployments

### Heroku
```bash
# Create Heroku app
heroku create your-app-name

# Set config vars
heroku config:set GOOGLE_SERVICE_ACCOUNT_JSON='{"type": "service_account", ...}'

# Deploy
git push heroku main
```

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway link
railway up
```

### DigitalOcean App Platform
1. Connect GitHub repository
2. Set environment variables in dashboard
3. Deploy with auto-scaling

## 🔧 Configuration

### Required Files
- ✅ `requirements.txt` - Python dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `pyproject.toml` - Project metadata
- ✅ `health-check.sh` - Deployment health check

### Optional Files
- `service_account.json` - Google Sheets credentials
- `Procfile` - Heroku deployment
- `Dockerfile` - Container deployment

## 🏥 Health Check

Run the health check script to verify deployment readiness:

```bash
chmod +x health-check.sh
./health-check.sh
```

## 📊 Features Available in Deployment

### ✅ Core Features
- 🛒 Order Management System
- 👥 User Authentication & Roles
- 📦 Inventory Management
- 🚚 Shipment Tracking
- 💬 Customer Support Chat

### ✅ Business Analytics
- 🧮 Advanced KPI Calculator
- 📅 Date-wise Business Analytics
- 📈 Revenue & Expense Tracking
- 👥 User Performance Metrics
- 📊 Interactive Charts & Reports

### ✅ Data Storage Options
- 📊 Google Sheets (Primary)
- 📁 Excel Files (Fallback)
- 🔒 Automatic credential detection

## 🔐 Security

### Production Checklist
- ✅ Secure credential management
- ✅ Environment variable configuration
- ✅ HTTPS enforcement (handled by platform)
- ✅ Input validation and sanitization
- ✅ Error handling and logging

## 📞 Support

- 📧 **Email**: support@crazyshopperz.com
- 📚 **Documentation**: Available in repository
- 🐛 **Issues**: GitHub Issues page
- 💬 **Community**: GitHub Discussions

---

**🎉 Your CrazyShopperz application is ready for production deployment!**

Access your deployed app and start managing orders, tracking analytics, and growing your business with comprehensive e-commerce tools.