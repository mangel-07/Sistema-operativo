import re

from models.base_algorithm import PageReference


_REFERENCE_PATTERN = re.compile(r"(\d+)(?:\s*:\s*([RW]))?", re.IGNORECASE)
MAX_REFERENCES = 20
MAX_FRAME_COUNT = 4


def parse_references(raw: str) -> list[PageReference]:
    tokens = raw.split(",")
    if not raw.strip() or any(not token.strip() for token in tokens):
        raise ValueError("Escribe referencias separadas por comas, por ejemplo: 1, 2, 3.")
    if len(tokens) > MAX_REFERENCES:
        raise ValueError(f"La cadena de referencia admite máximo {MAX_REFERENCES} referencias.")

    references: list[PageReference] = []
    for token in tokens:
        match = _REFERENCE_PATTERN.fullmatch(token.strip())
        if match is None:
            raise ValueError(
                f"Referencia no válida: «{token.strip()}». Usa números o número:R/número:W."
            )
        references.append(
            PageReference(int(match.group(1)), (match.group(2) or "R").upper())
        )
    return references


def parse_frame_count(raw: str) -> int:
    try:
        frame_count = int(raw.strip())
    except ValueError as error:
        raise ValueError("El número de marcos debe ser un entero.") from error
    if not 1 <= frame_count <= MAX_FRAME_COUNT:
        raise ValueError(f"El número de marcos debe estar entre 1 y {MAX_FRAME_COUNT}.")
    return frame_count