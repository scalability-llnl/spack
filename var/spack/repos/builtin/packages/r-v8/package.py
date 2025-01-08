# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RV8(RPackage):
    """Embedded JavaScript and WebAssembly Engine for R.

    An R interface to V8: Google's open source JavaScript and WebAssembly
    engine. This package can be compiled either with V8 version 6 and up or
    NodeJS when built as a shared library."""

    cran = "V8"

    version("5.0.0", sha256="668fb759f973016e1e6aae21d711e83226d6895b43b2476c77feadf47896b21a")
    version("4.3.0", sha256="7e395c4faed0d2a9d647820269d2d374953fc67c6108d57d63e93ec570dbe0d0")
    version("4.2.2", sha256="50653527198637a37c010052f394839f50a3c643975aac1d04e42d36f8e5313b")
    version("4.2.1", sha256="99881af4798d11da0adccd8e4e1aa5dc4adccf5e3572724c14f6f90c2b8c3ff0")
    version("4.2.0", sha256="6c62fdc974cc30fa975cad4ccb1e3796112fc2490a807f6e3d7878c3a5544743")
    version("4.0.0", sha256="146a4cb671264f865ac2f2e35bfdfb37e2df70e4f6784354fb6e8a80a19dbbc8")
    version("3.6.0", sha256="a3969898bf4a7c13d3130fae0d385cd048d46372ff4a412917b914b159261377")
    version(
        "3.4.0",
        sha256="f5c8a2a03cc1be9f504f47711a0fcd1b962745139c9fb2a10fbd79c4ae103fbd",
        deprecated=True,
    )

    depends_on("r-rcpp@0.12.12:", type=("build", "run"))
    depends_on("r-jsonlite@1.0:", type=("build", "run"))
    depends_on("r-curl@1.0:", type=("build", "run"))

    conflicts("@3.4.0", when="target=aarch64:")
    conflicts("@3.4.0", when="%gcc@5:")

    def setup_build_environment(self, env):
        spec = self.spec
        if (spec.platform == "darwin") or (
            spec.platform == "linux" and spec.target.family == "x86_64"
        ):
            env.append_flags("DOWNLOAD_STATIC_LIBV8", "1")
