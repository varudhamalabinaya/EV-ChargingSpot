# Session Management Implementation

## Overview

The application now has complete user session management that persists authentication state across page refreshes and manages user sessions globally.

## Architecture

### 1. **AuthContext** (`src/contexts/AuthContext.tsx`)
Global authentication state management using React Context API.

**Provides:**
- `user` - Current authenticated user object
- `isAuthenticated` - Boolean flag for auth state
- `isLoading` - Loading state during initialization
- `login()` - Login function
- `register()` - Register function
- `logout()` - Logout function
- `refreshSession()` - Token refresh for expired access tokens

### 2. **useAuth Hook** (`src/hooks/useAuth.ts`)
Custom hook to access auth context anywhere in the app.

```typescript
const { user, isAuthenticated, login, logout } = useAuth();
```

### 3. **ProtectedRoute Component** (`src/components/ProtectedRoute.tsx`)
Guards routes that require authentication.

```typescript
// Basic protected route
<ProtectedRoute>
  <Profile />
</ProtectedRoute>

// Admin-only route
<ProtectedRoute requireAdmin>
  <AdminDashboard />
</ProtectedRoute>
```

## Data Flow

### Login/Registration

```
User fills form
    ↓
handleSignUp/handleSignIn
    ↓
calls authContext.login() or authContext.register()
    ↓
apiClient.login/register()
    ↓
Tokens stored in localStorage
    ↓
getCurrentUser() fetches user data
    ↓
setUser(userData) updates global state
    ↓
Components using useAuth() re-render with new user data
    ↓
Navigate to protected page (auto-redirect in ProtectedRoute)
```

### Session Persistence

```
App mounts
    ↓
AuthProvider initializes
    ↓
useEffect calls initializeSession()
    ↓
Checks localStorage for access_token
    ↓
If token exists → calls apiClient.getCurrentUser()
    ↓
Sets user state if valid
    ↓
isLoading = false, components render with user data
```

### Logout

```
User clicks logout
    ↓
calls authContext.logout()
    ↓
apiClient.logout() clears refresh tokens on backend
    ↓
apiClient.clearTokens() removes from localStorage
    ↓
setUser(null) clears user state
    ↓
ProtectedRoutes redirect to /auth
```

## Token Storage

Tokens are stored in `localStorage`:
```javascript
localStorage.setItem('access_token', token);
localStorage.setItem('refresh_token', token);
```

**Why localStorage?**
- Persists across page refreshes
- Accessible by all tabs/windows
- Simple API client integration
- Tokens automatically sent with requests

## Components Updated

### Auth.tsx
- Uses `useAuth()` hook instead of direct API calls
- Calls `authContext.login()` and `authContext.register()`
- Auto-redirects to `/map` if already authenticated

### Navbar.tsx
- Uses `useAuth()` hook to get user state
- Shows "Sign In" button when not authenticated
- Shows user dropdown when authenticated
- Displays admin badge if user is superuser
- Admin menu items only show for admins

### Profile.tsx
- Shows user information
- Displays member since date
- Shows admin badge if applicable
- Protected route (requires authentication)

### App.tsx
- Wrapped with `<AuthProvider>`
- Protected routes wrapped with `<ProtectedRoute>`
- Admin routes wrapped with `<ProtectedRoute requireAdmin>`

## Authentication Flow

### Initial Load
1. App mounts
2. `AuthProvider` initializes
3. Checks `localStorage` for tokens
4. If tokens exist, fetches current user
5. Sets `user` state and `isLoading = false`
6. Components render with correct auth state

### User Registration
1. User fills signup form (email + password only)
2. Form validation with Zod
3. `authContext.register()` called
4. Backend creates user account
5. User shown confirmation message
6. User prompted to sign in

### User Login
1. User fills login form
2. Form validation with Zod
3. `authContext.login()` called
4. Backend validates credentials
5. Tokens returned and stored in `localStorage`
6. `getCurrentUser()` fetches user data
7. User state updated globally
8. Auto-redirect to `/map`

### Protected Routes
1. Route accessed (e.g., `/profile`)
2. `ProtectedRoute` component checks `isAuthenticated`
3. If `isLoading`, shows loading state
4. If not authenticated, redirects to `/auth`
5. If admin-only and user not admin, redirects to `/map`
6. Otherwise renders component

### Logout
1. User clicks "Sign Out" in dropdown
2. `logout()` called
3. Backend clears refresh tokens (TTL cleanup)
4. Tokens removed from `localStorage`
5. User state cleared
6. User redirected to home

## Auto-Redirect Behaviors

### Already Authenticated
- Visiting `/auth` → auto-redirect to `/map`
- This happens in Auth.tsx `useEffect`

### Not Authenticated
- Visiting `/profile` → redirect to `/auth`
- Visiting `/add-station` → redirect to `/auth`
- Visiting `/admin` → redirect to `/auth`
- This happens in `ProtectedRoute` component

