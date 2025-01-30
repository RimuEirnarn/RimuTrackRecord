import {system} from "../init.mjs"
/** @typedef {import("../types.mjs").Category} BaseCategory */

class Category {

  /**
   * 
   * @param {string} id 
   * @param {string} name 
   * @param {string} type 
   */
  constructor(id, name, type) {
    this.id = id
    this.name = name
    this.type = type
  }

  /**
   * @param {BaseCategory} base 
   * @returns {Category}
   */
  static #cast(base) {
    return new Category(base.id, base.name, base.type)
  }

  async add() {
    await system.db.category.add_category(this)
  }

  async patch() {
    await system.db.category.update_category(this)
  }

  static async delete(cid) {
    await system.db.category.delete_category(cid)
  }

  static async get(cid) {
    return this.#cast(await system.db.category.get_category(cid))
  }

  static async get_all() {
    const r = []
    (await system.db.category.get_categories()).forEach(el => r.push(el))
    return r
  }
}

export { Category }