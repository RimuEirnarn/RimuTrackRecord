import { bindForm, collectFormData } from "../../vendor/enigmarimu.js/binder/forms.mjs"
import { switchScheme, query_all_schemes } from "../theme_switcher.mjs"
import { bound_buttons, globalRepository } from "../../vendor/enigmarimu.js/binder/actions.mjs"
import { DEFAULT_SETTINGS, system, SYSTEM_SETTINGS } from "../init.mjs"
import { normalize } from "../utils.mjs"
import { localeValidity, MAPPING } from "../intl.mjs"
import { notification } from "../notify.mjs"

const DEFAULT_SCHEME = 'blue'

async function setupSettingsPage() {
  return { 'submit_text': "Save settings" }
}

async function schemeSelectionFill() {
  /** @type {JQuery} */
  const scheme_selector = $(document.querySelector("[data-bind='system/scheme']"))
  const themes = await query_all_schemes()
  const current_scheme = SYSTEM_SETTINGS.scheme
  themes.forEach(async (css_file) => {
    scheme_selector.append(`<option value="${css_file[0]}" ${current_scheme == css_file[0] ? "selected" : ""}>${await normalize(css_file[1])}</option>`)
    if (current_scheme == css_file[0])
        document.querySelector("option[selected][value='default']")?.removeAttribute("selected")
  })
}

async function currencySelectionFill() {
    /** @type {JQuery} */
    const currency_selector = $(document.querySelector("[data-bind='system/currency']"))
    const mapping = Object.entries(MAPPING)
    mapping.sort((a, b) => (a[0].localeCompare(b[0])))
    const current_currency = SYSTEM_SETTINGS.currency
    mapping.forEach((identifier) => {
        const [id, name] = identifier
        currency_selector.append(`<option value="${id}" ${current_currency == id ? "selected" : ""}>${name} (${id})</option>`)
        if (current_currency == id)
            document.querySelector("option[selected][value='default']")?.removeAttribute("selected")
    })
}

async function postInitSettingsPage() {
  bindForm({
    system: {
      dark_theme: SYSTEM_SETTINGS.theme === "dark",
      scheme: SYSTEM_SETTINGS.scheme,

      locale: SYSTEM_SETTINGS.locale,
      currency: SYSTEM_SETTINGS.currency
    },
  })

  await schemeSelectionFill()
  await currencySelectionFill()
  const base = document.querySelector('form')
  document.querySelector(`[data-id="settings-submit"]`).addEventListener("click", async (event) => {
    event.preventDefault()
    const data = collectFormData(base, {})
    if (data.system.scheme === "default") {
      data.system.scheme = DEFAULT_SCHEME
    }
    await switchScheme(data.system.scheme, data.system.dark_theme ? "dark" : "light")
    SYSTEM_SETTINGS.currency = data.system.currency == "default" ? DEFAULT_SETTINGS.currency : data.system.currency
    SYSTEM_SETTINGS.locale = localeValidity(data.system.locale) ? data.system.locale : SYSTEM_SETTINGS.locale
    await system.config.set("currency", SYSTEM_SETTINGS.currency)
    await system.config.set("locale", SYSTEM_SETTINGS.locale)
    notification.push({title: "", body: "Settings saved"})
  })
  bound_buttons(document.querySelector('body'), globalRepository)
}

function setup() {
  return {
    url: "pages/settings.html",
    async init() {
      return await setupSettingsPage()
    },
    async post_init() {
      return await postInitSettingsPage()
    }
  }
}

export { setup }