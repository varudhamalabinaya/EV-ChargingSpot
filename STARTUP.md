# 🚀 Plug Spotter Pro - Complete Startup Guide

## Prerequisites
- **Python 3.8+** installed
- **Node.js/npm** installed  
- **MongoDB Atlas account** with credentials configured in `.env`
- **Git** (optional, for version control)

---

## ✅ Pre-Flight Checklist

### Backend Configuration
- [x] Python requirements.txt created with all dependencies
- [x] MongoDB Atlas URI configured in `.env`
- [x] JWT secret key configured in `.env`
- [x] CORS origins configured for frontend
- [x] Python package `__init__.py` files created
- [x] All routers, schemas, and utilities in place

### Frontend Configuration
- [x] React + Vite project setup
- [x] Tailwind CSS + shadcn/ui configured
- [x] API client (`src/lib/api-client.ts`) created
- [x] Environment variable `VITE_API_BASE_URL` configured
- [x] All dependencies in package.json

---

## 📋 Step-by-Step Setup & Execution

### **Phase 1: Backend Installation (5 minutes)**

#### 1.1 Open Terminal/PowerShell and Navigate to Project
```bash
cd path\to\plug-spotter-pro-main
```

#### 1.2 Create Python Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 1.3 Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Expected output:** All packages installed successfully (watch for any errors)

#### 1.4 Verify Backend Configuration
```bash
cd ..
python -c "from backend.app.core.config import get_settings; s = get_settings(); print('✓ Backend configured'); print(f'  DB: {s.MONGODB_DB}'); print(f'  JWT Algorithm: {s.JWT_ALGORITHM}')"
```

**Expected output:** Should show database and JWT settings

---

### **Phase 2: Test MongoDB Connection (3 minutes)**

#### 2.1 Test Connection to MongoDB Atlas
```bash
python << 'EOF'
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.core.config import get_settings

async def test_connection():
    settings = get_settings()
    print(f"Connecting to: {settings.MONGODB_URI[:50]}...")
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    try:
        await client.admin.command('ping')
        print("✓ MongoDB connection successful!")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print("  Check your MONGODB_URI in .env")
        return False
    finally:
        client.close()

result = asyncio.run(test_connection())
EOF
```

**Troubleshooting:**
- If connection fails, verify MongoDB credentials in `.env`
- Check MongoDB Atlas IP whitelist includes your IP
- Ensure internet connection is stable

---

### **Phase 3: Run Backend Server (2 minutes)**

#### 3.1 Start Backend in Terminal 1
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

#### 3.2 Test Backend API
Open browser: **http://localhost:8000/docs**

You should see the Swagger UI with all API endpoints listed.

---

### **Phase 4: Frontend Installation (3 minutes)**

#### 4.1 Open New Terminal/PowerShell and Navigate to Project
```bash
cd path\to\plug-spotter-pro-main
```

#### 4.2 Install Frontend Dependencies
```bash
npm install
```

**Expected output:** All packages installed, no peer dependency errors

#### 4.3 Verify Frontend Configuration
Check that `.env` contains:
```env
VITE_API_BASE_URL="http://localhost:8000/api/v1"
```

---

### **Phase 5: Run Frontend Server (1 minute)**

#### 5.1 Start Frontend in Terminal 2
```bash
npm run dev
```

**Expected output:**
```
  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

#### 5.2 Test Frontend
Open browser: **http://localhost:5173**

You should see the Plug Spotter Pro homepage with:
- Navigation menu (Home, Map, Auth, etc.)
- Charge points map
- Station listings

---

## 🧪 Testing the Application

### Test 1: User Registration
1. Click **"Auth"** in navigation
2. Click **"Sign up"** tab
3. Enter:
   - Email: `test@example.com`
   - Password: `Test123!@#`
   - Full Name: `Test User`
4. Click **"Register"**

**Expected:** Redirected to login or success message

### Test 2: User Login
1. Click **"Auth"** in navigation
2. Enter credentials from registration
3. Click **"Login"**

**Expected:** Logged in, access_token stored in localStorage

