# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pystring(CMakePackage):
    """Pystring is a collection of C++ functions which match the interface and behavior
    of python's string class methods using std::string."""

    git = "https://github.com/imageworks/pystring"
    url = "https://github.com/imageworks/pystring/archive/refs/tags/v1.1.4.tar.gz"

    license("Apache-2.0")

    version("1.1.4", sha256="49da0fe2a049340d3c45cce530df63a2278af936003642330287b68cefd788fb")

    # Core dependencies
    depends_on("cmake@3.27.9:", type="build")
