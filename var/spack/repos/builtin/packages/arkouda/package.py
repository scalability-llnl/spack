# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.environment import is_system_path


class Arkouda(MakefilePackage):
    """Arkouda is a NumPy-like library for distributed data with a focus on
    large-scale data science applications."""

    homepage = "https://github.com/Bears-R-Us/arkouda"

    url = "https://github.com/Bears-R-Us/arkouda/archive/refs/tags/v2024.06.21.tar.gz"
    git = "https://github.com/Bears-R-Us/arkouda.git"

    test_requires_compiler = True

    # A list of GitHub accounts to notify when the package is updated.
    # TODO: add arkouda devs github account
    maintainers("arezaii")

    # See https://spdx.org/licenses/ for a list.
    license("MIT")

    version("master", branch="master")

    version(
        "2024.06.21", sha256="ab7f753befb3a0b8e27a3d28f3c83332d2c6ae49678877a7456f0fcfe42df51c"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("chapel@2.1 +hdf5 +zmq", type=("build", "link", "run", "test"))
    depends_on("cmake@3.13.4:", type="build")
    depends_on("python@3.9:", type=("build", "link", "run", "test"))
    depends_on("libzmq@4.2.5:", type=("build", "link", "run", "test"))
    depends_on("hdf5+hl~mpi", type=("build", "link", "run", "test"))
    depends_on("libiconv", type=("build", "link", "run", "test"))
    depends_on("libidn2", type=("build", "link", "run", "test"))
    depends_on(
        "arrow +parquet +snappy +zlib +brotli +bz2 +lz4 +zstd",
        type=("build", "link", "run", "test"),
    )

    # Shamelessly copied from the Chapel package.py
    def prepend_cpath_include(self, env, prefix):
        if not is_system_path(prefix):
            env.prepend_path("CPATH", prefix.include)

    # Shamelessly copied from the Chapel package.py
    def update_lib_path(self, env, prefix):
        if not is_system_path(prefix):
            env.prepend_path("LD_LIBRARY_PATH", prefix.lib)
            env.prepend_path("LIBRARY_PATH", prefix.lib)
            if prefix.lib.pkgconfig is not None:
                env.prepend_path("PKG_CONFIG_PATH", prefix.lib.pkgconfig)

    # Arkouda does not have an install target in its Makefile
    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("arkouda_server", prefix.bin)
        # Arkouda can have two executables depending on if Chapel is compiled in
        # single-locale or multi-locale mode
        if not self.spec.satisfies("^chapel comm=none"):
            install("arkouda_server_real", prefix.bin)
        install_tree(self.stage.source_path, prefix)

    def setup_build_environment(self, env):
        env.set("CHPL_FLAGS", "--no-compiler-driver")
        env.set(
            "CHPL_HOME",
            join_path(
                self.spec["chapel"].prefix,
                "share",
                "chapel",
                str(self.spec["chapel"].version.up_to(2)),
            ),
        )
        self.update_lib_path(env, self.spec["hdf5"].prefix)
        self.prepend_cpath_include(env, self.spec["hdf5"].prefix)
        self.update_lib_path(env, self.spec["libzmq"].prefix)
        self.prepend_cpath_include(env, self.spec["libzmq"].prefix)
        self.update_lib_path(env, self.spec["arrow"].prefix)
        self.prepend_cpath_include(env, self.spec["arrow"].prefix)
        self.update_lib_path(env, self.spec["libiconv"].prefix)
        self.prepend_cpath_include(env, self.spec["libiconv"].prefix)
        self.update_lib_path(env, self.spec["libidn2"].prefix)
        self.prepend_cpath_include(env, self.spec["libidn2"].prefix)
