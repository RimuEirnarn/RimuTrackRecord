// @ts-check
import { Template } from "../vendor/enigmarimu.js/template.mjs";
import { dummy_system  } from "./system_mock.mjs";
import "./events.mjs"
/** @typedef {import('./types.mjs').PyWebviewAPI} PyWebviewAPI */
/** @typedef {import('./types.mjs').DialogEnum} DialogEnum */
/** @typedef {import('./types.mjs').FixPoint} FixPoint */

/** @type {PyWebviewAPI} */
let system;
/** @type {Template} */
let alert_tmpl;

/** @type {DialogEnum} */
let dialog_enum;

/** @type {FixPoint} */
let fix_point;

/** @type {JQueryStatic} */
// @ts-ignore
let jQuery = window.$;
/** @type {typeof Chart} */
let chart = window.Chart

const DEFAULT_SETTINGS = {
    scheme: "blue",
    theme: "dark",
    currency: "USD",
    locale: 'en'
}

console.log("Initiating the system");
system = dummy_system;
/**
 * Global System Settings
 */
const SYSTEM_SETTINGS = {
    /** Whether code strictly checks its arguments/data */
    strict: {
        /** Strict value */
        value: true,
        /** Throw an error if false. Code needs to define fallback if forgiving is set to true */
        forgiving: false
    },

    /** System theme */
    theme: "",
    /** System color scheme */
    scheme: "",
    /** Locale used for numbers */
    locale: "",
    /** Locale used for currency */
    currency: ""
}
const INIT_STATE = {
  initjs_start: performance.now(),
  mainjs_start: 0,
  initjs_end: 0,
  mainjs_end: 0,
  init_to_runtime_start: 0,
  init_to_runtime_end: 0,
  total_start: performance.now(),
  total_end: 0
};

/**
 * Set log
 * @param {string} text 
 */
function setLog(text) {
  const syslog = document.querySelector("#system-log");
  console.log(`[SYSLOG] ${text}`);
  if (syslog)
    // @ts-ignore
    syslog.innerText = text;
}

async function init_alert() {
  // @ts-ignore
  // document.querySelector("html").setAttribute("data-bs-theme", DEFAULT_THEME);
  setLog("Downloading alert template");
  return Template.with_url("alert", "template/alert.html", 50);
}

try {
  // Attempt to initialize system and wait for pywebview to be available
  alert_tmpl = await init_alert();

  INIT_STATE.initjs_end = performance.now();

  setLog("Initiating pywebview API");
  INIT_STATE.pywebview_start = performance.now();
  system = await (async () => {
    return new Promise((resolve) => {
      setTimeout(resolve, 10);
    // @ts-ignore
    }).then(() => window.pywebview.api);
  })();

  if (!system) {
    throw new Error("PyWebview is not available.");
  }
  
  /** @type {PyWebviewAPI} */
  // @ts-ignore
  window.sys = system;

  fix_point = await system.window.fixpoint_enum()
  dialog_enum = await system.window.dialog_enum()

  INIT_STATE.pywebview_end = performance.now();

  console.log(
    `Base system initialized at ${
      INIT_STATE.initjs_end - INIT_STATE.initjs_start
    }ms`
  );
  console.log(
    `PyWebview API initialized at ${
      INIT_STATE.pywebview_end - INIT_STATE.pywebview_start
    }ms`
  );
  setLog("Base initialization is completed");
  INIT_STATE.init_to_runtime_start = performance.now()
} catch (error) {
  console.error("Error initializing pywebview:", error);
}

export { system, INIT_STATE, SYSTEM_SETTINGS, setLog, jQuery, chart as Chart, fix_point, dialog_enum, DEFAULT_SETTINGS };
