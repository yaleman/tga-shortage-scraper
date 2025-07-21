"""TGA Shortage Scraper Package"""

from typing import Optional, Dict, List
import csv
from datetime import date

from pydantic import BaseModel, Field, RootModel, model_validator

BASE_URL = "https://apps.tga.gov.au/Prod/msi/search"
# ?shortagetype=All&exportType=Excel
SHORTAGE_TYPES = [
    "All",
    "Critical",
]

EXPORT_TYPES = ["Excel"]


def get_params(
    shortage_type: Optional[str] = None, export_type: Optional[str] = None
) -> Dict[str, str]:
    """Construct the URL for the TGA Shortage Scraper."""
    if not shortage_type and not export_type:
        return {}
    params = {}

    if shortage_type:
        if shortage_type not in SHORTAGE_TYPES:
            raise ValueError(f"Invalid shortage type: {shortage_type}")
        params["shortagetype"] = shortage_type
    if export_type:
        if export_type not in EXPORT_TYPES:
            raise ValueError(f"Invalid export type: {export_type}")
        params["exportType"] = export_type
    return params


class ArtgData(BaseModel):
    """Data model for ARTG Shortage information."""

    artg_id: int = Field(alias="ARTG ID")
    artg_name: str = Field(alias="ARTG name")
    active_ingredients: str = Field(alias="Active ingredients")
    dosage_form: str = Field(alias="Dosage form")
    quantity_of_active_ingredients: str = Field(alias="Quantity of active ingredients")
    sponsor: str = Field(alias="Sponsor")
    phone: str = Field(alias="Phone")
    shortage_status: str = Field(alias="Shortage status")
    shortage_impact_rating: str = Field(alias="Shortage impact rating")
    availability: str = Field(alias="Availability")
    reason: str = Field(alias="Reason")
    management_action: str = Field(alias="Management action")
    deletion_from_market: Optional[date] = Field(alias="Deletion from market")
    supply_impact_start_date: Optional[date] = Field(alias="Supply impact start date")
    supply_impact_end_date: Optional[date] = Field(alias="Supply impact end date")
    last_updated: Optional[date] = Field(alias="Last updated")

    @model_validator(mode="before")
    def validate_dates(cls, values: Dict[str, str]) -> Dict[str, str]:  # pylint: disable=no-self-argument
        """Convert date strings to date objects."""
        for field in [
            "Supply impact start date",
            "Supply impact end date",
            "Last updated",
            "Deletion from market",
        ]:
            if field in values and values[field].strip() != "":
                date_string = values[field].split("/")
                values[field] = date(  # type: ignore[assignment]
                    year=int(date_string[2]),
                    month=int(date_string[1]),
                    day=int(date_string[0]),
                )
            else:
                values[field] = None  # type: ignore[assignment]
        return values


ArtgResults = RootModel[List[ArtgData]]


def handle_csv(
    lines: List[str], ingredient: Optional[str], search: Optional[str]
) -> ArtgResults:
    """Parse the CSV response text into a JSON object."""
    data = []

    search_keywords = search.lower().split() if search else []

    csv_reader = csv.DictReader(lines)
    for row in csv_reader:
        row_data = ArtgData.model_validate(row)
        if ingredient is not None and (
            (ingredient.lower() not in row_data.active_ingredients.lower())
            or (ingredient.lower() not in row_data.artg_name.lower())
        ):
            continue
        if search_keywords and not all(
            keyword in row_data.artg_name.lower() for keyword in search_keywords
        ):
            continue
        data.append(row_data)

    return ArtgResults.model_validate(data)
