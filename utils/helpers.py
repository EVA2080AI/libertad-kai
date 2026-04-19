"""Utilidades varias."""

def format_currency(amount: float, currency: str = 'USD') -> str:
    """Formatea una cantidad como moneda."""
    return f"${amount:.2f} {currency}"


def format_percentage(value: float) -> str:
    """Formatea un valor como porcentaje."""
    return f"{value:.2f}%"


def format_timestamp(ts: str) -> str:
    """Formatea un timestamp ISO a formato legible."""
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ts


def truncate_string(s: str, length: int = 50) -> str:
    """Trunca una cadena de texto."""
    if len(s) <= length:
        return s
    return s[:length-3] + "..."
