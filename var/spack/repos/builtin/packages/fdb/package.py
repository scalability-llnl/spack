# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fdb(CMakePackage):
    """FDB (Fields DataBase) is a domain-specific object store developed at
    ECMWF for storing, indexing and retrieving GRIB data."""

    homepage = "https://github.com/ecmwf/fdb"
    url = "https://github.com/ecmwf/fdb/archive/refs/tags/5.7.8.tar.gz"
    git = "https://github.com/ecmwf/fdb.git"

    maintainers("skosukhin", "victoria-cherkas", "dominichofer")

    license("Apache-2.0")

    version("master", branch="master")
    version("5.11.23", sha256="09b1d93f2b71d70c7b69472dfbd45a7da0257211f5505b5fcaf55bfc28ca6c65")
    version("5.11.17", sha256="375c6893c7c60f6fdd666d2abaccb2558667bd450100817c0e1072708ad5591e")
    version("5.10.8", sha256="6a0db8f98e13c035098dd6ea2d7559f883664cbf9cba8143749539122ac46099")
    version("5.7.8", sha256="6adac23c0d1de54aafb3c663d077b85d0f804724596623b381ff15ea4a835f60")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("tools", default=True, description="Build the command line tools")
    variant(
        "backends",
        values=any_combination_of(
            # FDB backend in indexed filesystem with table-of-contents with
            # additional support for Lustre filesystem stripping control:
            "lustre",
            # Backends that will be added later:
            # FDB backend in persistent memory (NVRAM):
            # 'pmem',  # (requires https://github.com/ecmwf/pmem)
            # FDB backend in CEPH object store (using Rados):
            # 'rados'  # (requires eckit with RADOS support)
        ),
        description="List of supported backends",
    )

    depends_on("cmake@3.12:", type="build")
    depends_on("ecbuild@3.4:", type="build")
    depends_on("ecbuild@3.7:", type="build", when="@5.11.6:")

    depends_on("eckit@1.16:")
    depends_on("eckit@1.24.4:", when="@5.11.22:")
    depends_on("eckit+admin", when="+tools")

    depends_on("eccodes@2.10:")
    depends_on("eccodes+tools", when="+tools")

    depends_on("metkit@1.5:+grib")

    depends_on("lustre", when="backends=lustre")

    # Starting version 1.7.0, metkit installs GribHandle.h to another directory.
    # That is accounted for only starting version 5.8.0:
    patch("metkit_1.7.0.patch", when="@:5.7.10+tools^metkit@1.7.0:")

    # Download test data before running a test:
    patch(
        "https://github.com/ecmwf/fdb/commit/86e06b60f9a2d76a389a5f49bedd566d4c2ad2b2.patch?full_index=1",
        sha256="8b4bf3a473ec86fd4d7672faa7d74292dde443719299f2ba59a2c8501d6f0906",
        when="@5.7.1:5.7.10+tools",
    )

    @property
    def libs(self):
        return find_libraries("libfdb5", root=self.prefix, shared=True, recursive=True)

    def cmake_args(self):
        enable_build_tools = "+tools" in self.spec

        args = [
            self.define("ENABLE_FDB_BUILD_TOOLS", enable_build_tools),
            self.define("ENABLE_BUILD_TOOLS", enable_build_tools),
            # We cannot disable the FDB backend in indexed filesystem with
            # table-of-contents because some default test programs and tools
            # cannot be built without it:
            self.define("ENABLE_TOCFDB", True),
            self.define("ENABLE_LUSTRE", "backends=lustre" in self.spec),
            self.define("ENABLE_PMEMFDB", False),
            self.define("ENABLE_RADOSFDB", False),
            # The tests download additional data (~10MB):
            self.define("ENABLE_TESTS", self.run_tests),
            # We do not need any experimental features:
            self.define("ENABLE_EXPERIMENTAL", False),
            self.define("ENABLE_SANDBOX", False),
        ]
        return args
