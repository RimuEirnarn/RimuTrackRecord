import { system } from "./init.mjs"

async function normalize(css_name) {
  return await system.str.title(css_name.replace(/\.css$/, "").replace(/-/g, " "))
}

export { normalize }