# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyModred(PythonPackage):
    """Modred is a parallelized library for finding
    modal decompositions and reduced-order models.
    """

    homepage = "https://github.com/belson17/modred"
    git = "https://github.com/belson17/modred.git"

    license("BSD-2-Clause")

    version("2.0.4", tag="v2.0.4", commit="b793efd353434799ec8c4c350757037f87dcf99a")
    version("2.0.3", tag="v2.0.3", commit="70f61fddf4192a33952f5c98103d2b90955c4e79")
    version("2.0.2", tag="v2.0.2", commit="674d6962f87c93697e4cbb4efd0785cd3398c4b1")
    version("2.0.1", tag="v2.0.1", commit="a557e72d6416b4beefd006ab3e90df7ae1ec6ddd")
    version("2.0.0", tag="v2.0.0", commit="ebf219ccedb3d753fad825d9b20ac9b14b84f404")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type="run")

    patch("v2x-setuptools-8.0.patch", when="@2: ^py-setuptools@8.0:")
