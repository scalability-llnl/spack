# Copyright Spack Project Developers. See COPYRIGHT file for details.
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

    maintainers("hjjvandam", "rbberger")

    license("BSD-3-Clause", checked_by="hjjvandam")

    version("1.4.33", tag="v1.4.33", commit="f479f18f8d036bd675ba628365dd5f6f0cff1c21")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-packaging", type="build")
    depends_on("cmake@3.5:", type="build")
