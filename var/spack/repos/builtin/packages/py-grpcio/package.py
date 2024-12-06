# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrpcio(PythonPackage):
    """HTTP/2-based RPC framework."""

    homepage = "https://grpc.io/"
    pypi = "grpcio/grpcio-1.32.0.tar.gz"

    license("Apache-2.0")

    version("1.64.0", sha256="257baf07f53a571c215eebe9679c3058a313fd1d1f7c4eede5a8660108c52d9c")
    version("1.63.0", sha256="f3023e14805c61bc439fb40ca545ac3d5740ce66120a678a3c6c2c55b70343d1")
    version("1.62.2", sha256="c77618071d96b7a8be2c10701a98537823b9c65ba256c0b9067e0594cdbd954d")
    version("1.60.1", sha256="dd1d3a8d1d2e50ad9b59e10aa7f07c7d1be2b367f3f2d33c5fade96ed5460962")
    version("1.56.2", sha256="0ff789ae7d8ddd76d2ac02e7d13bfef6fc4928ac01e1dcaa182be51b6bcc0aaa")
    version(
        "1.52.0",
        sha256="a5d4a83d29fc39af429c10b9b326c174fec49b73398e4a966a1f2a4f30aa4fdb",
        deprecated=True,  # https://github.com/grpc/grpc/issues/32306
    )
    version("1.48.2", sha256="90e5da224c6b9b23658adf6f36de6f435ef7dbcc9c5c12330314d70d6f8de1f7")
    version(
        "1.48.1",
        sha256="660217eccd2943bf23ea9a36e2a292024305aec04bf747fbcff1f5032b83610e",
        deprecated=True,  # https://github.com/grpc/grpc/issues/30372
    )
    version("1.43.0", sha256="735d9a437c262ab039d02defddcb9f8f545d7009ae61c0114e19dda3843febe5")
    version("1.42.0", sha256="4a8f2c7490fe3696e0cdd566e2f099fb91b51bc75446125175c55581c2f7bc11")
    version("1.39.0", sha256="57974361a459d6fe04c9ae0af1845974606612249f467bbd2062d963cb90f407")
    version("1.38.1", sha256="1f79d8a24261e3c12ec3a6c25945ff799ae09874fd24815bc17c2dc37715ef6c")
    version("1.38.0", sha256="abbf9c8c3df4d5233d5888c6cfa85c1bb68a6923749bd4dd1abc6e1e93986f17")
    version("1.37.1", sha256="df8305806311d3fe913d4f7eb3ef28e2072159ea12f95baab5d447f1380a71e3")
    version("1.37.0", sha256="b3ce16aa91569760fdabd77ca901b2288152eb16941d28edd9a3a75a0c4a8a85")
    version("1.36.0", sha256="70b11805bc9385fcd24e15bcdc5bd8bed463026cd2227d9fdd1ebda612ba0cd9")
    version("1.35.0", sha256="7bd0ebbb14dde78bf66a1162efd29d3393e4e943952e2f339757aa48a184645c")
    version("1.34.1", sha256="1c746a3cd8a830d8d916a9d0476a786aaa98c5cc2a096344af2be955e439f8ac")
    version("1.34.0", sha256="f98f746cacbaa681de0bcd90d7aa77b440e3e1327a9988f6a2b580d54e27d4c3")
    version("1.33.2", sha256="21265511880056d19ce4f809ce3fbe2a3fa98ec1fc7167dbdf30a80d3276202e")
    version("1.33.1", sha256="f19782ec5104599382a0f73f2dfea465d0e65f6818bb3c49ca672b97034c64c3")
    version("1.32.0", sha256="01d3046fe980be25796d368f8fc5ff34b7cf5e1444f3789a017a7fe794465639")
    version("1.30.0", sha256="e8f2f5d16e0164c415f1b31a8d9a81f2e4645a43d1b261375d6bab7b0adf511f")
    version("1.29.0", sha256="a97ea91e31863c9a3879684b5fb3c6ab4b17c5431787548fc9f52b9483ea9c25")
    version("1.28.1", sha256="cbc322c5d5615e67c2a15be631f64e6c2bab8c12505bc7c150948abdaa0bdbac")
    version("1.27.2", sha256="5ae532b93cf9ce5a2a549b74a2c35e3b690b171ece9358519b3039c7b84c887e")
    version("1.25.0", sha256="c948c034d8997526011960db54f512756fb0b4be1b81140a15b4ef094c6594a4")
    version(
        "1.16.0",
        sha256="0cc5f2d3ee21c642d8982f197c83053fd3a8cbcd6a60240d8c87c6c256b10d57",
        deprecated=True,
        # Released 6ish years ago and does not install for python 3.8 with gcc11
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    with default_args(type=("build", "run")):
        depends_on("py-coverage@4:")
        depends_on("py-wheel@0.29:")

        depends_on("py-cython@3:", when="@1.63.0:")
        depends_on("py-cython@0.29.8:2", when="@1.56.0:1.62")
        depends_on("py-cython@0.29.8:", when="@1.49.0:1.55")
        # States dependency in setup.py >=0.23
        # Package states >=0.23 but doesn't compile w/ >=3
        depends_on("py-cython@0.23:2", when="@:1.48")

        depends_on("py-protobuf@5.26.1:5", when="@1.63.0:")
        depends_on("py-protobuf@4.21.3:4", when="@1.49.0:1.62")
        depends_on("py-protobuf@3.5.0:3", when="@:1.48")

        depends_on("py-six@1.10:", when="@:1.48")

    depends_on("openssl")
    depends_on("zlib-api")
    depends_on("c-ares")
    depends_on("re2+shared")

    patch("30522.diff", when="@1.48")  # https://github.com/grpc/grpc/issues/30372

    def setup_build_environment(self, env):
        env.set("GRPC_PYTHON_BUILD_WITH_CYTHON", True)
        env.set("GRPC_PYTHON_BUILD_SYSTEM_OPENSSL", True)
        env.set("GRPC_PYTHON_BUILD_SYSTEM_ZLIB", True)
        env.set("GRPC_PYTHON_BUILD_SYSTEM_CARES", True)
        env.set("GRPC_PYTHON_BUILD_SYSTEM_RE2", True)
        # https://github.com/grpc/grpc/pull/24449
        env.set("GRPC_BUILD_WITH_BORING_SSL_ASM", "")
        env.set("GRPC_PYTHON_BUILD_EXT_COMPILER_JOBS", str(make_jobs))

        for dep in self.spec.dependencies(deptype="link"):
            query = self.spec[dep.name]
            for p in query.libs.directories:
                env.prepend_path("LIBRARY_PATH", p)
            for p in query.headers.directories:
                env.prepend_path("CPATH", p)

    def patch(self):
        filter_file("-std=gnu99", "", "setup.py")

        # use the spack packages
        filter_file(
            r"(\s+SSL_INCLUDE = ).*",
            r"\1('{0}',)".format(self.spec["openssl"].prefix.include),
            "setup.py",
        )
        filter_file(
            r"(\s+ZLIB_INCLUDE = ).*",
            r"\1('{0}',)".format(self.spec["zlib-api"].prefix.include),
            "setup.py",
        )
        filter_file(
            r"(\s+CARES_INCLUDE = ).*",
            r"\1('{0}',)".format(self.spec["c-ares"].prefix.include),
            "setup.py",
        )
        filter_file(
            r"(\s+RE2_INCLUDE = ).*",
            r"\1('{0}',)".format(self.spec["re2"].prefix.include),
            "setup.py",
        )
