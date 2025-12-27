from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Кастомный обработчик исключений для возврата JSON ошибок.
    """

    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict):
            errors = []
            for field, messages in response.data.items():
                if isinstance(messages, list):
                    for message in messages:
                        errors.append(
                            {
                                "field": field if field != "non_field_errors" else None,
                                "message": str(message),
                            }
                        )
                else:
                    errors.append(
                        {
                            "field": field if field != "non_field_errors" else None,
                            "message": str(messages),
                        }
                    )

            response.data = {
                "error": {
                    "code": response.status_code,
                    "message": "Validation failed"
                    if response.status_code == 400
                    else "Error occurred",
                    "details": errors,
                }
            }

    return response

