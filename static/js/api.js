/**
 * Central API Client for gulomte-mahalla Frontend
 * Handles REST API requests, Bearer token authentication, automatic token refresh, and error formatting.
 */

const API = (function () {
    const BASE_URL = '';

    // Auth Token Storage Keys
    const ACCESS_TOKEN_KEY = 'mahalla_access_token';
    const REFRESH_TOKEN_KEY = 'mahalla_refresh_token';
    const USER_KEY = 'mahalla_user';

    // Token Helpers
    function getAccessToken() {
        return localStorage.getItem(ACCESS_TOKEN_KEY) || sessionStorage.getItem(ACCESS_TOKEN_KEY);
    }

    function getRefreshToken() {
        return localStorage.getItem(REFRESH_TOKEN_KEY) || sessionStorage.getItem(REFRESH_TOKEN_KEY);
    }

    function setTokens(access, refresh) {
        if (access) {
            localStorage.setItem(ACCESS_TOKEN_KEY, access);
            sessionStorage.setItem(ACCESS_TOKEN_KEY, access);
        }
        if (refresh) {
            localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
            sessionStorage.setItem(REFRESH_TOKEN_KEY, refresh);
        }
    }

    function setCurrentUser(user) {
        if (user) {
            const raw = JSON.stringify(user);
            localStorage.setItem(USER_KEY, raw);
            sessionStorage.setItem(USER_KEY, raw);
        } else {
            localStorage.removeItem(USER_KEY);
            sessionStorage.removeItem(USER_KEY);
        }
    }

    function getCurrentUser() {
        const raw = localStorage.getItem(USER_KEY) || sessionStorage.getItem(USER_KEY);
        if (!raw) return null;
        try {
            return JSON.parse(raw);
        } catch (e) {
            return null;
        }
    }

    function clearAuth() {
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        sessionStorage.removeItem(ACCESS_TOKEN_KEY);
        sessionStorage.removeItem(REFRESH_TOKEN_KEY);
        sessionStorage.removeItem(USER_KEY);
    }

    function isAuthenticated() {
        const token = getAccessToken();
        return !!token && token.trim().length > 0;
    }

    // Refresh Token Request
    async function attemptTokenRefresh() {
        const refresh = getRefreshToken();
        if (!refresh) return false;

        try {
            const response = await fetch(`${BASE_URL}/User/token/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh }),
            });

            if (response.ok) {
                const data = await response.json();
                setTokens(data.access, data.refresh || refresh);
                return true;
            }
        } catch (err) {
            console.error('Failed to refresh token:', err);
        }

        clearAuth();
        return false;
    }

    // Core Fetch Wrapper
    async function request(endpoint, options = {}, isRetry = false) {
        const url = `${BASE_URL}${endpoint}`;
        const headers = options.headers || {};

        if (!(options.body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';
        }

        const token = getAccessToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            ...options,
            headers,
        };

        try {
            let response = await fetch(url, config);

            // Handle Token Expiration (401)
            if (response.status === 401 && !isRetry && !endpoint.includes('/User/login/')) {
                const refreshed = await attemptTokenRefresh();
                if (refreshed) {
                    return request(endpoint, options, true); // Retry with new token
                } else {
                    clearAuth();
                    window.location.replace('/login/');
                    throw new Error('Sessiya muddati tugadi. Iltimos, qaytadan tizimga kiring.');
                }
            }

            // Parse response
            let data = null;
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                data = await response.text();
            }

            if (!response.ok) {
                const errorMessage = parseErrorResponse(data, response.status);
                throw new Error(errorMessage);
            }

            return data;
        } catch (error) {
            throw error;
        }
    }

    // Error parser
    function parseErrorResponse(data, status) {
        if (typeof data === 'string' && data.trim()) return data;
        if (!data) return `Xatolik yuz berdi (${status})`;

        if (data.detail) return data.detail;

        if (typeof data === 'object') {
            const messages = [];
            for (const key in data) {
                if (Array.isArray(data[key])) {
                    messages.push(`${key}: ${data[key].join(', ')}`);
                } else if (typeof data[key] === 'string') {
                    messages.push(`${key}: ${data[key]}`);
                }
            }
            if (messages.length > 0) return messages.join('\n');
        }

        return `Server xatosi: ${status}`;
    }

    // Public API Client Object
    return {
        // Auth Actions
        login: async (username, password) => {
            const res = await request('/User/login/', {
                method: 'POST',
                body: JSON.stringify({ username, password }),
            });

            setTokens(res.access, res.refresh);
            if (res.user) {
                setCurrentUser(res.user);
            }
            return res;
        },

        logout: (redirect = true) => {
            clearAuth();
            if (redirect) {
                window.location.replace('/login/');
            }
        },

        getMe: async () => {
            const user = await request('/User/me/', { method: 'GET' });
            setCurrentUser(user);
            return user;
        },

        updateMe: async (data) => {
            const user = await request('/User/me/', {
                method: 'PUT',
                body: JSON.stringify(data),
            });
            setCurrentUser({ ...getCurrentUser(), ...user });
            return user;
        },

        changePassword: async (new_password, confirm_new_password) => {
            return await request('/User/change-password/', {
                method: 'POST',
                body: JSON.stringify({ new_password, confirm_new_password }),
            });
        },

        // News API
        news: {
            getAll: async () => {
                return await request('/News/', { method: 'GET' });
            },
            getById: async (id) => {
                return await request(`/News/${id}/`, { method: 'GET' });
            },
            create: async (data) => {
                return await request('/News/', {
                    method: 'POST',
                    body: JSON.stringify(data),
                });
            },
            update: async (id, data) => {
                return await request(`/News/${id}/`, {
                    method: 'PUT',
                    body: JSON.stringify(data),
                });
            },
            delete: async (id) => {
                return await request(`/News/${id}/`, { method: 'DELETE' });
            },
        },

        // Helpers
        getAccessToken,
        getRefreshToken,
        getCurrentUser,
        setCurrentUser,
        clearAuth,
        isAuthenticated,
    };
})();
