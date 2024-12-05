# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyfits(PythonPackage):
    """The PyFITS module is a Python library providing access to
    FITS(Flexible Image Transport System) files."""

    homepage = "https://github.com/spacetelescope/pyfits"
    url = "https://github.com/spacetelescope/PyFITS/archive/3.5.tar.gz"

    version("3.5", sha256="fd32596ee09170a70ddc87d0dfc5503d860ef6b68abcff486d7aa6993dff6162")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
