/**
 * Toast Notification Utility
 */
const Toast = (function () {
    function show(message, type = 'info', duration = 4000) {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `flex items-center w-full max-w-sm p-4 text-gray-800 bg-white rounded-xl shadow-lg border border-gray-100 transition-all duration-300 transform translate-y-2 opacity-0 space-x-3 z-50`;

        let icon = '<i class="fa-solid fa-circle-info text-blue-500 text-lg"></i>';
        let borderColor = 'border-l-4 border-l-blue-500';

        if (type === 'success') {
            icon = '<i class="fa-solid fa-circle-check text-emerald-500 text-lg"></i>';
            borderColor = 'border-l-4 border-l-emerald-500';
        } else if (type === 'error') {
            icon = '<i class="fa-solid fa-circle-xmark text-rose-500 text-lg"></i>';
            borderColor = 'border-l-4 border-l-rose-500';
        } else if (type === 'warning') {
            icon = '<i class="fa-solid fa-triangle-exclamation text-amber-500 text-lg"></i>';
            borderColor = 'border-l-4 border-l-amber-500';
        }

        toast.className += ` ${borderColor}`;

        toast.innerHTML = `
            <div class="flex-shrink-0">${icon}</div>
            <div class="flex-1 text-sm font-medium text-gray-700 whitespace-pre-line">${message}</div>
            <button type="button" class="text-gray-400 hover:text-gray-600 p-1 rounded-lg focus:outline-none" onclick="this.parentElement.remove()">
                <i class="fa-solid fa-xmark text-sm"></i>
            </button>
        `;

        container.appendChild(toast);

        // Animate in
        requestAnimationFrame(() => {
            toast.classList.remove('translate-y-2', 'opacity-0');
        });

        // Auto remove
        setTimeout(() => {
            toast.classList.add('opacity-0', 'translate-y-2');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    return {
        success: (msg, dur) => show(msg, 'success', dur),
        error: (msg, dur) => show(msg, 'error', dur),
        warning: (msg, dur) => show(msg, 'warning', dur),
        info: (msg, dur) => show(msg, 'info', dur),
    };
})();