### Test 3: View Stations
1. Click **"Stations"** or **"Map"**
2. Should display list of charging stations

**Note:** If empty, create stations via admin panel (requires superuser role)

### Test 4: Create Station (Admin Only)
1. Login with admin account
2. Click **"Add Station"** or **"Admin"**
3. Fill in station details:
   - Name: `Downtown Charger Hub`
   - Address: `123 Main St`
   - City: `San Francisco`
   - etc.
4. Click **"Create"**

**Expected:** Station added to database

---

## 🔑 API Endpoints Reference

### Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pwd","full_name":"User"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login-json \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pwd"}'

# Get Current User
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Stations
```bash
# List Stations
curl http://localhost:8000/api/v1/stations

# Get Station by ID
curl http://localhost:8000/api/v1/stations/STATION_ID

# Create Station (Admin)
curl -X POST http://localhost:8000/api/v1/stations \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"...","address":"...","city":"..."}'
```

Full API docs: **http://localhost:8000/docs**

---

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python --version

# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Check port 8000 is not in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # macOS/Linux
```

### MongoDB Connection Failed
1. Verify `.env` has correct `MONGODB_URI`
2. Check MongoDB Atlas credentials are correct
3. Whitelist your IP in MongoDB Atlas
4. Test with: `python -m pymongo mongodb://...`

### Frontend Can't Connect to Backend
1. Ensure backend is running on port 8000
2. Check `.env` has `VITE_API_BASE_URL="http://localhost:8000/api/v1"`
3. Check browser console for CORS errors
4. Verify firewall allows localhost communication

### Port Already in Use
```bash
# Backend - use different port
uvicorn app.main:app --reload --port 8001

# Frontend - use different port
npm run dev -- --port 3000
```

### Module Import Errors
```bash
# Reinstall all dependencies
pip install -r backend/requirements.txt --force-reinstall
npm install --force
```

---

## 📊 Project Structure

```
plug-spotter-pro-main/
├── backend/
│   ├── app/
│   │   ├── auth/              # Authentication logic
│   │   ├── stations/          # Station CRUD
│   │   ├── core/              # Config, DB, security
│   │   ├── schemas/           # Pydantic models
│   │   ├── utils/             # Helpers
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend docs
├── src/
│   ├── components/            # React components
│   ├── pages/                 # Route pages
│   ├── lib/
│   │   ├── api-client.ts      # Backend API client
│   │   └── utils.ts           # Utilities
│   ├── App.tsx                # Main app
│   └── main.tsx               # Entry point
├── .env                       # Environment variables
├── package.json               # Frontend dependencies
├── vite.config.ts             # Vite configuration
└── STARTUP.md                 # This file
```

---

## 🔐 Security Notes

### Production Deployment
Before deploying to production:

1. **Change JWT_SECRET_KEY**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Update CORS origins**
   ```env
   BACKEND_CORS_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"
   ```

3. **Use environment variables**
   - Never commit `.env` to git
   - Use managed secrets (AWS Secrets Manager, GitHub Secrets, etc.)

4. **Enable HTTPS**
   - Use Gunicorn + Nginx in production
   - Get SSL certificate (Let's Encrypt)

5. **Database Security**
   - Use MongoDB Atlas IP whitelist
   - Enable VPC peering for production

---

## 📚 Additional Resources

- **Backend Docs:** `backend/README.md`
- **FastAPI Docs:** http://localhost:8000/docs
- **React Docs:** https://react.dev
- **MongoDB Motor Docs:** https://motor.readthedocs.io
- **Pydantic Docs:** https://docs.pydantic.dev

---

## ✨ Quick Commands Reference

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
npm install
npm run dev

# Tests
pytest backend/

# Linting
npm run lint

# Build
npm run build
```

---

## 🎯 Success Indicators

✅ Backend running at `http://localhost:8000`
✅ Swagger docs accessible at `http://localhost:8000/docs`
✅ Frontend running at `http://localhost:5173`
✅ Can register new user
✅ Can login and see stations
✅ MongoDB connection confirmed
✅ No CORS errors in browser console

You're all set! 🎉

For issues, check the troubleshooting section or review log output carefully.
