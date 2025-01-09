# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Tuple, Union

from spack.version import GitVersion, StandardVersion


def concretization_version_order(version_info: Tuple[Union[GitVersion, StandardVersion], dict]):
    """Version order key for concretization, where preferred > not preferred,
    not deprecated > deprecated, finite > any infinite component; only if all are
    the same, do we use default version ordering."""
    version, info = version_info
    return (
        info.get("preferred", False),
        not info.get("deprecated", False),
        not version.isdevelop(),
        not version.is_prerelease(),
        version,
    )
