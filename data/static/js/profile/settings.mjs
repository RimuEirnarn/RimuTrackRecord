// Constants
const DEFAULT = Symbol('default');
const _DELOBJS_CW = ["js_api", "server", "server_args", "localization"];
const _DELOBJS_S = ["func", "server", "server_args", "menu"];
const _STR_DEFKEY = "py:default";
const _DELOBJS_API = ["html", "http_server", "http_port", "storage_path", "ssl", "args"];

class Validation {
  constructor() {
    this.errors = [];
  }

  set(condition, path, message) {
    if (!condition) {
      this.errors.push({ condition, path, message });
    }
  }

  toJSON() {
    return this.errors;
  }
}

/**
 * Remove default values and restricted values from namespace
 * @param {Object.<string, Any>} ns Namespace
 * @param {boolean} to_api 
 * @returns 
 */
function annihilate_defconst(ns, to_api = False) {
  const copied = { ...ns };
  for (const key in { ...ns }) {
    if ((ns[key] === DEFAULT) || (ns[k] == _STR_DEFKEY)) {
      delete copied[key];
      continue
    }
    if ((key in _DELOBJS_CW) || (key in _DELOBJS_S)) {
      delete copied[key];
      continue
    }
    if ((to_api) && (key in _DELOBJS_API)) {
      delete copied[key]
      continue
    }
  }
  return copied
}

class CWConfig {
  constructor({
    title = "",
    url = null,
    html = null,
    js_api = null,
    width = 800,
    height = 600,
    x = null,
    y = null,
    resizable = true,
    fullscreen = false,
    hidden = false,
    frameless = false,
    easy_drag = true,
    minimized = false,
    on_top = false,
    confirm_close = false,
    background_color = "#FFFFFF",
    transparent = false,
    text_select = false,
    zoomable = false,
    draggable = false,
    server = DEFAULT,
    server_args = DEFAULT,
    localization = null
  } = {}) {
    this.title = title;
    this.url = url;
    this.html = html;
    this.js_api = js_api;
    this.width = width;
    this.height = height;
    this.x = x;
    this.y = y;
    this.resizable = resizable;
    this.fullscreen = fullscreen;
    this.hidden = hidden;
    this.frameless = frameless;
    this.easy_drag = easy_drag;
    this.minimized = minimized;
    this.on_top = on_top;
    this.confirm_close = confirm_close;
    this.background_color = background_color;
    this.transparent = transparent;
    this.text_select = text_select;
    this.zoomable = zoomable;
    this.draggable = draggable;
    this.server = server;
    this.server_args = server_args;
    this.localization = localization;
  }

  validate() {
    const vl = new Validation();

    vl.set(typeof this.title === 'string', "app/title", "Title is not a string");
    try {
      const urlObj = new URL(this.url);
      vl.set(
        Boolean(urlObj.protocol && urlObj.host) && this.html === null,
        "app/url",
        "URL is malformed"
      );
    } catch {
      vl.set(
        true, // shadowed
        "app/url",
        "URL is malformed"
      );
    }


    vl.set(Number.isInteger(this.width), "app/width", "the width is not an integer");
    vl.set(Number.isInteger(this.height), "app/height", "the height is not an integer");
    vl.set(this.width > 0, "app/width", "width must not be less than 0");
    vl.set(this.height > 0, "app/height", "height must not be less than 0");

    const booleanProps = [
      this.resizable, this.fullscreen, this.hidden, this.frameless,
      this.easy_drag, this.minimized, this.on_top, this.confirm_close,
      this.transparent, this.text_select, this.zoomable, this.draggable
    ];

    vl.set(
      booleanProps.every(prop => typeof prop === 'boolean'),
      "app/bools",
      "A value is detected to be non-boolean"
    );

    vl.set(
      this.background_color.startsWith('#') && this.background_color.length === 7,
      "app/background_color",
      "Color format is invalid"
    );

    return vl;
  }

  toJSON() {
    return Object.fromEntries(
      Object.entries(this).filter(([_, v]) => v !== DEFAULT)
    );
  }
}

