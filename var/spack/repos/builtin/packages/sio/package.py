# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sio(CMakePackage):
    """SIO is a persistency solution for reading and writing binary data in SIO
    structures called record and block. SIO has originally been implemented as
    persistency layer for LCIO.
    """

    url = "https://github.com/iLCSoft/SIO/archive/v00-00-02.tar.gz"
    homepage = "https://github.com/iLCSoft/SIO"
    git = "https://github.com/iLCSoft/SIO.git"

    maintainers("vvolkl", "tmadlener", "jmcarcell")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("0.2", sha256="416c93402e7314b7aadedba8e7f9e0d4b0b4f4e34ce26285b04cebb505ecfab2")
    version("0.1", sha256="0407c0daeae53660c0562f9302a220f72ab51547050cd9fe9113b995804ab4b4")
    version("0.0.4", sha256="72e96e6a1cc8dd3641d3e2bb9876e75bf6af8074e1617220da9e52df522ef5c0")
    version("0.0.3", sha256="4c8b9c08480fb53cd10abb0e1260071a8c3f68d06a8acfd373f6560a916155cc")
    version("0.0.2", sha256="e4cd2aeaeaa23c1da2c20c5c08a9b72a31b16b7a8f5aa6d480dcd561ef667657")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "builtin_zlib",
        default=True,
        description="Use and statically link against a builtin version of zlib",
    )
    variant(
        "cxxstd",
        default="17",
        values=("11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("zlib-api", when="~builtin_zlib")

    def cmake_args(self):
        return [
            self.define("CMAKE_CXX_STANDARD", self.spec.variants["cxxstd"].value),
            # Examples are built this way, but if the examples are built they
            # are also used for tests
            self.define("SIO_EXAMPLES", self.run_tests),
            self.define_from_variant("SIO_BUILTIN_ZLIB", "builtin_zlib"),
        ]

    def url_for_version(self, version):
        """Translate version numbers to ilcsoft conventions.
        in spack, the convention is: 0.1 (or 0.1.0) 0.1.1, 0.2, 0.2.1 ...
        in ilcsoft, releases are dashed and padded with a leading zero
        the patch version is omitted when 0
        so for example v01-12-01, v01-12 ...

        :param self: spack package class that has a url
        :type self: class: `spack.PackageBase`
        :param version: version
        :type param: str
        """
        base_url = self.url.rsplit("/", 1)[0]

        if len(version) == 1:
            major = version[0]
            minor, patch = 0, 0
        elif len(version) == 2:
            major, minor = version
            patch = 0
        else:
            major, minor, patch = version

        # By now the data is normalized enough to handle it easily depending
        # on the value of the patch version
        if patch == 0:
            version_str = "v%02d-%02d.tar.gz" % (major, minor)
        else:
            version_str = "v%02d-%02d-%02d.tar.gz" % (major, minor, patch)

        return base_url + "/" + version_str
