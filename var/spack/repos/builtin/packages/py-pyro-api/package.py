# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyroApi(PythonPackage):
    """Generic API for dispatch to Pyro backends."""

    homepage = "https://github.com/pyro-ppl/pyro-api"
    pypi = "pyro-api/pyro-api-0.1.2.tar.gz"

    version("0.1.2", sha256="a1b900d9580aa1c2fab3b123ab7ff33413744da7c5f440bd4aadc4d40d14d920")

    depends_on("py-setuptools", type="build")
