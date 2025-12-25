# Task List: Sock Factory Inventory Management System (Simplified)

## Relevant Files

- `main.py` - CLI interface: menus, user input, display output
- `database.py` - All database operations: schema, CRUD, queries
- `config.py` - Constants (stages, database path, default values)
- `test_database.py` - Tests for database functions (optional but recommended)
- `data/inventory.db` - SQLite database file (auto-generated)
- `.gitignore` - Git ignore patterns
- `README.md` - Setup and usage instructions

### Notes

- Keep it simple: just 3 Python files (main.py, database.py, config.py)
- Tests are optional but recommended for database functions
- Use `python main.py` to run the application (or `python3` on some systems)
- Database file will be created automatically in `data/` directory on first run

## Instructions for Completing Tasks

**IMPORTANT:** As you complete each task, you must check it off in this markdown file by changing `- [ ]` to `- [x]`. This helps track progress and ensures you don't skip any steps.

Example:
- `- [ ] 1.1 Read file` → `- [x] 1.1 Read file` (after completing)

Update the file after completing each sub-task, not just after completing an entire parent task.

## Tasks

- [ ] 0.0 Project setup
  - [x] 0.1 Initialize git repository (`git init`)
  - [ ] 0.2 Create `.gitignore` (include `*.db`, `__pycache__`, `.venv`)
  - [ ] 0.3 Create `data/` directory for database file

- [ ] 1.0 Create config.py - Define constants
  - [ ] 1.1 Create `config.py` file
  - [ ] 1.2 Define STAGES constant: list of 4 stages ("Order", "Raw Made", "Sent for Press", "Sale")
  - [ ] 1.3 Define DATABASE_PATH constant: "data/inventory.db"
  - [ ] 1.4 Define stage transition map (which stage follows which)
  - [ ] 1.5 Test by importing config and printing values

- [ ] 2.0 Create database.py - Database schema and initialization
  - [ ] 2.1 Create `database.py` file
  - [ ] 2.2 Import sqlite3 and config
  - [ ] 2.3 Write `init_database()` function to create tables (sock_variants, inventory)
  - [ ] 2.4 Add SQL for sock_variants table (variant_id, quality, color, size, UNIQUE constraint)
  - [ ] 2.5 Add SQL for inventory table (id, variant_id, stage, quantity, foreign key, constraints)
  - [ ] 2.6 Test initialization by running function and checking if database file created

- [ ] 3.0 Create database.py - Add stock functions
  - [ ] 3.1 Write `add_stock()` function: takes quality, color, size, quantity
  - [ ] 3.2 In `add_stock()`: get or create variant (INSERT OR IGNORE into sock_variants)
  - [ ] 3.3 In `add_stock()`: add quantity to "Order" stage in inventory table
  - [ ] 3.4 Use transactions (BEGIN, COMMIT, ROLLBACK on error)
  - [ ] 3.5 Test manually: add a few different sock variants

- [ ] 4.0 Create database.py - Move stock functions
  - [ ] 4.1 Write `move_stock()` function: takes variant_id, source_stage, quantity
  - [ ] 4.2 Validate: check if enough stock exists in source stage
  - [ ] 4.3 Validate: determine destination stage from config (must be sequential)
  - [ ] 4.4 Execute: subtract from source stage, add to destination stage (in transaction)
  - [ ] 4.5 Return success/error message with before/after quantities
  - [ ] 4.6 Test manually: add stock, then move through stages

- [ ] 5.0 Create database.py - View stock functions
  - [ ] 5.1 Write `get_all_inventory()` function: JOIN variants and inventory tables
  - [ ] 5.2 Return list of dicts with: variant_id, quality, color, size, and quantity per stage
  - [ ] 5.3 Write `get_stock_summary()` function: sum quantities per stage
  - [ ] 5.4 Write `filter_inventory()` function: takes optional quality, color, size filters
  - [ ] 5.5 Test manually: view all stock, filter by quality/color

- [ ] 6.0 Create main.py - Main menu
  - [ ] 6.1 Create `main.py` file
  - [ ] 6.2 Import database functions and config
  - [ ] 6.3 Write `main_menu()` function: display options (1. Update Mode, 2. View Mode, 3. Exit)
  - [ ] 6.4 Get user choice with input validation (must be 1, 2, or 3)
  - [ ] 6.5 Call appropriate mode function based on choice
  - [ ] 6.6 Add loop to return to main menu after each mode
  - [ ] 6.7 Test: run main.py and navigate menus

- [ ] 7.0 Create main.py - View Mode
  - [ ] 7.1 Write `view_mode()` function
  - [ ] 7.2 Display view options: 1. Show all stock, 2. Show summary, 3. Filter stock, 4. Back
  - [ ] 7.3 Implement "Show all stock": call `get_all_inventory()` and display in table format
  - [ ] 7.4 Implement "Show summary": call `get_stock_summary()` and display totals per stage
  - [ ] 7.5 Implement "Filter stock": prompt for quality/color/size, call `filter_inventory()`
  - [ ] 7.6 Format output nicely with aligned columns
  - [ ] 7.7 Test: view stock in different ways

- [ ] 8.0 Create main.py - Update Mode
  - [ ] 8.1 Write `update_mode()` function
  - [ ] 8.2 Display update options: 1. Add new stock, 2. Move stock, 3. Back
  - [ ] 8.3 Implement "Add new stock": prompt for quality, color, size, quantity, call `add_stock()`
  - [ ] 8.4 Show confirmation message with what was added
  - [ ] 8.5 Implement "Move stock": list variants with stock in each stage
  - [ ] 8.6 Prompt user to select variant and source stage, enter quantity to move
  - [ ] 8.7 Call `move_stock()` and display confirmation with before/after quantities
  - [ ] 8.8 Handle errors gracefully (insufficient stock, invalid input)
  - [ ] 8.9 Test: add stock and move through all stages

- [ ] 9.0 Polish and finalize
  - [ ] 9.1 Add welcome message when app starts
  - [ ] 9.2 Add helpful prompts and error messages throughout
  - [ ] 9.3 Handle Ctrl+C gracefully (catch KeyboardInterrupt, say goodbye)
  - [ ] 9.4 Test complete workflow: add order → move to Raw Made → move to Sent for Press → move to Sale
  - [ ] 9.5 Fix any bugs found during testing

- [ ] 10.0 Documentation
  - [ ] 10.1 Create `README.md` with project description
  - [ ] 10.2 Add installation instructions (just run `python main.py`)
  - [ ] 10.3 Add usage examples for both modes
  - [ ] 10.4 Document the 4 stages and how stock flows through them
  - [ ] 10.5 Commit all files to git with descriptive message
