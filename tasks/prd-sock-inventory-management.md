# Product Requirements Document: Sock Factory Inventory Management System

## Introduction/Overview

The Sock Factory Inventory Management System is a command-line application designed to track sock inventory throughout the production and sales cycle for a local sock manufacturing facility. The system enables staff to monitor stock levels across five distinct stages: Order (via invoice), Raw Made (ready for press), Sent for Press, Ready Stock (after pressing), and Dispatch (ready for sale/shipment). The application supports tracking socks by quality, color, and size attributes, providing real-time visibility into inventory positions at each production stage.

**Problem it solves:** Currently, there is no centralized way to track sock inventory as it moves through the production pipeline, making it difficult to know how much stock is at each stage and which varieties are in production or ready for sale.

**Goal:** Provide a simple, reliable, local inventory tracking system that allows staff to update stock movements and view current inventory levels across all production stages.

## Goals

1. **Enable accurate stock tracking** across all five production stages with variant-level granularity (quality, color, size)
2. **Provide instant visibility** into current inventory levels at each stage for any sock variant
3. **Ensure data integrity** when moving stock between stages (subtract from source, add to destination)
4. **Support concurrent usage** by multiple staff members in the shop without data conflicts
5. **Maintain simplicity** with a text-based interface that requires minimal training

## User Stories

### Stock Manager (Update Role)
- As a stock manager, I want to add new sock orders to the system so that I can track incoming inventory from suppliers
- As a stock manager, I want to move socks from "Order" to "Raw Made" when they arrive and are ready for pressing
- As a stock manager, I want to move socks from "Raw Made" to "Sent for Press" when they are sent to the pressing facility
- As a stock manager, I want to move socks from "Sent for Press" to "Ready Stock" when they return from pressing
- As a stock manager, I want to move socks from "Ready Stock" to "Dispatch" when they are ready to sell or ship
- As a stock manager, I want to specify quality, color, and size for each stock entry so variants are tracked separately
- As a stock manager, I want to see confirmation messages after updates so I know the changes were saved

### Inventory Viewer (Read-Only Role)
- As an inventory viewer, I want to see current stock levels at each stage for all sock variants
- As an inventory viewer, I want to filter stock by quality, color, or size to find specific variants
- As an inventory viewer, I want to see a summary of total inventory across all stages
- As an inventory viewer, I want to check stock without worrying about accidentally modifying data

### Both Roles
- As a user, I want the interface to be simple and text-based so I can use it on any computer in the shop
- As a user, I want the application to start quickly and work offline since we don't need cloud access

## Functional Requirements

### FR1: Sock Variant Definition
1.1. The system must track socks with three attributes: Quality, Color, and Size
1.2. Each unique combination of Quality + Color + Size represents a distinct variant
1.3. The system must support 4 distinct quality types (specific names to be defined during implementation)
1.4. The system must support 10 distinct colors (specific names to be defined during implementation)
1.5. The system must support 10 distinct sizes (specific names to be defined during implementation)
1.6. The system must handle up to 400 possible variant combinations (4 × 10 × 10)
1.7. Users must be able to input/select quality, color, and size when adding stock

### FR2: Stock Stage Management
2.1. The system must maintain five distinct inventory stages: "Order", "Raw Made", "Sent for Press", "Ready Stock", "Dispatch"
2.2. Each stage must track quantity for each sock variant independently
2.3. The system must display stage names clearly in all interfaces

### FR3: Stock Addition (New Orders)
3.1. The system must allow users to add new stock to the "Order" stage
3.2. Users must specify Quality, Color, Size, and Quantity when adding stock
3.3. The system must validate that quantity is a positive integer
3.4. The system must allow users to optionally reference an invoice number for tracking
3.5. The system must confirm successful addition with a message showing what was added

### FR4: Stock Movement Between Stages
4.1. The system must allow users to move stock from one stage to the next in sequence only:
   - Order → Raw Made
   - Raw Made → Sent for Press
   - Sent for Press → Ready Stock
   - Ready Stock → Dispatch
4.2. The system must enforce sequential progression (no stage skipping allowed)
4.3. The system must support partial movements (e.g., move 30 units while 70 remain in current stage)
4.4. When moving stock, the system must subtract the quantity from the source stage
4.5. When moving stock, the system must add the quantity to the destination stage
4.6. The system must prevent moving more stock than available in the source stage
4.7. The system must validate that the quantity to move is a positive integer
4.8. The system must confirm successful movement with before/after quantities

### FR5: Stock Viewing and Reporting
5.1. The system must display current stock levels for all variants at all stages
5.2. The system must provide a summary view showing total quantity at each stage
5.3. The system must allow filtering by Quality, Color, or Size
5.4. The system must display stock in a clear, tabular text format
5.5. The system must show zero quantities for variants with no stock

### FR6: User Interface Modes
6.1. The system must provide two operational modes: "Update Mode" and "View Mode"
6.2. Update Mode must allow all stock modifications (add, move)
6.3. View Mode must only allow viewing stock levels (read-only)
6.4. Users must be able to select their mode when starting the application
6.5. The interface must clearly indicate which mode is active

### FR7: Data Persistence
7.1. The system must store all inventory data in a local SQLite database
7.2. The system must persist data between application sessions
7.3. The system must handle concurrent access from multiple users safely
7.4. The system must create the database file automatically on first run

### FR8: Error Handling and Validation
8.1. The system must validate all numeric inputs (quantities must be positive integers)
8.2. The system must prevent moving stock that doesn't exist
8.3. The system must display clear error messages for invalid operations
8.4. The system must not crash on invalid input; instead prompt user to retry

## Non-Goals (Out of Scope)

