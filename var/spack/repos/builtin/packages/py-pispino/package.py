# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPispino(PythonPackage):
    """PISPINO (PIpits SPIN-Off tools)."""

    homepage = "https://github.com/hsgweon/pispino"
    url = "https://github.com/hsgweon/pispino/archive/1.1.tar.gz"

    version("1.1", sha256="8fb2e1c0ae38ecca7c637de9c0b655eb18fc67d7838ceb5a6902555ea12416c0")

    # https://github.com/bioconda/bioconda-recipes/blob/master/recipes/pispino/meta.yaml
    depends_on("py-setuptools", type="build")
    depends_on("vsearch", type="run")
    depends_on("fastx-toolkit", type="run")
