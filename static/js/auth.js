/**
 * Central Frontend Authentication Guard & UI Controller
 */
(function () {
    // Check Auth State on Page Load & Browser Back Navigation
    function checkAuthGuard() {
        const path = window.location.pathname;
        const isLoginPage = path.startsWith('/login');
        const isPublicNewsPage = path.startsWith('/public');
        const authenticated = API.isAuthenticated();

        // 1. Unauthenticated users trying to access protected pages -> redirect to login
        if (!authenticated && !isLoginPage && !isPublicNewsPage) {
            API.clearAuth();
            window.location.replace('/login/');
            return false;
        }

        // 2. Authenticated users trying to access login page -> redirect to dashboard
        if (authenticated && isLoginPage) {
            window.location.replace('/dashboard/');
            return false;
        }

        return authenticated;
    }

    // Initialize UI and Event Listeners
    async function initAuthUI() {
        const authenticated = checkAuthGuard();

        if (authenticated) {
            try {
                const user = await API.getMe();
                updateUIWithUserInfo(user);
            } catch (e) {
                console.warn('Could not fetch user profile:', e);
                const cachedUser = API.getCurrentUser();
                if (cachedUser) {
                    updateUIWithUserInfo(cachedUser);
                } else {
                    // Invalid token state
                    API.logout(true);
                    return;
                }
            }
        } else {
            updateUIWithAnonymousInfo();
        }

        // Setup Mobile Sidebar Toggle
        const menuBtn = document.getElementById('mobile-menu-btn');
        const sidebar = document.getElementById('sidebar');
        const sidebarOverlay = document.getElementById('sidebar-overlay');

        if (menuBtn && sidebar && sidebarOverlay) {
            menuBtn.addEventListener('click', () => {
                sidebar.classList.toggle('-translate-x-full');
                sidebarOverlay.classList.toggle('hidden');
            });

            sidebarOverlay.addEventListener('click', () => {
                sidebar.classList.add('-translate-x-full');
                sidebarOverlay.classList.add('hidden');
            });
        }

        // Attach Logout Event Listeners
        setupLogoutControls();
    }

    // Attach functional Logout behavior to all logout buttons
    function setupLogoutControls() {
        const logoutBtns = document.querySelectorAll('.logout-btn');
        logoutBtns.forEach((btn) => {
            btn.onclick = function (e) {
                e.preventDefault();
                e.stopPropagation();

                if (typeof openModal === 'function') {
                    const html = `
                        <div class="text-center space-y-3 p-2">
                            <div class="w-12 h-12 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center mx-auto text-xl">
                                <i class="fa-solid fa-right-from-bracket"></i>
                            </div>
                            <div>
                                <h4 class="text-base font-bold text-gray-900">Hisobdan chiqishni xohlaysizmi?</h4>
                                <p class="text-xs text-gray-500 mt-1">Joriy seans yakunlanadi va qayta kirish talab etiladi.</p>
                            </div>
                        </div>
                    `;

                    const footerHtml = `
                        <button type="button" onclick="closeModal()" class="px-4 py-2 text-xs font-semibold text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50">Bekor qilish</button>
                        <button type="button" id="confirm-logout-btn" class="px-4 py-2 text-xs font-semibold text-white bg-rose-600 rounded-xl hover:bg-rose-700 shadow-md shadow-rose-500/20">Chiqish</button>
                    `;

                    openModal("Chiqishni Tasdiqlash", html, footerHtml);

                    const confirmBtn = document.getElementById('confirm-logout-btn');
                    if (confirmBtn) {
                        confirmBtn.onclick = function () {
                            if (typeof closeModal === 'function') closeModal();
                            API.logout(true);
                        };
                    }
                } else {
                    if (confirm('Tizimdan chiqishni tasdiqlaysizmi?')) {
                        API.logout(true);
                    }
                }
            };
        });
    }

    function updateUIWithUserInfo(user) {
        if (!user) return;

        const nameElements = document.querySelectorAll('.user-full-name');
        nameElements.forEach((el) => {
            el.textContent = user.full_name || user.username || 'Foydalanuvchi';
        });

        const usernameElements = document.querySelectorAll('.user-username');
        usernameElements.forEach((el) => {
            el.textContent = `@${user.username}`;
        });

        const navLoginLink = document.getElementById('nav-login-link');
        const navUserInfo = document.getElementById('nav-user-info');
        if (navLoginLink) navLoginLink.classList.add('hidden');
        if (navUserInfo) navUserInfo.classList.remove('hidden');

        // Admin-only elements
        const adminOnlyElements = document.querySelectorAll('.admin-only');
        adminOnlyElements.forEach((el) => {
            if (user.role === 'admin' || user.is_staff) {
                el.classList.remove('hidden');
            } else {
                el.classList.add('hidden');
            }
        });
    }

    function updateUIWithAnonymousInfo() {
        const navLoginLink = document.getElementById('nav-login-link');
        const navUserInfo = document.getElementById('nav-user-info');
        if (navLoginLink) navLoginLink.classList.remove('hidden');
        if (navUserInfo) navUserInfo.classList.add('hidden');

        const adminOnlyElements = document.querySelectorAll('.admin-only');
        adminOnlyElements.forEach((el) => el.classList.add('hidden'));
    }

    // Run on Initial DOM Load
    document.addEventListener('DOMContentLoaded', initAuthUI);

    // Handle Browser Back Button / BFCache Navigation
    window.addEventListener('pageshow', function (event) {
        if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
            checkAuthGuard();
        }
    });

    // Global export
    window.Auth = {
        checkAuthGuard,
        initAuthUI,
        logout: () => API.logout(true),
    };
})();
