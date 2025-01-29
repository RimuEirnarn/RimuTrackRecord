import { DownloadManager, prepare } from "../vendor/enigmarimu.js/downloader.mjs";
import { system, DEFAULT_SETTINGS, SYSTEM_SETTINGS } from "./init.mjs";

const MAPPING = {}
const DM = new DownloadManager(true)

/**
 * Loads mapping data to be used
 */
async function loadCurrencyData() {
  DM.setQueue([prepare("currencies", "/static/vendor/countries.data.json", {}, true)])
  await DM.execute_async((response_string, _) => {
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
  DM.clear()
}

/**
 * 
 * @returns {Promise<string>}
 */
async function _fetchLocale() {
  let locale = await system.config.get("locale", DEFAULT_SETTINGS.locale)
  if (SYSTEM_SETTINGS.strict.value) {
    if (!localeValidity(locale)) {
      if (!SYSTEM_SETTINGS.strict.forgiving)
        throw Error(`${locale}: Not a proper locale.`)
      locale = DEFAULT_SETTINGS.locale
    }
  }
  return locale
}

/**
 * Format currency as plain number to any currency
 * @param {number} number 
 * @returns {Promise<string>}
 */
async function formatCurrency(number) {
  let locale = await _fetchLocale()
  /** @type {string} */ let currency = await system.config.get("currency", DEFAULT_SETTINGS.currency)
  // console.debug(locale, currency)
  return new Intl.NumberFormat(locale, { style: "currency", currency: currency }).format(number)
}

/**
 * Format time (timestamp) into relative time
 * @param {number} time 
 * @returns {Promise<string>}
 */
async function formatTime(time) {
  let locale = await _fetchLocale()
  return new Intl.DateTimeFormat(locale, {timeStyle: 'medium', dateStyle: 'medium'}).format(time * 1000)
}

function localeValidity(locale) {
  try {
    new Intl.NumberFormat(locale, { style: 'currency', currency: 'USD' }).format(1)
    return true;
  } catch {
    return false
  }
}

await loadCurrencyData()
// console.debug(MAPPING)

export { loadCurrencyData, formatCurrency, localeValidity, formatTime, MAPPING }