# Deployment Guide - Documentation Generation Agent

## Prerequisites
- Render.com account
- GitHub repository with the code
- Gemini API key

## Step-by-Step Deployment

### Step 1: Prepare Repository
Ensure your `Documentation Generation Agent` folder is in the repository root:
```
D:\Fyp\Code\
├── Documentation Generation Agent/
│   ├── main.py
│   ├── document_generator.py
│   ├── document_templates.py
│   ├── node_fetcher.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   └── README.md
├── backend/
└── ...
```

### Step 2: Push to GitHub
```bash
cd "D:\Fyp\Code"
git add "Documentation Generation Agent"
git commit -m "Add Documentation Generation Agent"
git push origin main
```

### Step 3: Create Web Service on Render

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Click "New +"** → **"Web Service"**
3. **Connect Repository**: Select your GitHub repository
4. **Configure Service**:

#### Basic Settings
- **Name**: `nexa-documentation-agent`
- **Region**: `Singapore` (or closest to your users)
- **Branch**: `main`
- **Root Directory**: `Documentation Generation Agent`
- **Runtime**: `Python 3`

#### Build & Deploy Settings
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

#### Instance Type
- **Free** (for testing)
- **Starter** or higher (for production)

### Step 4: Configure Environment Variables

Add these environment variables in Render dashboard:

| Key | Value |
|-----|-------|
| `GEMINI_API_KEY` | `AIzaSyABR71sWAOBMG_MRBKDggDLFEyT45qj9j4` |
| `DOC_AGENT_GEMINI_MODEL` | `gemini-2.0-flash-exp` |
| `NODE_BASE_URL` | `https://nexa-au2s.onrender.com/api` |
| `DOC_AGENT_API_KEY` | (Optional) Leave empty or set a secret key |
| `DOC_AGENT_API_KEY_HEADER` | `X-API-Key` |
| `PORT` | (Auto-set by Render) |

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment to complete (5-10 minutes)
3. Note the deployed URL: `https://nexa-documentation-agent.onrender.com`

### Step 6: Update Node Backend

Update your Node backend `.env`:

#### For Production (Render)
```env
DOCUMENTATION_AGENT_URL=https://nexa-documentation-agent.onrender.com
```

#### For Local Development
```env
DOCUMENTATION_AGENT_URL=http://localhost:8003
```

**Important**: Redeploy your Node backend on Render after updating the environment variable.

### Step 7: Test Deployment

#### Test Health Endpoint
```bash
curl https://nexa-documentation-agent.onrender.com/health
```

Expected response:
```json
{
  "ok": true,
  "service": "NEXA Documentation Generation Agent",
  "version": "1.0.0"
}
```

#### Test Readiness
```bash
curl https://nexa-documentation-agent.onrender.com/ready
```

Expected response:
```json
{
  "ok": true,
  "ready": true,
  "gemini_configured": true
}
```

#### Test Document Types
```bash
curl https://nexa-documentation-agent.onrender.com/api/documentation/types \
  -H "Content-Type: application/json"
```

## Monitoring

### Check Logs in Render
1. Go to your service dashboard
2. Click "Logs" tab
3. Monitor for:
   - `🚀 Starting NEXA Documentation Generation Agent`
   - `📝 Gemini API configured: True`
   - Incoming requests

### Common Startup Messages
```
🚀 Starting NEXA Documentation Generation Agent on port 8003
📝 Gemini API configured: True
📝 DocumentGenerator initialized with model: gemini-2.0-flash-exp
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
```

## Troubleshooting

### Issue: Service won't start
**Check:**
1. Build logs for Python errors
2. All required files are present
3. `requirements.txt` is in root directory

### Issue: Gemini API not working
**Check:**
1. `GEMINI_API_KEY` is set correctly
2. API key has quota available
3. Check logs for API errors

### Issue: Can't fetch project context
**Check:**
1. `NODE_BASE_URL` is correct
2. Node backend is accessible
3. Authentication headers are forwarded

### Issue: Timeout errors
**Solution:**
- Increase timeout in `node_fetcher.py` if needed
- Or upgrade to paid Render plan for better performance

## Scaling Considerations

### Free Tier Limitations
- Spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Limited CPU and memory

### Recommended for Production
- **Starter Plan** or higher
- Enable **Auto-Scaling**
- Set **Health Check Path**: `/ready`
- Monitor response times and errors

## Security Best Practices

1. **API Key Authentication**:
   ```env
   DOC_AGENT_API_KEY=your_secure_random_key_here
   ```
   Generate with: `openssl rand -base64 32`

2. **HTTPS Only**: Render automatically provides SSL

3. **Environment Variables**: Never commit `.env` to git

4. **Rate Limiting**: Consider adding rate limiting in production

## Cost Estimation

### Render.com Pricing
- **Free**: $0/month (with limitations)
- **Starter**: $7/month (recommended)
- **Standard**: $25/month (for high traffic)

### Gemini API Pricing
- **Gemini 2.0 Flash**: Very low cost
- Approximately $0.000375 per 1K tokens
- Average document generation: ~5K-10K tokens = $0.002-$0.004
- 1000 documents/month ≈ $2-$4

**Total estimated cost**: ~$9-$11/month (Starter + API usage)

## Backup and Rollback

### Create Backup Branch
```bash
git checkout -b documentation-agent-stable
git push origin documentation-agent-stable
```

### Rollback on Render
1. Go to service dashboard
2. Click "Manual Deploy"
3. Select previous deployment

## Monitoring & Alerts

### Set Up Alerts in Render
1. Go to service settings
2. Enable "Deploy notifications"
3. Configure Slack/email alerts
4. Set up custom monitors for:
   - Response time > 5s
   - Error rate > 5%
   - CPU usage > 80%

## Maintenance

### Regular Tasks
- [ ] Monitor Gemini API quota
- [ ] Check error logs weekly
- [ ] Update dependencies monthly
- [ ] Review and optimize slow queries
- [ ] Monitor disk usage

### Update Python Dependencies
```bash
pip list --outdated
pip install --upgrade <package>
pip freeze > requirements.txt
```

## Support URLs

- **Render Dashboard**: https://dashboard.render.com/
- **Service URL**: https://nexa-documentation-agent.onrender.com
- **Health Check**: https://nexa-documentation-agent.onrender.com/health
- **API Docs**: https://nexa-documentation-agent.onrender.com/docs (FastAPI auto-docs)

---

**Deployment Status**: Ready to deploy ✅  
**Estimated Deployment Time**: 5-10 minutes  
**Recommended Plan**: Starter ($7/month)  
