# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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
