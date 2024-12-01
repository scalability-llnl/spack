# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *  # noqa: F401
from spack.pkg.builtin.mock.cmake_client import CmakeClient


class CmakeClientInheritor(CmakeClient):
    """A dumy package that inherits from one using cmake."""
