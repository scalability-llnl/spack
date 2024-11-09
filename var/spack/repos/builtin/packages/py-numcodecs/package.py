# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumcodecs(PythonPackage):
    """Numcodecs is a Python package providing buffer compression and
    transformation codecs for use in data storage and communication
    applications.
    """

    homepage = "https://github.com/zarr-developers/numcodecs"
    pypi = "numcodecs/numcodecs-0.6.4.tar.gz"
    git = "https://github.com/zarr-developers/numcodecs.git"

    # 'numcodecs.tests' excluded from 'import_modules' because it requires
    # an additional dependency on 'pytest'
    import_modules = ["numcodecs"]

    license("MIT")

    version("main", branch="main", submodules=True)
    version("master", branch="main", submodules=True, deprecated=True)
    version("0.13.0", sha256="ba4fac7036ea5a078c7afe1d4dffeb9685080d42f19c9c16b12dad866703aa2e")
    version("0.12.1", sha256="05d91a433733e7eef268d7e80ec226a0232da244289614a8f3826901aec1098e")
    version("0.12.0", sha256="6388e5f4e94d18a7165fbd1c9d3637673b74157cff8bc644005f9e2a4c717d6e")
    version("0.11.0", sha256="6c058b321de84a1729299b0eae4d652b2e48ea1ca7f9df0da65cb13470e635eb")
    version("0.7.3", sha256="022b12ad83eb623ec53f154859d49f6ec43b15c36052fa864eaf2d9ee786dd85")
    version("0.6.4", sha256="ef4843d5db4d074e607e9b85156835c10d006afc10e175bda62ff5412fca6e4d")

    depends_on("c", type="build")  # generated

    variant("msgpack", default=False, description="Codec to encode data as msgpacked bytes.")

    depends_on("python@3.10:", when="@0.13:", type=("build", "link", "run"))
    depends_on("python@3.8:", when="@0.11:0.12", type=("build", "link", "run"))
    depends_on("python@3.6:3", when="@0.7:0.10", type=("build", "link", "run"))
    depends_on("py-setuptools@64:", when="@0.11:", type="build")
    depends_on("py-setuptools@18.1:", type="build")
    depends_on("py-setuptools-scm@6.2: +toml", when="@0.11:", type="build")
    depends_on("py-setuptools-scm@1.5.5: +toml", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    # https://github.com/zarr-developers/numcodecs/issues/521
    depends_on("py-numpy@:1", when="@:0.12.0", type=("build", "run"))
    depends_on("py-py-cpuinfo", when="@0.11:", type="build")
    depends_on("py-entrypoints", when="@0.10.1:0.11", type=("build", "run"))
    depends_on("py-msgpack", type=("build", "run"), when="+msgpack")

    patch("apple-clang-12.patch", when="%apple-clang@12:")

    # TODO: this package should really depend on blosc, zstd, lz4, zlib, but right now it vendors
    # those libraries without any way to use the system versions.
    # https://github.com/zarr-developers/numcodecs/issues/464

    def setup_build_environment(self, env):
        # This package likes to compile natively by checking cpu features and then setting flags
        # -msse2 and -mavx2, which we want to avoid in Spack. This could go away if the package
        # supports external libraries.
        if self.spec.satisfies("target=x86_64:"):
            if "avx2" not in self.spec.target.features:
                env.set("DISABLE_NUMCODECS_AVX2", "1")
            if "sse2" not in self.spec.target.features:
                env.set("DISABLE_NUMCODECS_SSE2", "1")

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%oneapi"):
                flags.append("-Wno-error=implicit-function-declaration")
        return (flags, None, None)
