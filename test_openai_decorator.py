from enum import Enum
from typing import Annotated
import json
from typing_extensions import Doc
from openai_decorator import get_openai_spec

expected_spec = {
    "name": "get_current_temperature",
    "description": "Get the current temperature for a specific location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g., San Francisco, CA",
            },
            "unit": {
                "type": "string",
                "enum": ["Celsius", "Fahrenheit"],
                "description": "The temperature unit to use. Infer this from the user's location.",
            },
        },
    },
}


class TemperatureUnit(Enum):
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"


def get_current_temperature(
    location: Annotated[str, Doc("The city and state, e.g., San Francisco, CA")],
    unit: Annotated[TemperatureUnit, Doc("The temperature unit to use")],
) -> str:
    """
    Get the current temperature for a specific location
    """
    return f"The temperature at {location} is 37 {unit}"


def main():
    spec = get_openai_spec(get_current_temperature)
    print(json.dumps(expected_spec, indent=4))
    print()
    print(json.dumps(spec, indent=4))

    # assert spec == expected_spec


if __name__ == "__main__":
    main()
