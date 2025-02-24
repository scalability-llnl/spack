# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQuickjsr(RPackage):
    """An 'R' interface to the 'QuickJS' portable 'JavaScript' engine.
    The engine and all 'R' to 'JavaScript' interoperability is bundled
    within the package, requiring no dependencies beyond a 'C' compiler."""

    homepage = "https://bellard.org/quickjs/"
    cran = "QuickJSR"

    license("MIT", checked_by="wdconinc")

    version("1.3.1", sha256="10559d6e84a838ec97acdbc6028a59e2121811d4a20e83c95cdb8fb4ce208fd1")
