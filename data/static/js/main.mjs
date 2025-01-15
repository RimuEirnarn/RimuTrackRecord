import { setLog, system, DEFAULT_SETTINGS, SYSTEM_SETTINGS, INIT_STATE } from "./init.mjs"
import { Template } from "../vendor/enigmarimu.js/template.mjs"
import { setup, goto } from "../vendor/enigmarimu.js/pages.mjs"
import { config } from "../vendor/enigmarimu.js/config.mjs"
import { switchScheme } from "./theme_switcher.mjs"
import "./actions.mjs"
import "./intl.mjs"
import { formatCurrency } from "./intl.mjs"
import { notification } from "./notify.mjs"
// import { setup as index_page } from "./pages/index.mjs"
// import { setup as settings_page } from "./pages/settings.mjs"

async function test_error() {
  try {
    await system.sys.raise_me()
  } catch {
    // console.log(await system.error.get_errors())
  }
}

async function post_pywebview_init() {
  setLog("Configuring theme");
  await system.config.set_if_not_exists("theme", DEFAULT_SETTINGS.theme)
  await system.config.set_if_not_exists("scheme", DEFAULT_SETTINGS.scheme)
  await system.config.set_if_not_exists("currency", DEFAULT_SETTINGS.currency)
  await system.config.set_if_not_exists('locale', DEFAULT_SETTINGS.locale)
  /** @type {string} */
  const theme = await system.config.get("theme");
  /** @type {string} */
  const scheme = await system.config.get("scheme")
  await switchScheme(scheme, theme);
}

async function post_system_setting_init() {
    // For non-scheme/theme settings

    SYSTEM_SETTINGS.locale = await system.config.get("locale", DEFAULT_SETTINGS.locale)
    SYSTEM_SETTINGS.currency = await system.config.get("currency", DEFAULT_SETTINGS.currency)
}

async function init_navbar() {
  /** @type {Element} */
  // @ts-ignore
  const base = document.querySelector("#navbar")
  setLog("Downloading base navigation template")
  const nav = await Template.with_url("navbar", "template/navbar.html", 50)
  nav.render("#navbar", {
    app_name: "RimuTrackRecord"
  })

  base.querySelectorAll("a[href]").forEach((element) => {
    element.addEventListener("click", async (event) => {
      event.preventDefault()
      const url = element.getAttribute('href')
      if (!url)
        return;
      try {
        await goto(url)
      } catch {
        throw new Error(`Page from URL: ${url} doesn't exists`)
      }
    })
  })
}

// async function page_setup() {
//   setup({
//     "/": index_page(),
//     "/settings": settings_page()
//   })
// }

async function page_setup() {
  const routes = {
    "/": "./pages/index.mjs",
    "/settings": "./pages/settings.mjs",
  };

  const routeSetup = {};
  for (const [path, modulePath] of Object.entries(routes)) {
    routeSetup[path] = (await import(modulePath)).setup();
  }

  setup(routeSetup);
}

// async function test() {
//     const prv = SYSTEM_SETTINGS.strict.forgiving
//     const prvl = await system.config.get('locale', DEFAULT_SETTINGS.locale)
//     await system.config.set('locale', "randombullshitgo999")
//     SYSTEM_SETTINGS.strict.forgiving = false
//     await formatCurrency(900)
//     SYSTEM_SETTINGS.strict.forgiving = prv
//     await system.config.set('locale', prvl)
// }

async function main() {
  if (system.init_error) {
    notification.push({body: "Error loading application. Refreshing immediately"})
    location.reload()
  }
  console.info("Starting main")
//   console.info("Config dumping")
//   console.table(await system.config.config_dump())
  console.info("Post initialization [webview]")
  await post_pywebview_init()
  await post_system_setting_init()
  config.target.app = '#app'
  console.info("Initializing navbar")
  await init_navbar()
  console.info("Setting up pages")
  await page_setup()

  console.info("Navigating to the main page")
  await goto("/")
}

// await test()
await main()
INIT_STATE.init_to_runtime_end = performance.now()
INIT_STATE.total_end = performance.now()

console.info(`Initialization took ${INIT_STATE.init_to_runtime_end - INIT_STATE.init_to_runtime_start}ms\nTotal time: ${INIT_STATE.total_end - INIT_STATE.total_start}ms`)