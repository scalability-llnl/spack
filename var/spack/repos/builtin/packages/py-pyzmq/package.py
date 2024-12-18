# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyzmq(PythonPackage):
    """PyZMQ: Python bindings for zeromq."""

    homepage = "https://github.com/zeromq/pyzmq"
    pypi = "pyzmq/pyzmq-22.3.0.tar.gz"

    license("BSD-3-Clause")

    version("26.2.0", sha256="070672c258581c8e4f640b5159297580a9974b026043bd4ab0470be9ed324f1f")
    version("26.1.1", sha256="a7db05d8b7cd1a8c6610e9e9aa55d525baae7a44a43e18bc3260eb3f92de96c6")
    version("26.0.3", sha256="dba7d9f2e047dfa2bca3b01f4f84aa5246725203d6284e3790f2ca15fba6b40a")
    version("25.1.2", sha256="93f1aa311e8bb912e34f004cf186407a4e90eec4f0ecc0efd26056bf7eda0226")
    version("25.0.2", sha256="6b8c1bbb70e868dc88801aa532cae6bd4e3b5233784692b786f17ad2962e5149")
    version("24.0.1", sha256="216f5d7dbb67166759e59b0479bca82b8acf9bed6015b526b8eb10143fb08e77")
    version("22.3.0", sha256="8eddc033e716f8c91c6a2112f0a8ebc5e00532b4a6ae1eb0ccc48e027f9c671c")
    version("18.1.0", sha256="93f44739db69234c013a16990e43db1aa0af3cf5a4b8b377d028ff24515fbeb3")
    version("18.0.1", sha256="8b319805f6f7c907b101c864c3ca6cefc9db8ce0791356f180b1b644c7347e4c")
    version("17.1.2", sha256="a72b82ac1910f2cf61a49139f4974f994984475f771b0faa730839607eeedddf")
    version("16.0.2", sha256="0322543fff5ab6f87d11a8a099c4c07dd8a1719040084b6ce9162bcdf5c45c9d")
    version(
        "14.7.0",
        sha256="77994f80360488e7153e64e5959dc5471531d1648e3a4bff14a714d074a38cc2",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@2.6:2.7,3.2:3.8", type=("build", "run"), when="@:14")

    # pyproject.toml
    with when("@26:"):
        depends_on("py-scikit-build-core +pyproject", type="build")
    with when("@:25"):
        depends_on("py-setuptools", type="build")
        # https://github.com/zeromq/pyzmq/issues/1278
        # https://github.com/zeromq/pyzmq/pull/1317
        depends_on("py-setuptools@:59", when="@17:18.0", type="build")

    depends_on("py-packaging", type="build")
    depends_on("py-cython@3:", type="build", when="@26:")
    depends_on("py-cython@0.29.35:", type="build", when="@25.1.1: ^python@3.12:")
    depends_on("py-cython@0.29:", type="build", when="@22.3.0:")
    depends_on("py-cython@0.20:", type="build", when="@18:")
    depends_on("py-cython@0.16:", type="build")
    depends_on("libzmq", type=("build", "link"))
    depends_on("libzmq@3.2:", type=("build", "link"), when="@22.3.0:")
    # Only when python is provided by 'pypy'
    depends_on("py-py", type=("build", "run"), when="@:22")
    depends_on("py-cffi", type=("build", "run"), when="@:22")

    # Undocumented dependencies
    depends_on("py-gevent", type=("build", "run"))

    @run_before("install", when="@15:19")
    def remove_cythonized_files(self):
        # Before v20.0.0 an ancient cythonize API was used, for which we cannot
        # force re-cythonization. Re-cythonizing v14.x fails in general, so
        # restrict to 15:19
        for f in find(".", "*.pyx"):
            touch(f)

    @run_before("install", when="@:25")
    def setup(self):
        """Create config file listing dependency information."""

        with open("setup.cfg", "w") as config:
            config.write(
                """\
[global]
zmq_prefix = {0}

[build_ext]
library_dirs = {1}
include_dirs = {2}
""".format(
                    self.spec["libzmq"].prefix,
                    self.spec["libzmq"].libs.directories[0],
                    self.spec["libzmq"].headers.directories[0],
                )
            )

    @property
    def import_modules(self):
        # importing zmq mutates the install prefix, meaning spack install --test=root py-pyzmq
        # would result in a different install prefix than spack install py-pyzmq. Therefore do not
        # run any import tests.
        return [] if self.spec.satisfies("@:20") else ["zmq"]
