import {system} from "../init.mjs"
/** @typedef {import("../types.mjs").Transaction} BaseTransaction */

class Transaction {

  /**
   * Transaction class
   * @param {string} id 
   * @param {string} type 
   * @param {string} category 
   * @param {number} amount 
   * @param {number} time 
   * @param {string} notes 
   */
  constructor(id, type, category, amount, time, notes) {
    this.id = id;
    this.type = type;
    this.category = category
    this.amount = amount
    this.time = time;
    this.notes = notes
  }

  /**
   * Push current transaction to database
   */
  async push() {
      system.db.transaction.add_transaction(this)
  }

  /**
   * Update current transaction
   */
  async update() {
    system.db.transaction.update_transaction(this)
  }

  /**
   * Delete current transaction
   */
  async delete() {
    system.db.transaction.delete_transaction(this.id)
  }

  /**
   * cast base transaction to array of transaction
   * @param {BaseTransaction[]} arrayBase 
   * @param {Transaction[]} target 
   */
  static #castTo(arrayBase, target) {
    arrayBase.forEach(e => {
      target.push(new Transaction(e.id, e.type, e.category_id, e.amount, e.time, e.notes))
    });
  }

  /**
   * Get transaction from database
   * @param {string} id 
   * @returns {Transaction}
   */
  static async get(id) {
    /** @type {BaseTransaction} */ const base = system.db.transaction.get_transaction(id)
    return new Transaction(base.id, base.notes, base.type, base.category_id, base.amount, base.time, base.notes)
  }

  /**
   * Get all ungrouped transaction from database
   * @returns {Promise<Transaction[]>}
   */
  static async get_ungrouped() {
    const r = []
    const base = await (system.db.transaction.get_ungrouped_transactions())
    this.#castTo(base, r)
    return r
  }

  /**
   * Get all transaction from database
   * @param {number} [limit=0] 
   * @param {string} [order=null] order of operation. Either asc/desc
   * @returns {Promise<Transaction[]>}
   */
  static async get_all(limit = 0, order = null) {
    const r = []
    const base = await system.db.transaction.get_transactions(limit, order)
    this.#castTo(base, r)
    return r
  }

  /**
   * Get transactions based on amount
   * @param {number} amount 
   * @param {string} state whether filtering less by amount or greater than certain amount (key: greater/lesser)
   * @param {number} limit 
   * @param {string} [order=null] order of operation. Either asc/desc
   * @returns {Promise<Transaction[]>}
   */
  static async get_by_amount(amount, state, limit = 0, order=null) {
    /** @type {Transaction[]} */ const r = []
    const base = await system.db.transaction.get_transaction_by_amount(amount, state, limit, order)
    this.#castTo(base, r)
    return r
  }

  /**
   * Get transactions based on category
   * @param {string} cid 
   * @param {number} limit 
   * @param {string} [order=null] order of operation. Either asc/desc
   * @returns {Promise<Transaction[]>}
   */
  static async get_by_category(cid, limit = 0, order=null) {
    const r = []
    const base = await system.db.transaction.get_transactions_by_category(cid, limit, order)
    this.#castTo(base, r)
    return r
  }

  /**
   * Get transactions based on time/date
   * @param {number} date 
   * @param {string} state whether filtering before (older) or after (newer) (key: older/newer)
   * @param {number} limit 
   * @param {string} [order=null] order of operation. Either asc/desc
   * @returns {Promise<Transaction[]>}
   */
  static async get_by_time(date, state, limit = 0, order=null) {
    const r = []
    const base = await system.db.transaction.get_transactions_by_time(date, state, limit, order)
    this.#castTo(base, r)
    return r
  }

  /**
   * Get transactions based on type
   * @param {number} tr_type 
   * @param {number} limit 
   * @param {string} [order=null] order of operation. Either asc/desc
   * @returns {Promise<Transaction[]>}
   */
  static async get_by_type(tr_type, limit = 0, order=null) {
    const r = []
    const base = await system.db.transaction.get_transactions_by_type(tr_type, limit, order)
    this.#castTo(base, r)
    return r
  }
}

export { Transaction }