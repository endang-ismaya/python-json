import sys
from inspect import signature
from typing import Any, Type, Union, get_args, get_origin


def get_constructor_type_hints(cls):
    """
    Extracts type hints from the constructor (__init__) of the given class.
    Resolves forward references.
    """
    init_signature = signature(cls.__init__)
    return {
        param: param_type.annotation
        for param, param_type in init_signature.parameters.items()
        if param != "self" and param_type.annotation != param_type.empty
    }


def resolve_forward_references(cls, prop_type):
    """
    Resolves forward references for a property type.
    """
    if isinstance(prop_type, str):
        try:
            # Use the class's module to resolve the reference
            module = sys.modules[cls.__module__]
            resolved = eval(prop_type, module.__dict__)
            return resolved
        except (NameError, AttributeError):
            raise ValueError(
                f"Unable to resolve forward reference for: {prop_type}"
            )
    return prop_type


def validate_object_json(json_data: dict, cls: Type[Any]) -> bool:
    """
    Validates if the given JSON data conforms to the structure and data types
    of the specified class. Returns True if valid, otherwise returns a list of
    errors.
    """
    errors = []

    # Get the type hints from the class constructor
    annotations = get_constructor_type_hints(cls)

    for prop, prop_type in annotations.items():
        prop_type = resolve_forward_references(cls, prop_type)

        print(
            f"Validating property: {prop}, Expected type: {prop_type}, Value: {json_data.get(prop)}"
        )

        if prop not in json_data:
            errors.append(f"Missing property: {prop}")
            continue

        value = json_data[prop]
        origin = get_origin(prop_type)
        args = get_args(prop_type)

        # Handle lists (e.g., List[str], List[Review])
        if origin is list:
            if not isinstance(value, list):
                errors.append(f"{prop} should be a list")
            else:
                inner_type = args[0]  # Get the type inside List
                for i, item in enumerate(value):
                    print(
                        f"Validating list item {i}: {item}, Expected type: {inner_type}"
                    )
                    if hasattr(inner_type, "__annotations__"):
                        nested_errors = validate_object_json(item, inner_type)
                        errors.extend(
                            [f"{prop}[{i}].{e}" for e in nested_errors]
                        )
                    elif not isinstance(item, inner_type):
                        errors.append(
                            f"{prop}[{i}] should be of type {inner_type}"
                        )

        # Handle user-defined classes (e.g., Price, Review)
        elif hasattr(prop_type, "__annotations__"):
            if not isinstance(value, dict):
                errors.append(
                    f"{prop} should be an object of type {prop_type.__name__}"
                )
            else:
                nested_errors = validate_object_json(value, prop_type)
                if (
                    nested_errors is not True
                ):  # Only extend if errors are found
                    errors.extend([f"{prop}.{e}" for e in nested_errors])

        # Handle Union types (e.g., Union[int, None])
        elif origin is Union:
            if not any(
                isinstance(value, t) for t in args if t is not type(None)
            ):
                errors.append(f"{prop} should be one of types {args}")

        # Handle primitive types
        else:
            if not isinstance(value, prop_type):
                # Allow conversion for floats
                if prop_type is float and isinstance(value, str):
                    try:
                        # Attempt to convert the string to a float
                        float_value = float(value)
                        # Check if the float value, when converted back to a string, matches the original string
                        if str(float_value) != value:
                            errors.append(
                                f"{prop} should be a float, but got invalid value: {value}"
                            )
                    except ValueError:
                        # If conversion fails, mark as invalid float
                        errors.append(
                            f"{prop} should be a float, but got invalid value: {value}"
                        )

    print(f"Errors: {errors}")
    return errors if errors else True
