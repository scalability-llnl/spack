# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xbraid(MakefilePackage):
    """XBraid: Parallel time integration with Multigrid"""

    homepage = "https://computing.llnl.gov/projects/parallel-time-integration-multigrid/software"
    url = "https://github.com/XBraid/xbraid/archive/v2.2.0.tar.gz"
    tags = ["radiuss"]

    version("3.1.0", sha256="3419b22918c65555e8c552b70a0837a251a74c471dac8e4a7b2272bf7d955c88")
    version("3.0.0", sha256="06988c0599cd100d3b3f3ebb183c9ad34a4021922e0896815cbedc659aaadce6")
    version("2.3.0", sha256="706f0acde201c7c336ade3604679759752a74e2cd6c2a29a8bf5676b6e54b704")
    version("2.2.0", sha256="082623b2ddcd2150b3ace65b96c1e00be637876ec6c94dc8fefda88743b35ba3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    @when("@:2.2.0")
    def build(self, spec, prefix):
        make("libbraid.a")

    @when("@2.3.0:")
    def build(self, spec, prefix):
        make("braid")

    # XBraid doesn't have a real install target, so it has to be done
    # manually
    @when("@2.3.0:")
    def install(self, spec, prefix):
        # Install headers
        mkdirp(prefix.include)
        install("braid/*.h", prefix.include)
        install("braid/*.hpp", prefix.include)

        # Install library
        mkdirp(prefix.lib)
        install("braid/libbraid.a", join_path(prefix.lib, "libbraid.a"))

        # Install other material (e.g., examples, tests, docs)
        mkdirp(prefix.share)
        install("makefile.inc", prefix.share)
        install_tree("examples", prefix.share.examples)
        install_tree("drivers", prefix.share.drivers)

        # TODO: Some of the scripts in 'test' are useful, even for
        # users; some could be deleted from an installation because
        # they're not useful to users
        install_tree("test", prefix.share.test)
        install_tree("misc", prefix.share.misc)
        install_tree("docs", prefix.share.docs)

    @when("@:2.2.0")
    def install(self, spec, prefix):
        # Install headers
        mkdirp(prefix.include)
        install("*.h", prefix.include)

        # Install library
        mkdirp(prefix.lib)
        library = "libbraid.a"
        install(library, join_path(prefix.lib, library))

        # Install other material (e.g., examples, tests, docs)
        mkdirp(prefix.share)
        install("makefile.inc", prefix.share)
        install_tree("examples", prefix.share.examples)
        install_tree("drivers", prefix.share.drivers)

        # TODO: Some of the scripts in 'test' are useful, even for
        # users; some could be deleted from an installation because
        # they're not useful to users
        install_tree("test", prefix.share.test)
        install_tree("user_utils", prefix.share.user_utils)
        install_tree("docs", prefix.share.docs)

    @property
    def libs(self):
        return find_libraries("libbraid", root=self.prefix, shared=False, recursive=True)
