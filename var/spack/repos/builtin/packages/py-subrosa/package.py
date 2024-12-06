# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySubrosa(PythonPackage):
    """Subrosa is a Python implementation of Shamir's Secret Sharing. An
    algorithm for sharing a secret with a group of people without letting any
    individual of the group know the secret."""

    homepage = "https://github.com/DasIch/subrosa/"
    url = "https://github.com/DasIch/subrosa/archive/0.1.0.tar.gz"

    version("0.1.0", sha256="dc8172119a338874afa0bdcba035224c965ff71d2cbceda70b1ed2377aa390ea")

    depends_on("py-setuptools", type="build")
    depends_on("py-gf256", type=("build", "run"))
