from unidecode import unidecode


def custom_slugify(value: str) -> str:
    """Преобразует строку в slug, заменяя пробелы на дефисы и приводя к нижнему регистру."""
    slug = unidecode(value).replace(" ", "-").lower().replace("'", "")
    return slug
