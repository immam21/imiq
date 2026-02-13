# Google Sheets Deployment Guide

## Overview
The IMIQ application now supports **two methods** for Google Sheets authentication:

### Method 1: File-based Credentials (Development)
- Use `service_account.json` file in the project directory
- Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the file path

### Method 2: Environment Variable JSON (Production/Deployment) ✅ RECOMMENDED
- Store the entire JSON content as an environment variable
- More secure for cloud deployments (no files in codebase)

## Deployment Options

### Option A: Environment Variable with JSON Content

1. **Get your service account JSON content:**
   ```bash
   cat service_account.json
   ```

2. **Set the environment variable with the JSON content:**
   ```bash
   export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account","project_id":"your-project",...}'
   ```

3. **Run your application:**
   ```bash
   python3 -m streamlit run app.py
   ```

### Option B: File Path Environment Variable

1. **Upload your service account file to your deployment environment**

2. **Set the file path:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service_account.json"
   ```

3. **Run your application:**
   ```bash
   python3 -m streamlit run app.py
   ```

## Platform-Specific Deployment

### Heroku
Add to your app's Config Vars:
```
GOOGLE_SERVICE_ACCOUNT_JSON = {"type":"service_account","project_id":"..."}
```

### Docker
In your `docker-compose.yml`:
```yaml
environment:
  - GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"..."}
```

### Railway/Vercel/Netlify
Add environment variable in your platform's dashboard:
- Key: `GOOGLE_SERVICE_ACCOUNT_JSON`
- Value: `{"type":"service_account","project_id":"..."}`

### AWS/GCP/Azure
Use platform-specific secrets management:
- AWS: Systems Manager Parameter Store or Secrets Manager
- GCP: Secret Manager
- Azure: Key Vault

## Security Best Practices

1. **Never commit credentials to version control**
2. **Use environment variables in production**
3. **Rotate credentials regularly**
4. **Limit service account permissions to minimum required**
5. **Use secrets management services for sensitive data**

## Testing Your Deployment

After setting environment variables, test with:

```bash
# Test environment variable setup
python3 -c "import os; print('✅ GOOGLE_SERVICE_ACCOUNT_JSON:', 'SET' if os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON') else 'NOT SET')"

# Test application
python3 verify_setup.py
```

## Example Service Account JSON Structure

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "service-account@your-project.iam.gserviceaccount.com",
  "client_id": "client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account%40your-project.iam.gserviceaccount.com"
}
```

## Troubleshooting

- **Credentials not found**: Check environment variable names and content
- **Permission denied**: Verify service account has access to the Google Sheet
- **JSON parsing error**: Ensure JSON content is properly formatted and escaped
- **Import error**: Install required packages: `pip install gspread oauth2client`