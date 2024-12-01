# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrpcioTools(PythonPackage):
    """Protobuf code generator for gRPC"""

    homepage = "https://grpc.io/"
    pypi = "grpcio-tools/grpcio-tools-1.42.0.tar.gz"

    version("1.62.2", sha256="5fd5e1582b678e6b941ee5f5809340be5e0724691df5299aae8226640f94e18f")
    version("1.56.2", sha256="82af2f4040084141a732f0ef1ecf3f14fdf629923d74d850415e4d09a077e77a")
    version("1.48.2", sha256="8902a035708555cddbd61b5467cea127484362decc52de03f061a1a520fe90cd")
    version("1.48.1", sha256="1178f2ea531f80cc2027ec64728df6ffc8e98cf1df61652a496eafd612127183")
    version("1.42.0", sha256="d0a0daa82eb2c2fb8e12b82a458d1b7c5516fe1135551da92b1a02e2cba93422")
    version("1.39.0", sha256="39dfe7415bc0d3860fdb8dd90607594b046b88b57dbe64284efa4820f951c805")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-protobuf@3.12.0:3", when="@1.48.1:", type=("build", "run"))
    depends_on("py-protobuf@3.5.0.post1:3", type=("build", "run"))
    depends_on("py-grpcio@1.62.2:", when="@1.62.2:", type=("build", "run"))
    depends_on("py-grpcio@1.56.2:", when="@1.56.2:", type=("build", "run"))
    depends_on("py-grpcio@1.48.2:", when="@1.48.2:", type=("build", "run"))
    depends_on("py-grpcio@1.48.1:", when="@1.48.1:", type=("build", "run"))
    depends_on("py-grpcio@1.42.0:", when="@1.42.0:", type=("build", "run"))
    depends_on("py-grpcio@1.39.0:", when="@1.39.0:1.41", type=("build", "run"))
    depends_on("py-cython@0.23:", type="build")
    depends_on("openssl")
    depends_on("zlib-api")
    depends_on("c-ares")
    depends_on("re2+shared")

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
        if self.spec.satisfies("%fj"):
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
