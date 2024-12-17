# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other: object
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Any

from typing_extensions import Protocol


class SupportsRichComparison(Protocol):
    """Objects that support =, !=, <, <=, >, and >=."""

    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError

    def __ne__(self, other: Any) -> bool:
        raise NotImplementedError

    def __lt__(self, other: Any) -> bool:
        raise NotImplementedError

    def __le__(self, other: Any) -> bool:
        raise NotImplementedError

    def __gt__(self, other: Any) -> bool:
        raise NotImplementedError

    def __ge__(self, other: Any) -> bool:
        raise NotImplementedError
