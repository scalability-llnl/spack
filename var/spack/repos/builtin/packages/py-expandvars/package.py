# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExpandvars(PythonPackage):
    """Expand system variables Unix style."""

    homepage = "https://github.com/sayanarijit/expandvars"
    pypi = "expandvars/expandvars-0.12.0.tar.gz"

    license("MIT")

    version("0.12.0", sha256="7d1adfa55728cf4b5d812ece3d087703faea953e0c0a1a78415de9df5024d844")

    depends_on("py-hatchling", type="build")
