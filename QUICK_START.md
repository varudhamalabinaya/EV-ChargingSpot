# 🚀 Quick Start Guide - Plug Spotter Pro with WebSocket Real-Time Updates

## 📋 Prerequisites
- **Python 3.8+** installed
- **Node.js/npm** installed
- **MongoDB Atlas** account with connection URI in `.env`
- Internet connection for MongoDB connection

---

## ✅ Step 1: Verify Environment Configuration

Before starting, ensure your `.env` file has:

```env
MONGODB_URI="mongodb+srv://your_username:your_password@your_cluster.mongodb.net/?retryWrites=true&w=majority&appName=YourApp"
MONGODB_DB="plugspotter"
JWT_SECRET_KEY="your-secret-key-change-this-in-production"
VITE_API_BASE_URL="http://localhost:8000/api/v1"
BACKEND_CORS_ORIGINS="http://localhost:5173,http://localhost:3000,http://localhost:8000"
```

**Check your `.env`:**
- ✓ MONGODB_URI is filled in with real credentials
- ✓ VITE_API_BASE_URL points to localhost:8000
- ✓ All required fields are present

---

## 🎯 Option 1: Automatic Startup (Easiest)

### On Windows:

**Terminal 1 - Backend:**
```batch
Double-click: RUN_BACKEND.bat
```

**Terminal 2 - Frontend:**
```batch
Double-click: RUN_FRONTEND.bat
```

---

## 🎯 Option 2: Manual Startup (If scripts don't work)

### Terminal 1 - Install & Run Backend:

```bash
cd c:\Users\ABINAYA\OneDrive\Desktop\plug-spotter-pro-main
python -m pip install fastapi uvicorn motor pymongo pydantic pydantic-settings python-jose passlib python-multipart python-dotenv cryptography

cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2 - Install & Run Frontend:

```bash
cd c:\Users\ABINAYA\OneDrive\Desktop\plug-spotter-pro-main
npm install --legacy-peer-deps
npm run dev
```

**Expected output:**
```
➜  Local:   http://localhost:5173/
➜  press h to show help
```

---

## 🔌 Step 2: Verify Connection

### Check Backend API:
Open browser: **http://localhost:8000/docs**
- Should see Swagger UI with all API endpoints
- WebSocket endpoint: `/api/v1/realtime/ws/station/{station_id}`

### Check Frontend:
Open browser: **http://localhost:5173**
- Should see Plug Spotter Pro homepage
- Navigation menu visible

### Check Browser Console:
Open **DevTools (F12)** → **Console**
- Should see no CORS errors
- Should see connection attempts to WebSocket

---

## ✨ Test WebSocket Real-Time Updates

### 1. Create a Station (Admin/Backend Test)
```bash
curl -X POST http://localhost:8000/api/v1/stations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Charging Station",
    "address": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "zipcode": "94105",
    "charger_types": ["DC Fast", "Level 2"],
    "available_ports": 5,
    "total_ports": 10,
    "status": "active",
    "price_per_kwh": 0.35,
    "network": "TestNet",
    "is_available": true
  }'
```

### 2. View Station in Frontend
- Navigate to "Map" or "Stations" page
- You should see the station listed
- Real-time availability status shows "Live" connection

### 3. Update Station Status via WebSocket
In another terminal:
```bash
curl -X PATCH http://localhost:8000/api/v1/stations/{station_id} \
  -H "Content-Type: application/json" \
  -d '{
    "status": "maintenance",
    "is_available": false
  }'
