# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Arkouda(MakefilePackage):
    """Arkouda is a NumPy-like library for distributed data with a focus on
    large-scale data science applications."""

    homepage = "https://github.com/Bears-R-Us/arkouda"

    # Arkouda does not have a current PyPI package, so we use the GitHub tarball
    url = "https://github.com/Bears-R-Us/arkouda/archive/refs/tags/v2024.10.02.tar.gz"
    git = "https://github.com/Bears-R-Us/arkouda.git"

    test_requires_compiler = True

    # A list of GitHub accounts to notify when the package is updated.
    # TODO: add arkouda devs github account
    maintainers("arezaii")

    # See https://spdx.org/licenses/ for a list.
    license("MIT")

    version("master", branch="master")

    version(
        "2024.10.02", sha256="00671a89a08be57ff90a94052f69bfc6fe793f7b50cf9195dd7ee794d6d13f23"
    )
    version(
        "2024.06.21", sha256="ab7f753befb3a0b8e27a3d28f3c83332d2c6ae49678877a7456f0fcfe42df51c"
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    variant(
        "distributed",
        default=False,
        description="Build Arkouda for distributed execution on a cluster or supercomputer",
    )

    depends_on("chapel@2.1: +hdf5 +zmq", type=("build", "link", "run", "test"))
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

    requires("^chapel comm=none", when="~distributed")
    requires("^chapel +python-bindings", when="@2024.10.02:")
    requires(
        "^chapel comm=gasnet",
        "^chapel comm=ugni",
        "^chapel comm=ofi",
        policy="one_of",
        when="+distributed",
    )

    # Some systems need explicit -fPIC flag when building the Arrow functions
    patch("makefile-fpic-2024.06.21.patch", when="@2024.06.21")
    patch("makefile-fpic-2024.10.02.patch", when="@2024.10.02:")

    sanity_check_is_file = [join_path("bin", "arkouda_server")]

    def check(self):
        # skip b/c we need the python client
        pass

    # override the default edit method to apply the patch
    def edit(self, spec, prefix):
        self.update_makefile_paths(spec, prefix)

    def update_makefile_paths(self, spec, prefix):
        # add to the Makefile.paths file for all of the dependencies installed by spack
        # in the form $(eval $(call add-path,<path-to-dep-aka-prefix>))
        with open("Makefile.paths", "w") as f:
            f.write("$(eval $(call add-path,{0}))\n".format(spec["hdf5"].prefix))
            f.write("$(eval $(call add-path,{0}))\n".format(spec["libzmq"].prefix))
            f.write("$(eval $(call add-path,{0}))\n".format(spec["arrow"].prefix))
            f.write("$(eval $(call add-path,{0}))\n".format(spec["libiconv"].prefix))
            f.write("$(eval $(call add-path,{0}))\n".format(spec["libidn2"].prefix))

    # Arkouda does not have an install target in its Makefile
    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("arkouda_server", prefix.bin)
        # Arkouda can have two executables depending on if Chapel is compiled in
        # single-locale or multi-locale mode
        if not self.spec.satisfies("^chapel comm=none"):
            install("arkouda_server_real", prefix.bin)
        # install_tree(self.stage.source_path, prefix)
