import { DownloadManager, prepare } from "../vendor/enigmarimu.js/downloader.mjs";
import { system, DEFAULT_SETTINGS, SYSTEM_SETTINGS } from "./init.mjs";

const MAPPING = {}
const DM = new DownloadManager(true)

/**
 * Loads mapping data to be used
 */
async function loadCurrencyData() {
    DM.setQueue([prepare("currencies", "/static/vendor/countries.data.json", {}, true)])
    await DM.execute_async((response_string, object) => {
        let json = JSON.parse(response_string)
        json.forEach(element => {
            // console.log(element)
            let id = Object.keys(element.currencies)[0]
            if (Object.keys(element.currencies).length == 0)
                return;
            let name = element.currencies[id].name
            MAPPING[id] = name
        });
        return json
    })
}

async function formatCurrency(number) {
    let locale = await system.config.get("locale", DEFAULT_SETTINGS.locale)
    if (SYSTEM_SETTINGS.strict.value) {
        if ((!localeValidity(locale)) && !SYSTEM_SETTINGS.strict.forgiving)
            throw Error(`${locale}: Not a proper locale.`)
        locale = DEFAULT_SETTINGS.locale
    }
    let currency = await system.config.get("currency", DEFAULT_SETTINGS.currency)
    console.log(currency)
    return new Intl.NumberFormat(locale, {style: "currency", currency: currency}).format(number)
}

function localeValidity(locale) {
    try {
        new Intl.NumberFormat(locale, {style: 'currency', currency: 'USD'}).format(1)
        return true;
    } catch {
        return false
    }
}

await loadCurrencyData()
console.debug(MAPPING)

export { loadCurrencyData, formatCurrency, localeValidity, MAPPING }