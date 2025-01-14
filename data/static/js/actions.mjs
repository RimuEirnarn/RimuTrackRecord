import { globalRepository } from "../vendor/enigmarimu.js/binder/actions.mjs"
import { system } from "./init.mjs"

globalRepository.redownload = async (_) => {
    console.log("this was called")
    return await system.sys.redownload_webui_dependency()
}

console.debug(globalRepository)