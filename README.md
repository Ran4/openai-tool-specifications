Python decorator and helper functions for generating openai tool specifications.

Example:

```python
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

print(get_openai_spec(get_current_temperature))
```

Output:

```json
{
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
```