class StartConfig {
  constructor({
    func = null,
    args = null,
    localization = null,
    gui = null,
    debug = false,
    http_server = false,
    http_port = false,
    user_agent = null,
    private_mode = false,
    storage_path = null,
    menu = DEFAULT,
    server = DEFAULT,
    ssl = false,
    server_args = DEFAULT
  } = {}) {
    this.func = func;
    this.args = args;
    this.localization = localization;
    this.gui = gui;
    this.debug = debug;
    this.http_server = http_server;
    this.http_port = http_port;
    this.user_agent = user_agent;
    this.private_mode = private_mode;
    this.storage_path = storage_path;
    this.menu = menu;
    this.server = server;
    this.ssl = ssl;
    this.server_args = server_args;
  }

  validate() {
    const vl = new Validation();
    vl.set(
      typeof this.debug === 'boolean' && typeof this.private_mode === 'boolean',
      "start/any",
      "Either debug/private mode is not boolean"
    );
    return vl;
  }

  toJSON() {
    return Object.fromEntries(
      Object.entries(this).filter(([_, v]) => v !== DEFAULT)
    );
  }
}

class WebviewSetting {
  constructor({
    ALLOW_DOWNLOADS = false,
    ALLOW_FILE_URLS = true,
    ALLOW_EXTERNAL_LINKS_IN_BROWSER = true,
    OPEN_DEVTOOL_IN_DEBUG = true
  } = {}) {
    this.ALLOW_DOWNLOADS = ALLOW_DOWNLOADS;
    this.ALLOW_FILE_URLS = ALLOW_FILE_URLS;
    this.ALLOW_EXTERNAL_LINKS_IN_BROWSER = ALLOW_EXTERNAL_LINKS_IN_BROWSER;
    this.OPEN_DEVTOOL_IN_DEBUG = OPEN_DEVTOOL_IN_DEBUG;
  }

  validate() {
    const allValues = Object.values(this);
    if (!allValues.every(v => typeof v === 'boolean')) {
      throw new Error("All WebviewSetting values must be boolean");
    }
  }

  toJSON() {
    return { ...this };
  }
}

function createConfigsFromDict(configDict) {
  // Get the field names for each config type
  const cwFields = new Set(Object.getOwnPropertyNames(new CWConfig({})));
  const startFields = new Set(Object.getOwnPropertyNames(new StartConfig({})));
  const settingFields = new Set(Object.getOwnPropertyNames(new WebviewSetting({})));

  // Initialize objects to hold sorted config values
  const cwDict = {};
  const startDict = {};
  const settingDict = {};

  // Sort config items into appropriate dictionaries
  for (const [key, value] of Object.entries(configDict)) {
    if (cwFields.has(key)) {
      cwDict[key] = value;
    } else if (startFields.has(key)) {
      startDict[key] = value;
    } else if (settingFields.has(key)) {
      settingDict[key] = value;
    }
  }

  // Create new config objects
  const cwConfig = new CWConfig(cwDict);
  const startConfig = new StartConfig(startDict);
  const webviewSetting = new WebviewSetting(settingDict);

  return [cwConfig, startConfig, webviewSetting];
}

/**
 * Profile for webview/advanced settings
 */
class Profile {
  constructor(url = null, title = null) {
    this._data = new CWConfig({ title, url });
    this._start_data = new StartConfig({ private_mode: false, storage_path: null });
    this.common_config = new WebviewSetting();
  }

  updateFromConfig(configDict) {
    try {
      [this._data, this._start_data, this.common_config] = createConfigsFromDict(configDict);

      // Validate the new configs
      // const validationResults = this.validate();
      // if (validationResults.length > 0) {
      //   throw new Error(`Invalid configuration: ${JSON.stringify(validationResults)}`);
      // }
    } catch (error) {
      throw new Error(`Failed to update configuration: ${error.message}`);
    }
  }

  validate() {
    const validations = [];
    validations.push(...this._data.validate().toJSON());
    validations.push(...this._start_data.validate().toJSON());
    this.common_config.validate();
    return validations;
  }

  toDict() {
    return {
      app: this._data.toJSON(),
      start: this._start_data.toJSON(),
      config: this.common_config.toJSON()
    };
  }
}

export { Profile, CWConfig, StartConfig, WebviewSetting, annihilate_defconst }