# Sock Factory Inventory Management System

A command-line inventory management system for tracking sock production through multiple manufacturing stages.

## Overview

This system helps manage sock inventory as it moves through the production pipeline, from initial order to final dispatch. It provides real-time tracking, inventory views, and stage-by-stage movement capabilities.

## Features

- **Inventory Tracking**: Track socks by quality, color, and size
- **Stage Management**: Move inventory through 5 production stages
- **Real-time Views**: View current inventory, summaries, and filtered data
- **Data Persistence**: SQLite database for reliable data storage
- **User-Friendly CLI**: Simple menu-driven interface with formatted tables

## Production Stages

The system tracks inventory through 5 sequential stages:

1. **Order** - Initial stock entry point
2. **Raw Made** - Raw socks manufactured
3. **Sent for Press** - Sent to pressing facility
4. **Ready Stock** - Finished and ready for dispatch
5. **Dispatch** - Final stage, ready for delivery

Stock can only move sequentially through these stages (e.g., from Order → Raw Made → Sent for Press, etc.).

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install tabulate
```

3. Run the application:
```bash
python main.py
```

The database will be automatically created on first run.

## Usage

### Starting the Application

```bash
python main.py
```

You'll be greeted with:
```
Hello Roopa Enterprises.
Database ready!

=== Main Menu ===
1. Update Mode
2. View Mode
3. Exit
```

### Update Mode

Update Mode allows you to add new stock and move stock between stages.

#### Adding New Stock

1. Select **Update Mode** (option 1)
2. Choose **Add new stock** (option 1)
3. Enter details:
   - Quality (e.g., A, B, C)
   - Color (e.g., red, blue, white)
   - Size (e.g., S, M, L, XL)
   - Quantity (number of units)

Stock is automatically added to the **Order** stage.

**Example:**
```
Quality: A
Color: red
Size: M
Quantity: 100

✓ Successfully added 100 units of red M socks (Quality A) to Order stage
```

#### Moving Stock

1. Select **Update Mode** (option 1)
2. Choose **Move stock** (option 2)
3. Review the current inventory table
4. Enter sock details (quality, color, size)
5. Select source stage (Order, Raw Made, Sent for Press, or Ready Stock)
6. Enter quantity to move

The system automatically moves stock to the next sequential stage.

**Example:**
```
--- Select Sock to Move ---
Quality: A
Color: red
Size: M

Which stage are you changing?
1. Order --> Raw Made
2. Raw Made --> Sent for Press
3. Sent for Press --> Ready Stock
4. Ready Stock --> Dispatch

Enter your choice (1-4): 1

Quantity to move: 50

✓ Successfully moved 50 units
  From: Order (remaining: 50)
  To: Raw Made (new total: 50)
```

### View Mode

View Mode provides different ways to view your inventory.

#### Show All Stock

Displays complete inventory in a formatted table showing:
- Variant ID
- Quality
- Color
- Size
- Stage
- Quantity

#### Show Summary

Displays total quantities per stage with a grand total:

```
=== Stock Summary by Stage ===
╒════════════════╤══════════════════╕
│ Stage          │   Total Quantity │
╞════════════════╪══════════════════╡
│ Order          │              150 │
│ Raw Made       │               50 │
│ Sent for Press │                0 │
│ Ready Stock    │                0 │
│ Dispatch       │              100 │
╘════════════════╧══════════════════╛

Grand Total: 300 units across all stages
```

#### Filter Stock

Filter inventory by quality, color, and/or size:

1. Select filters one by one
2. Choose "Done" when filters are set
3. View filtered results in table format

### Complete Workflow Example

```
1. Add 100 white M socks (Quality A) → Order stage
2. Move 100 from Order → Raw Made
3. Move 100 from Raw Made → Sent for Press
4. Move 100 from Sent for Press → Ready Stock
5. Move 100 from Ready Stock → Dispatch
```

Result: All 100 units successfully tracked through production to dispatch.

## Project Structure

```
sockStock/
├── main.py              # CLI interface and user interaction
├── database.py          # Database operations and queries
├── config.py            # Configuration constants
├── data/
│   └── inventory.db     # SQLite database (auto-created)
├── tasks/
│   └── tasks-sock-inventory-system.md
└── README.md           # This file
```

## Error Handling

The system includes robust error handling for:

- **Insufficient stock**: Cannot move more than available
- **Invalid input**: Validates all user inputs
- **Missing variants**: Alerts when sock type doesn't exist
- **Stage validation**: Ensures sequential stage progression
- **Graceful exit**: Ctrl+C handled cleanly

## Database

The system uses SQLite for data persistence:

- **Location**: `data/inventory.db`
- **Tables**:
  - `sock_variants`: Unique sock types (quality, color, size)
  - `inventory`: Stock quantities per variant and stage
- **Persistence**: Data survives between sessions

## Tips

- Use descriptive quality codes (A, B, C) for easy filtering
- Check inventory summary regularly to track bottlenecks
- Move stock in batches that match production capacity
- Use filters to focus on specific sock types

## Exiting the Application

- Choose option 3 from Main Menu for clean exit
- Or press Ctrl+C to interrupt (gracefully handled)

## Support

For issues or questions, refer to the task documentation in `tasks/tasks-sock-inventory-system.md`.

---

*Developed for Roopa Enterprises*
