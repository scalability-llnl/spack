# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIni(RPackage):
    """Read and Write '.ini' Files.

    Parse simple '.ini' configuration files to an structured list. Users can
    manipulate this resulting list with lapply() functions. This same
    structured list can be used to write back to file after modifications."""

    cran = "ini"

    license("GPL-3.0-only")

    version("0.3.1", sha256="7b191a54019c8c52d6c2211c14878c95564154ec4865f57007953742868cd813")
