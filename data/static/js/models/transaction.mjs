import {system} from "../init.mjs"
/** @typedef {import("../types.mjs").Transaction} BaseTransaction */

class Transaction {

  /**
   * Transaction class
   * @param {string} id 
   * @param {string} name 
   * @param {string} type 
   * @param {string} category 
   * @param {string} amount 
   * @param {string} time 
   */
  constructor(id, name, type, category, amount, time) {
    this.id = id;
    this.name = name;
    this.type = type;
    this.category = category
    this.amount = amount
    this.time = time;
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
   * Get transaction from database
   * @param {string} id 
   * @returns {Transaction}
   */
  static async get(id) {
    /** @type {BaseTransaction} */ const base = system.db.transaction.get_transaction(id)
    return new Transaction(base.id, base.name, base.type, base.category_id, base.amount, base.time)
  }
}

export { Transaction }