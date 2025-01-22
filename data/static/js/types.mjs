/**
 * Python API
 * @typedef {Object} PyWebviewAPI
 * 
 * @prop {SystemAPI} sys
 * @prop {DatabaseAPI} db
 * @prop {ConfigAPI} config
 * @prop {ConfigAPI} sys_config
 * @prop {StringAPI} str
 * @prop {ErrorAPI} error
 * @prop {WindowAPI} window
 * @prop {boolean} init_error
 * 
 * @prop {() => Promise<Number>} retrieve_current_savings
 * @prop {() => Promise<never>} exit
 * @prop {() => Promise<boolean>} is_prod
 */

/**
 * String API
 * @typedef {Object} StringAPI
 * @prop {(s: string) => Promise<string>} title Title case a string
 */

/**
 * System API
 * @typedef {Object} SystemAPI
 * @prop {(path: string) => Promise<string[]>} list_files List files in a directory
 * @prop {() => Promise<string[]>} list_base_files List all files residing in DATA directory
 * @prop {(path: string) => Promise<string>} read_file Read a file
 * @prop {() => Promise<null>} redownload_webui_dependency Redownload this mode dependencies
 * @prop {() => Promise<never>} raise_me Raise an error
 */

/**
 * Database API
 * @typedef {Object} DatabaseAPI
 * @prop {BudgetAPI} budget
 * @prop {CollectionAPI} collection
 * @prop {TransactionAPI} transaction
 * @prop {CategoryAPI} category
 * @prop {CollectionTransactionAPI} collection_transaction
 */

/**
 * Config API
 * @typedef {Object} ConfigAPI
 * @prop {(name: string, fallback: null = null) => Promise<any>} get
 * @prop {(name: string, value: any) => Promise<null>} set
 * @prop {(name: string) => Promise<null>} delete
 * @prop {(name: string, value: any) => Promise<null>} set_if_not_exists
 * @prop {() => Promise<Array.<string, string>>} config_dump
 * @prop {() => Promise<Object.<string, any>>} as_object
 */


/**
 * Budget API
 * @typedef {Object} BudgetAPI
 * @prop {(data: Budget) => Promise<null>} add_budget Add a budget
 * @prop {(data: Budget) => Promise<null>} update_budget Update a budget
 * @prop {(budget_id: string) => Promise<null>} delete_budget Delete a budget
 * @prop {() => Promise<Budget[]>} get_budgets Get all budgets
 * @prop {(budget_id: string) => Promise<Budget>} get_budget Get a budget
 */

/**
 * Budget
 * @typedef {Object} Budget
 * @prop {string} id
 * @prop {string} category_id
 * @prop {number} amount
 */

/**
 * Collection API
 * @typedef {Object} CollectionAPI
 * @prop {(data: Collection) => Promise<null>} add_collection Add a collection
 * @prop {(data: Collection) => Promise<null>} update_collection Update a collection
 * @prop {(collection_id: string) => Promise<null>} delete_collection Delete a collection
 * @prop {(limit: number=0, sort_by: string ='asc') => Promise<Collection[]>} get_collections Get all collections
 * @prop {(collection_id: string) => Promise<Collection>} get_collection Get a collection
 * @prop {(date: number) => Promise<Collection[]>} get_collections_by_date Get collections by date
 */

/**
 * Collection
 * @typedef {Object} Collection
 * @prop {string} id
 * @prop {string} name
 * @prop {string} notes
 * @prop {Number} time
 */

/**
 * Transaction API
 * @typedef {Object} TransactionAPI
 * @prop {(data: Transaction) => Promise<null>} add_transaction Add a transaction
 * @prop {(data: Transaction) => Promise<null>} update_transaction Update a transaction
 * @prop {(transaction_id: string) => Promise<null>} delete_transaction Delete a transaction
 * @prop {(limit: number=0) => Promise<Transaction[]>} get_transactions Get all transactions
 * @prop {(transaction_id: string) => Promise<Transaction>} get_transaction Get a transaction
 * @prop {(category_id: string, limit: number=0) => Promise<Transaction[]>} get_transactions_by_category Get all transactions by category
 * @prop {(date: number, limit: number=0) => Promise<Transaction[]>} get_transactions_by_time Get all transactions by time
 * @prop {(tr_type: string, limit: number=0) => Promise<Transaction[]>} get_transactions_by_type Get all transactions by type
 * @prop {(amount: number, limit: 0number=0) => Promise<Transaction[]>} get_transaction_by_amount Get all transactions by amount
 * @prop {() => Promise<Transaction[]>} get_ungrouped_transactions Get all ungrouped transactions
 */

/**
 * Transaction
 * @typedef {Object} Transaction
 * @prop {string} id
 * @prop {string} type
 * @prop {string} category_id
 * @prop {Number} amount
 * @prop {Number} time
 */

