# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List, Tuple


def tokenize_flags(flags_values: str, propagate: bool = False) -> List[Tuple[str, bool]]:
    """Given a compiler flag specification as a string, this returns a list
    where the entries are the flags. For compiler options which set values
    using the syntax "-flag value", this function groups flags and their
    values together. Any token not preceded by a "-" is considered the
    value of a prior flag."""
    tokens = flags_values.split()
    if not tokens:
        return []
    flag = tokens[0]
    flags_with_propagation = []
    for token in tokens[1:]:
        if not token.startswith("-"):
            flag += " " + token
        else:
            flags_with_propagation.append((flag, propagate))
            flag = token
    flags_with_propagation.append((flag, propagate))
    return flags_with_propagation
