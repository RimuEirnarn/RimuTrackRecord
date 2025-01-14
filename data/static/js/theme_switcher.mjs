import { system, SYSTEM_SETTINGS } from "./init.mjs";

const BASE = '#color-scheme'

/**
 * Switch to scheme and theme
 * @param {string} scheme 
 * @param {string} theme 
 * @returns 
 */
function switchScheme(scheme, theme) {
    if (!validateBeforeApplying(scheme, theme)) {
        return;
    }
    system.config.set("scheme", scheme);
    system.config.set('theme', theme);
    SYSTEM_SETTINGS.scheme = scheme;
    SYSTEM_SETTINGS.theme = theme;

    if (document.querySelector("html").getAttribute("data-bs-theme") !== theme)
        document.querySelector("html").setAttribute("data-bs-theme", theme);

    document.querySelector(BASE).setAttribute('href', `/static/css/theme/${theme}-${scheme}-pastel.css`)
}

/**
 * Validate before applying a scheme
 * @param {string} scheme 
 * @param {string} theme 
 * @returns {boolean} condition if we're allowed to apply a scheme
 */
function validateBeforeApplying(scheme, theme) {
    if (scheme === SYSTEM_SETTINGS.scheme && theme === SYSTEM_SETTINGS.theme) {
        return false;
    }

    // In case if the #color-scheme attribute mismatch with SYSTEM_SETTINGS,
    const base = document.querySelector(BASE);
    if (!base.getAttribute('href').includes(`${SYSTEM_SETTINGS.theme}-${SYSTEM_SETTINGS.scheme}-pastel`)) {
        return true;
    }

    return true;
}

/**
 * Returns all themes
 * @returns {Promise<string[]>}
 */
async function query_all_themes() {
    return await system.sys.list_files("static/css/theme");
}

/**
 * Returns all schemes
 * @returns {Promise<array.<string, string>>}
 */
async function query_all_schemes() {
    const themes = await query_all_themes()
    const schemes = []
    for (const theme of themes) {
        const scheme = theme.split('-')[1]
        if (theme.startsWith('dark')) continue;
        schemes.push([scheme, scheme+'-pastel'])
    }

    return schemes
}

export { switchScheme, query_all_themes, query_all_schemes }