1. **Cloud synchronization or remote access** - This is a local-only application for in-shop use
2. **User authentication or authorization** - No login system; users self-select their mode
3. **Historical logs or audit trails** - Only current stock levels are tracked, not movement history
4. **Analytics or trend reporting** - No charts, graphs, or time-based analysis
5. **Integration with accounting or ERP systems** - Standalone inventory tracking only
6. **Multi-location inventory** - Single factory/shop location only
7. **Barcode scanning or hardware integration** - Manual text input only
8. **Automated reordering or alerts** - No notifications or automatic ordering
9. **Export to Excel or PDF** - Data viewable in terminal only
10. **Mobile app or web interface** - Command-line/terminal interface only

## Design Considerations

### User Interface
- Text-based menu system with numbered options for easy navigation
- Clear section headers and dividers for readability
- Tabular format for displaying stock (aligned columns)
- Color coding in terminal (if supported) for different stages
- Input prompts should clearly indicate expected format (e.g., "Enter quantity (number):")

### Data Model
- **Variants Table**: Store unique combinations of Quality, Color, Size
- **Inventory Table**: Link variants to stages with quantities
- Consider using foreign keys to maintain referential integrity
- Index on variant attributes for fast filtering

### Workflow
- Main menu → Mode selection (Update/View) → Action selection → Execute → Return to menu
- Confirmation prompts before destructive operations (moving large quantities)
- "Back" option at each level to return to previous menu

## Technical Considerations

### Technology Stack
- **Language**: Python (recommended for cross-platform CLI, easy SQLite integration)
- **Database**: SQLite3 (local, lightweight, serverless, built into Python)
- **UI Library**: Simple `input()` and `print()` (or optionally `rich` library for better formatting)

### Database Schema (Suggested)
```sql
-- Variants table (supports up to 400 combinations: 4 qualities × 10 colors × 10 sizes)
CREATE TABLE sock_variants (
    variant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    quality TEXT NOT NULL,
    color TEXT NOT NULL,
    size TEXT NOT NULL,
    UNIQUE(quality, color, size)
);

-- Inventory table
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    variant_id INTEGER NOT NULL,
    stage TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (variant_id) REFERENCES sock_variants(variant_id),
    UNIQUE(variant_id, stage),
    CHECK(stage IN ('Order', 'Raw Made', 'Sent for Press', 'Ready Stock', 'Dispatch')),
    CHECK(quantity >= 0)
);

-- Optional: Master lists for variant attributes (ensures consistency)
CREATE TABLE qualities (
    quality_id INTEGER PRIMARY KEY AUTOINCREMENT,
    quality_name TEXT NOT NULL UNIQUE
);

CREATE TABLE colors (
    color_id INTEGER PRIMARY KEY AUTOINCREMENT,
    color_name TEXT NOT NULL UNIQUE
);

CREATE TABLE sizes (
    size_id INTEGER PRIMARY KEY AUTOINCREMENT,
    size_name TEXT NOT NULL UNIQUE
);
```

**Note on Scale**: With 400 possible variant combinations (4 qualities × 10 colors × 10 sizes), simple numbered menus or text input with validation will work well for a CLI interface.

### Concurrent Access
- Use SQLite's built-in locking mechanisms
- Implement transactions for stock movements to ensure atomicity
- Consider using WAL (Write-Ahead Logging) mode for better concurrent read performance

### Error Handling
- Wrap database operations in try-except blocks
- Provide user-friendly error messages (avoid technical jargon)
- Log errors to a file for debugging (optional)

## Success Metrics

1. **System adoption**: Staff consistently use the system for stock tracking within first month
2. **Data accuracy**: Stock counts in system match physical inventory checks (>95% accuracy)
3. **Operational efficiency**: Staff can complete stock updates in under 2 minutes per transaction
4. **System reliability**: Zero data loss incidents during normal operations
5. **User satisfaction**: Staff report the system is easy to use and saves time compared to manual tracking

## Open Questions

### Answered
✅ **Variant attributes**: 4 quality types, 10 colors, 10 sizes (400 possible combinations) - Specific names TBD during implementation
✅ **Partial movements**: Yes, users can move partial quantities (e.g., 30 out of 100)
✅ **Stage skipping**: No, must follow sequential order (Order → Raw Made → Sent for Press → Ready Stock → Dispatch)

### Remaining Questions
1. **Specific variant names**: What are the exact names for the 4 quality types? The 10 colors? The 10 sizes?
2. **Variant input method**: For variant selection, should we use:
   - Numbered menus (e.g., "1. Quality A, 2. Quality B...")?
   - Free text input with validation?
   - Combination of both (menu for quality, text for color/size)?
3. **Bulk operations**: Should the system support moving multiple variants at once, or one at a time?
4. **Correction mechanism**: If a mistake is made (wrong quantity entered), how should corrections be handled?
   - Direct editing of quantities?
   - Reverse movements (move back to previous stage)?
   - Delete and re-add?
5. **Initial stock**: Is there existing inventory that needs to be imported, or starting fresh?
6. **Backup strategy**: Should the system include a manual backup command to copy the database file?
7. **Invoice tracking**: Should invoice numbers be mandatory or optional? Should there be a way to view all orders from a specific invoice?

---

**Document Version**: 1.2
**Created**: 2025-12-25
**Last Updated**: 2025-12-25
**Target Audience**: Development team, factory managers

**Update Log**:
- v1.2: Corrected variant scale to 4×10×10 = 400 combinations (not 40,000)
- v1.1: Updated with answers to initial questions (partial movements: yes, sequential stages: enforced)
- v1.0: Initial PRD creation

**Next Steps**:
1. Define specific names for 4 quality types, 10 colors, and 10 sizes
2. Decide on variant input method (numbered menus, text input, or combination)
3. Answer remaining open questions
4. Proceed to technical implementation planning
