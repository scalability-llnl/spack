# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAutoray(PythonPackage):
    """Write backend agnostic numeric code compatible with any numpy-ish array library."""

    homepage = "https://github.com/jcmgray/autoray"
    pypi = "autoray/autoray-0.5.3.tar.gz"

    license("Apache-2.0")

    version("0.6.12", sha256="721328aa06fc3577155d988052614a7b4bd6e4d01b340695344031ee4abd2a1e")
    version("0.6.11", sha256="23e6dc013913de318952580cfbf054920ebd5eacd060fc48edebb678307b4b0d")
    version("0.6.10", sha256="afff46ed3a001daad1bed917aecda75a8f0d36c0c8823eed877db4e8d55a8b20")
    version("0.6.9", sha256="9f41759f6a286bc280c4f6aece436da1c87ce75eb00efe7dc7319860c43654fa")
    version("0.6.8", sha256="8e31832597cb2075e5f9f65894fafff9d726d9287718415d3c8b008e592f0197")
    version("0.6.7", sha256="8945cfdf3aa8a35f9fe1abc03d84925db61f58bbd386623206dd8e9ba1d9e377")
    version("0.6.6", sha256="a31cd03f983a6e80b58f40618a652b7979fa09c762050f5dc4b7e6b6a0a3b62d")
    version("0.6.5", sha256="093f151539769b03374f67bd2296cf76d359ac190ab6fd8ebe26984a2dc88a4c")
    version("0.6.4", sha256="b8e38ff87e2ea1dd8bd17ddd1174f02c41dc4cfec933a3aac9f0516288548e81")
    version("0.6.3", sha256="6729f49c8787778fd8bc2a3b57a625c8c21577c6e92628cad4b13aefd7531355")
    version("0.6.1", sha256="857cbd4d60d47511ab9956f8765d5fd3c68a538d317cda7d829b00982c599140")
    version("0.6.0", sha256="ba3f30812549209bbba9d4976528f3f84bf84c22374699fd2e6aa84bf496d295")
    version("0.5.3", sha256="ecbecbc1ab65dd704234b3307fa7c7a511a36f6b9339a0ffcdaa4e5a7aab826b")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@45:", type="build")
    depends_on("py-setuptools-scm@6.2:+toml", type="build")
