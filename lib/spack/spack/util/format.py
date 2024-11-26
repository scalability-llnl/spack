# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Optional


def get_version_lines(version_hashes_dict: dict, url_dict: Optional[dict] = None) -> str:
    """
    Renders out a set of versions like those found in a package's
    package.py file for a given set of versions and hashes.

    Args:
        version_hashes_dict (dict): A dictionary of the form: version -> checksum.
        url_dict (dict): A dictionary of the form: version -> URL.

    Returns:
        (str): Rendered version lines.
    """
    version_lines = []

    for v, h in version_hashes_dict.items():
        version_lines.append(f'    version("{v}", sha256="{h}")')

    return "\n".join(version_lines)
