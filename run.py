"""
Entry point to run the travel agent for a given city.
"""
import argparse

from graph import app


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a 1-day travel plan: attractions, weather summary, and itinerary."
    )
    parser.add_argument(
        "city",
        nargs="?",
        default="Tunis",
        help="City to plan the trip for (default: Tunis)",
    )
    args = parser.parse_args()

    result = app.invoke({"city": args.city})

    print("Top Attractions:", result.get("attractions"))
    print("\nWeather Summary:", result.get("weather"))
    print("\nItinerary:", result.get("itinerary"))


if __name__ == "__main__":
    main()
