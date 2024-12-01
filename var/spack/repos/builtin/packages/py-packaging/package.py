# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPackaging(PythonPackage):
    """Core utilities for Python packages."""

    homepage = "https://github.com/pypa/packaging"
    pypi = "packaging/packaging-19.2.tar.gz"

    license("BSD-2-Clause")
    version("24.1", sha256="026ed72c8ed3fcce5bf8950572258698927fd1dbda10a5e981cdf0ac37f4f002")
    version("23.2", sha256="048fb0e9405036518eaaf48a55953c750c11e1a1b68e0dd1a9d62ed0c092cfc5")
    version("23.1", sha256="a392980d2b6cffa644431898be54b0045151319d1e7ec34f0cfed48767dd334f")
    version("23.0", sha256="b6ad297f8907de0fa2fe1ccbd26fdaf387f5f47c7275fedf8cce89f99446cf97")
    version("21.3", sha256="dd47c42927d89ab911e606518907cc2d3a1f38bbd026385970643f9c5b8ecfeb")
    version("21.0", sha256="7dc96269f53a4ccec5c0670940a4281106dd0bb343f47b7471f779df49c2fbe7")
    version("20.9", sha256="5b327ac1320dc863dca72f4514ecc086f31186744b84a230374cc1fd776feae5")
    version("19.2", sha256="28b924174df7a2fa32c1953825ff29c61e2f5e082343165438812f00d3a7fc47")
    version("19.1", sha256="c491ca87294da7cc01902edbe30a5bc6c4c28172b5138ab4e4aa1b9d7bfaeafe")
    version("19.0", sha256="0c98a5d0be38ed775798ece1b9727178c4469d9c3b4ada66e8e6b7849f8732af")
    version("17.1", sha256="f019b770dd64e585a99714f1fd5e01c7a8f11b45635aa953fd41c689a657375b")
    version("16.8", sha256="5d50835fdf0a7edf0b55e311b7c887786504efea1177abd7e69329a8e5ea619e")

    depends_on("py-flit-core@3.3:", when="@22:", type="build")

    # Needed to bootstrap Spack correctly on Python 3.6 (rhel8 platform-python)
    depends_on("python@3.7:", when="@22:", type=("build", "run"))
    depends_on("python@3.8:", when="@24.1", type=("build", "run"))

    # Historical dependencies
    depends_on("py-setuptools@40.8.0:", when="@20.8:21", type="build")
    depends_on("py-setuptools", when="@:20.7", type="build")
    depends_on("py-pyparsing@2.0.2:3.0.4,3.0.6:", when="@21.3:21", type=("build", "run"))
    depends_on("py-pyparsing@2.0.2:2", when="@21.1:21.2", type=("build", "run"))
    depends_on("py-pyparsing@2.0.2:", when="@:21.0", type=("build", "run"))
    depends_on("py-six", when="@:20.7", type=("build", "run"))
    depends_on("py-attrs", when="@19.1", type=("build", "run"))
