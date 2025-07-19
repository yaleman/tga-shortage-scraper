from typing import Optional
import requests
import click

from tga_shortage_scraper import get_params, handle_csv, BASE_URL


@click.command()
@click.option("--ingredient", help="Search for an active ingredient.")
def main(ingredient: Optional[str]) -> None:
    """Main function to run the TGA Shortage Scraper."""

    # Create a session
    session = requests.Session()

    # Get parameters for the request
    params = get_params(shortage_type="All", export_type="Excel")

    # Make the request and print the response
    response = session.get(BASE_URL, params=params)
    try:
        # skip the excel headers
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.reason}")
            return
        if not response.text:
            print("No data found.")
            return
        # Check if the response is empty
        if response.text.strip() == "":
            print("No data found.")
            return
        # there's an excel header and TGA info in the first 10 lines, so skip them
        response_text = response.text.strip().splitlines()[10:]

        # the response is a csv, so parse it into json
        results = handle_csv(response_text, ingredient=ingredient)

        print(results.model_dump_json(indent=2))
    except BrokenPipeError:
        # Handle the case where the output is piped and the pipe is closed
        return


if __name__ == "__main__":
    main()