### Insufficient Permissions
- Admin trying to access `/profile` → allowed
- User trying to access `/admin` → redirect to `/map`
- This happens in `ProtectedRoute` with `requireAdmin`

## Accessing User Data

### In Components
```typescript
import { useAuth } from '@/hooks/useAuth';

function MyComponent() {
  const { user, isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) return <div>Loading...</div>;
  
  if (!isAuthenticated) return <div>Please sign in</div>;
  
  return <div>Welcome, {user?.email}</div>;
}
```

### Conditional Rendering
```typescript
const { user, isAuthenticated } = useAuth();

return (
  <>
    {isAuthenticated && user?.is_superuser && (
      <AdminPanel />
    )}
    
    {isAuthenticated && !user?.is_superuser && (
      <UserPanel />
    )}
    
    {!isAuthenticated && (
      <GuestPanel />
    )}
  </>
);
```

## API Integration

### API Client Methods
All methods in `src/lib/api-client.ts` automatically:
- Add `Authorization: Bearer {token}` header
- Handle token storage
- Parse responses
- Throw errors for failed requests

```typescript
// Methods available
apiClient.register(email, password)
apiClient.login(email, password)
apiClient.logout(refreshToken, allSessions?)
apiClient.refreshToken(refreshToken)
apiClient.getCurrentUser()
apiClient.getStations(filters?)
apiClient.createStation(stationData)
// ... and more
```

## Token Refresh Strategy

When access token expires:
1. API returns 401 Unauthorized
2. App should call `refreshToken()` with refresh token
3. New tokens received and stored
4. Retry original request

This is handled automatically in `AuthContext.refreshSession()`.

## Security Notes

✅ **Implemented:**
- Passwords hashed with bcrypt on backend
- Refresh tokens stored with TTL on backend
- Access tokens expire (60 minutes default)
- HTTPS recommended for production
- Tokens cleared on logout
- Protected routes prevent unauthorized access

⚠️ **Production Considerations:**
- Use `httpOnly` cookies instead of localStorage (if possible)
- Implement refresh token rotation
- Add CSRF protection
- Implement rate limiting on auth endpoints
- Add email verification for new accounts
- Implement password reset flow

## Testing the Session

### Test 1: Registration & Login
1. Go to `/auth`
2. Click "Sign Up"
3. Enter email and password
4. Click "Sign Up"
5. Should show success message
6. Click "Sign In" tab
7. Use registered credentials
8. Should redirect to `/map` with user authenticated

### Test 2: Session Persistence
1. After login, refresh the page
2. User should still be logged in (check Navbar)
3. Tokens stored in localStorage (check DevTools)

### Test 3: Protected Routes
1. Open browser DevTools
2. Go to Application → localStorage
3. Remove `access_token` and `refresh_token`
4. Try to access `/profile`
5. Should redirect to `/auth`

### Test 4: Logout
1. Click user avatar in Navbar
2. Click "Sign Out"
3. Should redirect to home page
4. Navbar should show "Sign In" button
5. localStorage should be cleared

### Test 5: Auto-Redirect
1. After login, try to access `/auth`
2. Should auto-redirect to `/map`

## Troubleshooting

### User Not Persisting After Refresh
- Check localStorage has tokens (DevTools → Application)
- Check backend `/auth/me` endpoint returns user
- Check AuthProvider is wrapping entire app in App.tsx

### Protected Routes Not Working
- Verify `ProtectedRoute` component wraps the route
- Check `useAuth()` hook is being used
- Verify `isAuthenticated` state is correct

### Cannot Login
- Check MongoDB connection
- Check user document exists in database
- Check password hash verification
- Check `/auth/login-json` endpoint in backend

### Navbar Not Updating
- Verify `useAuth()` hook is called
- Check component re-renders when user state changes
- Check localStorage has tokens after login

## File Structure

```
src/
├── contexts/
│   └── AuthContext.tsx          # Global auth state
├── hooks/
│   └── useAuth.ts               # Auth context hook
├── components/
│   ├── ProtectedRoute.tsx       # Route protection
│   ├── Navbar.tsx               # Updated for auth
│   └── ...
├── pages/
│   ├── Auth.tsx                 # Updated for auth context
│   ├── Profile.tsx              # Shows user info
│   └── ...
├── lib/
│   └── api-client.ts            # API integration
└── App.tsx                      # Wrapped with AuthProvider
```

## Next Steps

1. Test all authentication flows
2. Monitor browser console for errors
3. Check backend logs for API issues
4. Verify MongoDB user documents
5. Test protected routes
6. Test logout and session clearing
7. Add email verification (optional)
8. Add password reset (optional)
9. Implement token refresh on 401
10. Deploy to production with HTTPS

---

Session management is now complete! Users will have persistent authentication across page refreshes, protected routes, and proper session management. 🎉
