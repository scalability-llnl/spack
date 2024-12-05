# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmGdb(AutotoolsPackage):
    """This is ROCmgdb, the ROCm source-level debugger for Linux,
    based on GDB, the GNU source-level debugger."""

    homepage = "https://github.com/ROCm/ROCgdb"
    url = "https://github.com/ROCm/ROCgdb/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    license("LGPL-2.0-or-later")

    maintainers("srekolam", "renjithravindrankannath")
    version("6.2.1", sha256="bed312c3fbb9982166538036bb9fd4a75053117c65ba80e34dbdae629a8fe6e4")
    version("6.2.0", sha256="753fd4f34d49fb0297b01dca2dd7cdf12cd039caa622a5f2d153362d27a8659c")
    version("6.1.2", sha256="19208de18d503e1da79dc0c9085221072a68e299f110dc836204364fa1b532cc")
    version("6.1.1", sha256="3d982abc130a286d227948aca5783f2e4507ef4275be21dad0914e37217ba19e")
    version("6.1.0", sha256="e90d855ca4c1478acf143d45ff0811e7ecd068711db155de6d5f3593cdef6230")
    version("6.0.2", sha256="69b7c3d63435e7d99088980498c68422e52b69244d10a3a62541633e733286e0")
    version("6.0.0", sha256="0db4ab32ca729e69688cdb238df274ce5cf58b5cb2538584662cca4358708c2b")
    version("5.7.1", sha256="5cd150b5796aea9d77efd43b89d30a34fa4125338179eb87c6053abcac9f3c62")
    version("5.7.0", sha256="94fba57b2f17b593de61f7593b404fabc00b054d38567be57d12cf7654b7969a")
    version("5.6.1", sha256="d2b40d4c5aa41a6ce2a84307627b30d16a458672e03e13f9d27c12f2dc3f21d6")
    version("5.6.0", sha256="997ef1883aac2769552bc7082c70b837f4e98b57d24c133cea52b9c92fb0dee1")
    version("5.5.1", sha256="359258548bc7e6abff16bb13c301339fb96560b2b961433c9e0712e4aaf2d9e1")
    version("5.5.0", sha256="d3b100e332facd9635e328f5efd9f0565250edbe05be986baa2e0470a19bcd79")
    with default_args(deprecated=True):
        version("5.4.3", sha256="28c1ce39fb1fabe61f86f6e3c6940c10f9a8b8de77f7bb4fdd73b04e172f85f6")
        version("5.4.0", sha256="7ee984d99818da04733030b140c1f0929639bc719a5e418d53cc2c2a8cbc9a79")
        version("5.3.3", sha256="9fc3ccd9378ad40f2f0c9577bc400cc9a202d0ae4656378813b67653b9023c46")
        version("5.3.0", sha256="402537baf0779cae586d608505e81173ba85f976fe993f1633e3afe81669350f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@3:", type="build")
    depends_on("texinfo", type="build")
    depends_on("bison", type="build")
    depends_on("flex@2.6.4:", type="build")
    depends_on("libunwind", type="build")
    depends_on("expat", type=("build", "link"))
    depends_on("python", type=("build", "link"))
    depends_on("zlib-api", type="link")
    depends_on("babeltrace@1.2.4", type="link")
    depends_on("gmp", type=("build", "link"))
    depends_on("mpfr", type=("build", "link"))

    for ver in [
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
    ]:
        depends_on(f"rocm-dbgapi@{ver}", type="link", when=f"@{ver}")
        depends_on(f"comgr@{ver}", type="link", when=f"@{ver}")

    for ver in [
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
    ]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    build_directory = "spack-build"

    def configure_args(self):
        # Generic options to compile GCC
        options = [
            # Distributor options
            "--program-prefix=roc",
            "--enable-64-bit-bfd",
            "--with-bugurl=https://github.com/ROCm/ROCgdb/issues",
            "--with-pkgversion=-ROCm",
            "--enable-targets=x86_64-linux-gnu,amdgcn-amd-amdhsa",
            "--disable-ld",
            "--disable-gas",
            "--disable-gdbserver",
            "--disable-sim",
            "--enable-tui",
            "--disable-gdbtk",
            "--disable-shared",
            "--with-expat",
            "--with-system-zlib" "--without-guile",
            "--with-babeltrace",
            "--with-lzma",
            "--with-python",
            "--with-rocm-dbgapi={0}".format(self.spec["rocm-dbgapi"].prefix),
        ]
        if self.spec.satisfies("@5.2.0:"):
            options.append("--disable-gprofng")
        return options
