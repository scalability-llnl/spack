# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Mariadb(CMakePackage):
    """MariaDB Server is one of the most popular database servers
    in the world.

    MariaDB turns data into structured information in a wide array of
    applications, ranging from banking to websites. It is an enhanced, drop-in
    replacement for MySQL. MariaDB is used because it is fast, scalable and
    robust, with a rich ecosystem of storage engines, plugins and many other
    tools make it very versatile for a wide variety of use cases.
    """

    homepage = "https://mariadb.org/about/"
    url = "http://ftp.hosteurope.de/mirror/archive.mariadb.org/mariadb-10.2.8/source/mariadb-10.2.8.tar.gz"

    license("GPL-2.0-or-later")

    version("11.3.2", sha256="5570778f0a2c27af726c751cda1a943f3f8de96d11d107791be5b44a0ce3fb5c")
    version("10.9.6", sha256="fe6f5287fccc6a65b8bbccae09e841e05dc076fcc13017078854ca387eab8ae9")
    version("10.8.8", sha256="8de1a151842976a492d6331b543d0ed87259febbbc03b9ebce07c80d754d6361")
    version("10.8.2", sha256="14e0f7f8817a41bbcb5ebdd2345a9bd44035fde7db45c028b6d4c35887ae956c")
    version("10.4.12", sha256="fef1e1d38aa253dd8a51006bd15aad184912fce31c446bb69434fcde735aa208")
    version("10.4.8", sha256="10cc2c3bdb76733c9c6fd1e3c6c860d8b4282c85926da7d472d2a0e00fffca9b")
    version("10.4.7", sha256="c8e6a6d0bb4f22c416ed675d24682a3ecfa383c5283efee70c8edf131374d817")
    version("10.2.8", sha256="8dd250fe79f085e26f52ac448fbdb7af2a161f735fae3aed210680b9f2492393")
    version("10.1.23", sha256="54d8114e24bfa5e3ebdc7d69e071ad1471912847ea481b227d204f9d644300bf")
    version("5.5.56", sha256="950c3422cb262b16ce133caadbc342219f50f9b45dcc71b8db78fc376a971726")
    version("10.1.14", sha256="18e71974a059a268a3f28281599607344d548714ade823d575576121f76ada13")
    version("5.5.49", sha256="2c82f2af71b88a7940d5ff647498ed78922c92e88004942caa213131e20f4706")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "nonblocking",
        default=True,
        description="Allow non blocking " "operations in the mariadb client library.",
    )

    provides("mariadb-client")
    provides("mysql-client")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("cmake@2.6:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("bison", type="build")
    depends_on("jemalloc")
    depends_on("libaio", when="platform=linux")
    depends_on("libedit")
    depends_on("libevent", when="+nonblocking")
    depends_on("ncurses")
    depends_on("zlib-api")
    depends_on("curl")
    depends_on("libxml2")
    depends_on("lz4")
    depends_on("libzmq")
    depends_on("msgpack-c")
    depends_on("openssl")
    depends_on("openssl@:1.0", when="@:10.1")
    depends_on("krb5")

    conflicts("%gcc@9.1.0:", when="@:5.5")
    conflicts("%gcc@13:", when="@:10.8.7")  # https://github.com/spack/spack/issues/41377

    # patch needed for cmake-3.20
    patch(
        "https://github.com/mariadb-corporation/mariadb-connector-c/commit/242cab8c.patch?full_index=1",
        sha256="760fd19cd8d4d756a0799ed9110cfd2898237e43835fefe3668079c5b87fc36d",
        working_dir="libmariadb",
        when="@10.2.8:10.4.12",
    )

    def cmake_args(self):
        args = []

        args.append("-DENABLE_DTRACE:BOOL=OFF")

        return args