/**
 * Category API
 * @typedef {Object} CategoryAPI
 * @prop {(data: Category) => Promise<null>} add_category Add a category
 * @prop {(data: Category) => Promise<null>} update_category Update a category
 * @prop {(category_id: string) => Promise<null>} delete_category Delete a category
 * @prop {(limit: number=0, sort_by: string='asc') => Promise<Category[]>} get_categories Get all categories
 * @prop {(category_id: string) => Promise<Category>} get_category Get a category
 */

/**
 * Category
 * @typedef {Object} Category
 * @prop {string} id
 * @prop {string} name
 * @prop {string} type
 */

/**
 * Collection Transaction API
 * @typedef {Object} CollectionTransactionAPI
 * @prop {(data: CollectionTransaction) => Promise<null>} add_collection_transaction Add a collection transaction
 * @prop {(data: CollectionTransaction) => Promise<null>} update_collection_transaction Update a collection transaction
 * @prop {(ct_id: string) => Promise<null>} delete_collection_transaction Delete a collection transaction
 * @prop {(limit: number=0, sort_by: string='asc') => Promise<CollectionTransaction[]>} get_collection_transactions Get all collection transactions
 * @prop {(ct_id: string) => Promise<CollectionTransaction>} get_collection_transaction Get a collection transaction
 * @prop {(ct_id: string) => Promise<CollectionTransaction[]>} get_collection_by_transaction Get all collection transactions by collection
 * @prop {(ct_id: string) => Promise<CollectionTransaction[]>} get_transactions_by_collection Get all collection transactions by transaction
 */

/**
 * Collection Transaction
 * @typedef {Object} CollectionTransaction
 * @prop {string} id
 * @prop {string} collection_id
 * @prop {string} transaction_id
 */

/**
 * PythonException
 * @typedef {Object} PythonException
 * @prop {string} name
 * @prop {string} value
 * @prop {PythonException | null} cause
 * @prop {PythonException | null} context
 * @prop {string[]} notes
 * @prop {string[]} arguments
 * @prop {TracebackType[]} traceback
 */

/**
 * TracebackType
 * @typedef {Object} TracebackType
 * @prop {string} filename
 * @prop {string} name
 * @prop {Array.[string, string]} lineno
 * @prop {Array.[string, string]} colno
 * @prop {string} line
 * @prop {Object<string, string>} locals
 */

/**
 * Error API
 * @typedef {Object} ErrorAPI
 * @prop {() => Promise<PythonException[]>} get_errors retrieve all errors
 * @prop {() => Promise<null>} apply Apply excepthook to system
 */

/**
 * Window API
 * @typedef {Object} WindowAPI
 * @prop {() => Promise<number>} height Window height
 * @prop {() => Promise<number>} width Window width
 * @prop {() => Promise<FixPoint>} fixpoint_enum FixPoint Enum
 * @prop {() => Promise<DialogEnum>} dialog_enum Dialog Enum
 * @prop {(size_: Array.<number, number>? = null) => Promise<Array.<number, number>>} size Get/set window size
 * @prop {(title: string = "") => Promise<string>} title Get/set window title
 * @prop {(set_val: boolean | null = null) => Promise<boolean>} on_top Get/set on-top property
 * @prop {() => Promise<Array.<number, number>>} get_position Get window position
 * @prop {(title: string, message: string) => Promise<boolean>} create_confirmation_dialog Create confirmation dialog
 * @prop {(dialog_type: number = 10, directory: string = "", allow_multiple: boolean = false, save_filename: string = "", filetype: Array.<string> = []) => Promise<string[] | string>} create_file_dialog Create file dialog, dialog type uses DialogEnum
 * @prop {(title: string) => Promise<null>} set_title
 * @prop {(width: number, height: number, fix_point: number | null = null) => Promise<null>} resize Resize current window, fix_point is Enum, uses FixPoint
 * @prop {() => Promise<null>} restore Restore current minimized window
 * @prop {() => Promise<null>} show Show if hidden
 * @prop {() => Promise<null>} toggle_fullscreen Toggle fullscreen
 * @prop {() => Promise<null>} maximize Maximize the window
 * @prop {() => Promise<null>} minimize minimize the window
 * @prop {() => Promise<null>} native_window Return native window object
 * @prop {(x: number, y: number) => Promise<null>} move Move current window
 */

/**
 * FixPoint, usable for resize
 * @typedef {Object} FixPoint
 * @prop {number} NORTH
 * @prop {number} WEST
 * @prop {number} EAST
 * @prop {number} SOUTH
 */

/**
 * Dialog Enum, usable for file dialog
 * @typedef {Object} DialogEnum
 * @prop {number} open
 * @prop {number} folder
 * @prop {number} save
 */