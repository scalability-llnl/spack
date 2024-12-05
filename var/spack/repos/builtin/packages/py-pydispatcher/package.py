# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydispatcher(PythonPackage):
    """Multi-producer-multi-consumer signal dispatching mechanism."""

    homepage = "https://pydispatcher.sourceforge.net/"
    pypi = "PyDispatcher/PyDispatcher-2.0.5.tar.gz"

    version("2.0.5", sha256="5570069e1b1769af1fe481de6dd1d3a388492acddd2cdad7a3bde145615d5caf")

    depends_on("py-setuptools", type="build")
