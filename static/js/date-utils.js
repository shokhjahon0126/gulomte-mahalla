/**
 * Date Utilities for G'ulomte Mahalla Frontend
 * Formats ISO date strings into natural, human-readable Uzbek date representations.
 * Example: "2026-09-14T07:20:00" -> "14-sentabr 2026, 07:20"
 */

const DateUtils = (function () {
    const UZ_MONTHS = [
        'yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun',
        'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr'
    ];

    function parseDate(dateInput) {
        if (!dateInput) return null;
        const d = new Date(dateInput);
        if (isNaN(d.getTime())) return null;
        return d;
    }

    /**
     * Format date with time: "14-sentabr 2026, 07:20"
     */
    function formatDateTime(dateInput) {
        const d = parseDate(dateInput);
        if (!d) return '---';

        const day = d.getDate();
        const month = UZ_MONTHS[d.getMonth()];
        const year = d.getFullYear();
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');

        return `${day}-${month} ${year}, ${hours}:${minutes}`;
    }

    /**
     * Format date only: "14-sentabr 2026"
     */
    function formatDate(dateInput) {
        const d = parseDate(dateInput);
        if (!d) return '---';

        const day = d.getDate();
        const month = UZ_MONTHS[d.getMonth()];
        const year = d.getFullYear();

        return `${day}-${month} ${year}`;
    }

    /**
     * Format for card "Bugungi sana": "14-sentabr"
     */
    function formatShortDate(dateInput = new Date()) {
        const d = parseDate(dateInput) || new Date();
        const day = d.getDate();
        const month = UZ_MONTHS[d.getMonth()];

        return `${day}-${month}`;
    }

    return {
        formatDateTime,
        formatDate,
        formatShortDate,
    };
})();
