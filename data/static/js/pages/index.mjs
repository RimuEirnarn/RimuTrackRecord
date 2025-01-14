import { system } from "../init.mjs"
import { formatCurrency } from "../intl.mjs";

async function setupIndexPage() {
  console.log('init')
  return {
    'current_balance': await formatCurrency(await system.retrieve_current_savings()),
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