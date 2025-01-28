import { system } from "../init.mjs"
import { formatCurrency } from "../intl.mjs";
import { Transaction } from "../models/transaction.mjs";

async function setupIndexPage() {
  const balance = await system.retrieve_current_savings()
  const first_five = await Transaction.get_all(5, 'asc')
  console.debug(first_five)
  return {
    'current_balance': await formatCurrency(balance),
    'balance_status': balance >= 0 ? 'text-success' : 'text-danger',
    'recent_transactions': '+9999',
    "monthly_transaction": "+9999",
    "spending_categories": "+9999"
  }
}

function setup()  {
    return {
        url: "pages/index.html",
        async init() {
            return await setupIndexPage()
        }
    }
}

export { setup }