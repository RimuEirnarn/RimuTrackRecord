/** @typedef {import('./types.mjs').PyWebviewAPI} PyWebviewAPI */

/** @type {PyWebviewAPI} */
let dummy_system = {
    sys: {
        async raise_me() { throw Error() },
        async list_files(_) { return []},
        async list_base_files() { return []},
        async read_file(_) { return "" },
        async redownload_webui_dependency() { return null }
    },
    db: {
        budget: {
            async add_budget(_) { return null },
            async update_budget(_) { return null },
            async delete_budget(_) { return null },
            async get_budgets() { return [] },
            async get_budget(_) { return null }
        },
        collection: {
            async add_collection(_) { return null },
            async update_collection(_) { return null },
            async delete_collection(_) { return null },
            async get_collections() { return [] },
            async get_collection(_) { return null }
        },
        transaction: {
            async add_transaction(_) { return null },
            async update_transaction(_) { return null },
            async delete_transaction(_) { return null },
            async get_transactions() { return [] },
            async delete_transaction_by_category(_) { return null },
            async delete_transaction_by_time(_) { return null },
            async delete_transaction_by_type(_) { return null },
            async delete_transaction_by_amount(_) { return null },
            async get_transaction(_) { return null },
            async get_ungrouped_transactions() { return [] },
        },
        category: {
            async add_category(_) { return null },
            async update_category(_) { return null },
            async delete_category(_) { return null },
            async get_categories() { return [] },
            async get_category(_) { return null }
        },
        collection_transaction: {
            async add_collection_transaction(_) { return null },
            async delete_collection_transaction(_) { return null },
            async get_collection_transactions() { return [] },
            async get_collection_transaction(_) { return null },
            async get_collection_by_transaction(_) { return [] },
            async get_transactions_by_collection(_) { return [] }
        }
    },
    config: {
        async get(_) { return "" },
        async set(_, __) { return null },
        async delete(_) { return null },
        async set_if_not_exists(_, __) { return null },
        async config_dump() { return [] }
    },
    str: {
        async title(_) { return ""}
    },
    error: {
        async get_errors() { return [] },
        async apply() { return null }
    },
    init_error: true
}

export { dummy_system }