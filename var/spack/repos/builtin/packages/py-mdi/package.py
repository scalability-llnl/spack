# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMdi(PythonPackage):
    """MolSSI Driver Interface (MDI) Library

    The MolSSI Driver Interface (MDI) project provides a standardized API for
    fast, on-the-fly communication between computational chemistry codes. This
    greatly simplifies the process of implementing methods that require the
    cooperation of multiple software packages and enables developers to write a
    single implementation that works across many different codes.
    """

    homepage = "https://molssi-mdi.github.io/MDI_Library"
    git = "https://github.com/MolSSI-MDI/MDI_Library.git"
    url = "https://github.com/MolSSI-MDI/MDI_Library/archive/refs/tags/v1.4.30.tar.gz"

    maintainers("hjjvandam")

    license("BSD-3-Clause", checked_by="hjjvandam")

    version(
        "1.4.30",
        sha256="96681171b3735cb1c413311ff44fbcb4401841ffcdbf0c1f395e737a5fab52e8",
        extension="tar.gz",
        url="https://codeload.github.com/MolSSI-MDI/MDI_Library/tar.gz/refs/tags/v1.4.30",
    )

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-packaging", type="build")
    depends_on("cmake", type="build")
