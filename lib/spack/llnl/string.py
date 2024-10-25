# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""String manipulation functions that do not have other dependencies than Python
standard library
"""
from typing import List, Optional


def comma_list(sequence: List[str], article: str = "") -> str:
    if type(sequence) is not list:
        sequence = list(sequence)

    if not sequence:
        return ""
    if len(sequence) == 1:
        return sequence[0]

    out = ", ".join(str(s) for s in sequence[:-1])
    if len(sequence) != 2:
        out += ","  # oxford comma
    out += " "
    if article:
        out += article + " "
    out += str(sequence[-1])
    return out


def comma_or(sequence: List[str]) -> str:
    """Return a string with all the elements of the input joined by comma, but the last
    one (which is joined by 'or').
    """
    return comma_list(sequence, "or")


def comma_and(sequence: List[str]) -> str:
    """Return a string with all the elements of the input joined by comma, but the last
    one (which is joined by 'and').
    """
    return comma_list(sequence, "and")


def ordinal(number: int) -> str:
    """Return the ordinal representation (1st, 2nd, 3rd, etc.) for the provided number.

    Args:
        number: int to convert to ordinal number

    Returns: number's corresponding ordinal
    """
    idx = (number % 10) << 1
    tens = number % 100 // 10
    suffix = "th" if tens == 1 or idx > 6 else "thstndrd"[idx : idx + 2]
    return f"{number}{suffix}"


def quote(sequence: List[str], q: str = "'") -> List[str]:
    """Quotes each item in the input list with the quote character passed as second argument."""
    return [f"{q}{e}{q}" for e in sequence]


def plural(n: int, singular: str, plural: Optional[str] = None, show_n: bool = True) -> str:
    """Pluralize <singular> word by adding an s if n != 1.

    Arguments:
        n: number of things there are
        singular: singular form of word
        plural: optional plural form, for when it's not just singular + 's'
        show_n: whether to include n in the result string (default True)

    Returns:
        "1 thing" if n == 1 or "n things" if n != 1
    """
    number = f"{n} " if show_n else ""
    if n == 1:
        return f"{number}{singular}"
    elif plural is not None:
        return f"{number}{plural}"
    else:
        return f"{number}{singular}s"