```

- Frontend should instantly update without page refresh
- Status badge should change to "Maintenance"
- Connection indicator stays "Live" (green)

---

## 🆘 Troubleshooting

### ❌ "Failed to fetch" Error

**Solution 1: Check Backend is Running**
```bash
curl http://localhost:8000/docs
```
If error: Backend not running, restart Terminal 1

**Solution 2: Check CORS Configuration**
In `.env`, verify:
```env
BACKEND_CORS_ORIGINS="http://localhost:5173,http://localhost:3000,http://localhost:8000"
```

**Solution 3: Restart Both Servers**
- Stop both terminals (Ctrl+C)
- Wait 5 seconds
- Restart both

---

### ❌ MongoDB Connection Failed

**Check your credentials:**
```bash
cd c:\Users\ABINAYA\OneDrive\Desktop\plug-spotter-pro-main
python test_mongo.py
```

**If fails:**
1. Verify `.env` has correct `MONGODB_URI`
2. Check MongoDB Atlas IP whitelist includes your IP
3. Verify internet connection is stable
4. Restart MongoDB Atlas cluster if needed

---

### ❌ Port Already in Use

**For Backend (port 8000):**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F

REM Then restart with different port:
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**For Frontend (port 5173):**
```bash
npm run dev -- --port 3000
```

---

### ❌ WebSocket Connection Not Updating

**Check Browser Console (F12):**
1. Look for WebSocket errors
2. Connection should show "ws://localhost:8000/api/v1/realtime/ws/station/{id}"
3. Should see "pong" messages every 30 seconds

**Backend Logs:**
- Look for "WebSocket connected for station"
- Should see "Status updated for station"
- Check for any error messages

---

## 📊 New WebSocket Real-Time Features

### Components Added:
1. **`useStationWebSocket.ts`** - Enhanced hook with:
   - Auto-reconnection with exponential backoff
   - Connection error tracking
   - Reconnection attempt counter
   - Force reconnect capability

2. **`RealTimeConnectionStatus.tsx`** - Visual indicator showing:
   - ✓ Live (green) - Connected and receiving updates
   - ⟳ Reconnecting (yellow) - Auto-reconnecting with attempt count
   - ✗ Disconnected (red) - Connection failed

3. **`RealTimeStationsList.tsx`** - Real-time dashboard displaying:
   - All stations with live availability
   - Real-time status updates
   - Connection status per station
   - Last update timestamp

### Backend Improvements:
- **Enhanced logging** in `websocket_manager.py` for debugging
- **Error handling** for failed broadcasts
- **Connection tracking** with statistics
- **Graceful cleanup** of disconnected clients

---

## 🎓 API Endpoints

### WebSocket:
```
ws://localhost:8000/api/v1/realtime/ws/station/{station_id}
```

### REST Endpoints:
- **List Stations**: `GET /api/v1/stations`
- **Get Station**: `GET /api/v1/stations/{id}`
- **Create Station**: `POST /api/v1/stations` (admin)
- **Update Station**: `PATCH /api/v1/stations/{id}` (admin)
- **Delete Station**: `DELETE /api/v1/stations/{id}` (admin)

Full API docs: **http://localhost:8000/docs**

---

## 📝 Key Files Modified/Created

**Frontend:**
- ✓ `src/hooks/useStationWebSocket.ts` - Enhanced WebSocket hook
- ✓ `src/components/RealTimeConnectionStatus.tsx` - Connection indicator
- ✓ `src/components/RealTimeStationsList.tsx` - Real-time stations list
- ✓ `src/components/StationAvailabilityStatus.tsx` - Status display

**Backend:**
- ✓ `backend/app/core/websocket_manager.py` - Enhanced manager with logging
- ✓ `backend/app/realtime/router.py` - Improved WebSocket handler

---

## ✅ Success Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Swagger UI accessible at http://localhost:8000/docs
- [ ] Browser shows no CORS errors
- [ ] Can see stations in frontend
- [ ] WebSocket connects (check browser console)
- [ ] Status updates appear in real-time
- [ ] Connection indicator shows "Live" (green)

---

## 🆘 Still Having Issues?

1. **Check all terminals are open** (backend, frontend)
2. **Verify .env configuration** (MongoDB URI, API base URL)
3. **Check firewall** allows localhost on ports 8000 & 5173
4. **Clear browser cache** (Ctrl+Shift+Delete)
5. **Restart both servers** (stop with Ctrl+C, wait 5s, restart)
6. **Check MongoDB Atlas** status and IP whitelist

---

## 📞 Support

- **API Documentation**: http://localhost:8000/docs
- **Backend Logs**: Check terminal running backend
- **Frontend Logs**: Check browser console (F12)
- **MongoDB Test**: Run `python test_mongo.py`

Enjoy real-time updates! 🎉
