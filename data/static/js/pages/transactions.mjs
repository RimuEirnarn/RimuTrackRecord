import { bound_buttons, globalRepository } from "../../vendor/enigmarimu.js/binder/actions.mjs";
import { goto } from "../../vendor/enigmarimu.js/pages.mjs";
import { Template } from "../../vendor/enigmarimu.js/template.mjs";
import { formatCurrency, formatTime } from "../intl.mjs";
import { Category } from "../models/category.mjs";
import { Transaction } from "../models/transaction.mjs";

const tmp = await Template.with_url("transaction", "template/transaction.html", 50)

async function add_transaction() {
  return await goto("/add_transaction")
}

async function postInitTransactionPage() {
  const base = "#target-table-transaction"
  const transactions = await Transaction.get_all(0, 'asc')
  const tbl = []

  for (let tr of transactions) {
    // console.log(tr)
    tbl.push({
      id: tr.id,
      type: tr.type,
      category: (await Category.get(tr.category)).name,
      amount: await formatCurrency(tr.amount),
      time: await formatTime(tr.time),
      notes: tr.notes
    })
  }

  tmp.batch_prepend(base, tbl)
}


function setup() {
  globalRepository.add_transaction = add_transaction
  return {
    url: "pages/transaction.html",
    async post_init() {
      await postInitTransactionPage()
      bound_buttons(document.querySelector("#app"))
    }
  }
}

export { setup }