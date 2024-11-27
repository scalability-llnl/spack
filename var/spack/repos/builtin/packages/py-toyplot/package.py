# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyToyplot(PythonPackage):
    """A modern plotting toolkit supporting electronic publishing and reproducibility."""

    homepage = "https://github.com/sandialabs/toyplot"
    pypi = "toyplot/toyplot-0.19.0.tar.gz"

    maintainers("snehring")

    license("BSD-3-Clause")

    version("1.0.3", sha256="7b7b2bc5784fd75e5c695300bffc80d568c83bebef543bb54e6e6c2229912edd")
    version("0.19.0", sha256="d199b4ac2d5ee454fec8be937bd9f1a313145545adc192bb0db2fd3defada484")

    depends_on("py-setuptools", type="build")

    depends_on("py-arrow@1.0:", type=("build", "run"))
    depends_on("py-custom-inherit", type=("build", "run"))
    depends_on("py-multipledispatch", type=("build", "run"))
    depends_on("py-numpy@1.8.0:", type=("build", "run"))
    depends_on("py-pypng", type=("build", "run"))
    depends_on("py-reportlab", type=("build", "run"))
