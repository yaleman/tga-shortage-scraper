# TGA Shortage Scraper

A command-line tool to scrape the Australian TGA (Therapeutic Goods
Administration) shortage database for ARTG (Australian Register of Therapeutic
Goods) entries.

## Usage

### Basic Usage

Fetch all shortage entries:

```bash
uv run tga-shortage-scraper
```

### Filter by Ingredient

Search for entries containing a specific active ingredient:

```bash
uv run tga-shortage-scraper --ingredient <ingredient_name>
```

### Example Output

Here's an example of searching for roxithromycin:

```bash
uv run tga-shortage-scraper --ingredient roxithromycin
```

Output:

```json
[
    {
        "artg_id": 99937,
        "artg_name": "ROXIMYCIN roxithromycin 150mg tablet blister pack",
        "active_ingredients": "roxithromycin",
        "dosage_form": "Tablet, film coated",
        "quantity_of_active_ingredients": "150 mg",
        "sponsor": "Alphapharm Pty Ltd",
        "phone": "1800 274 276",
        "shortage_status": "Discontinued",
        "shortage_impact_rating": "Low",
        "availability": "Unavailable",
        "reason": "Manufacturing",
        "management_action": "Alternative generic products are available.",
        "deletion_from_market": "2024-08-05",
        "supply_impact_start_date": null,
        "supply_impact_end_date": null,
        "last_updated": "2024-08-08"
    },
    {
        "artg_id": 99939,
        "artg_name": "ROXIMYCIN roxithromycin 300mg tablet blister pack",
        "active_ingredients": "roxithromycin",
        "dosage_form": "Tablet, film coated",
        "quantity_of_active_ingredients": "300 mg",
        "sponsor": "Alphapharm Pty Ltd",
        "phone": "1800 274 276",
        "shortage_status": "Discontinued",
        "shortage_impact_rating": "Medium",
        "availability": "Unavailable",
        "reason": "Manufacturing",
        "management_action": "Alternative generic products are availalbe.",
        "deletion_from_market": "2024-08-05",
        "supply_impact_start_date": null,
        "supply_impact_end_date": null,
        "last_updated": "2024-08-08"
    }
]
```

### Help

To see all available options:

```bash
uv run tga-shortage-scraper --help
```

## Output Format

The tool outputs data as formatted JSON with the following fields for each ARTG
entry:

- `artg_id`: The ARTG identification number
- `artg_name`: Full product name
- `active_ingredients`: Active pharmaceutical ingredients
- `dosage_form`: Form of the medication (tablet, capsule, etc.)
- `quantity_of_active_ingredients`: Strength/dosage information
- `sponsor`: Company responsible for the product
- `phone`: Contact phone number
- `shortage_status`: Current shortage status
- `shortage_impact_rating`: Impact severity (Low, Medium, High)
- `availability`: Current availability status
- `reason`: Reason for the shortage
- `management_action`: Actions being taken to address the shortage
- `deletion_from_market`: Date removed from market (if applicable)
- `supply_impact_start_date`: When the shortage began (if known)
- `supply_impact_end_date`: Expected resolution date (if known)
- `last_updated`: Date the information was last updated

## Data Source

This tool fetches data from the official TGA shortage database at:
<https://apps.tga.gov.au/Prod/msi/search>

## Development

### Running Tests

```bash
uv run pytest
```

### Type Checking

```bash
uv run mypy --strict tga_shortage_scraper tests/
```

### Linting

```bash
uv run ruff check tga_shortage_scraper tests
```

### Formatting

```bash
uv run ruff fmt tga_shortage_scraper tests
```
