from typing import Any, Callable
from typing_extensions import Doc
from enum import Enum
from typing import get_args


def get_openai_spec(f: Callable) -> dict[str, Any]:
    '''
    Example:

    >>> class TemperatureUnit(Enum):
    ...     CELSIUS = "Celsius"
    ...     FAHRENHEIT = "Fahrenheit"

    >>> def get_current_temperature(
    ...     location: Annotated[str, Doc("The city and state, e.g., San Francisco, CA")],
    ...     unit: Annotated[TemperatureUnit, Doc("The temperature unit to use")],
    ... ) -> str:
    ...     """
    ...     Get the current temperature for a specific location
    ...     """
    ...     return f"The temperature at {location} is 37 {unit}"

    >>> get_openai_spec(get_current_temperature)
    ... {
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
                    "description": "The temperature unit to use",
                },
            },
        },
    }
    '''

    def get_property_dict(annotation: Any) -> dict:
        origin_type = getattr(annotation, "__origin__", annotation)

        if origin_type is int:
            output_type = "integer"
        elif origin_type is float:
            output_type = "float"
        elif origin_type is str:
            output_type = "string"
        elif issubclass(origin_type, Enum):
            output_type = "string"
        else:
            raise ValueError(f"Invalid origin_type {origin_type}")

        docs: list[str] = [
            arg.documentation for arg in get_args(annotation) if isinstance(arg, Doc)
        ]

        return {
            "type": output_type,
            **(
                {"enum": [x.value for x in origin_type.__members__.values()]}
                if issubclass(origin_type, Enum)
                else {}
            ),
            "description": "\n".join(docs),
        }

    properties = {
        name: get_property_dict(annotation)
        for name, annotation in f.__annotations__.items()
        if name != "return"
    }
    return {
        "name": f.__name__,
        "description": (f.__doc__ or "").strip(),
        "parameters": {
            "type": "object",
            "properties": properties,
        },
    }
