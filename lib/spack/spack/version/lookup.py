# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Optional, Tuple


class AbstractRefLookup:
    def get(self, ref) -> Tuple[Optional[str], int]:
        """Get the version string and distance for a given git ref.

        Args:
            ref (str): git ref to lookup

        Returns: optional version string and distance"""
        return None, 0
