# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySyned(PythonPackage):
    """A python library to define the components of a synchrotron beamline and
    their positions. They can be read/write to json files. It is used by OASYS
    as a common tool to define sources and optical systems that are then
    exported to the different add-ons."""

    homepage = "https://github.com/oasys-kit/syned"
    git = "https://github.com/oasys-kit/syned.git"

    version("develop", branch="master")

    depends_on("py-numpy")
    depends_on("py-scipy")
    depends_on("py-setuptools")
