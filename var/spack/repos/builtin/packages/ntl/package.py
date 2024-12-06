# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ntl(MakefilePackage):
    """NTL  -- a library for doing number theory

    NTL is open-source software distributed under the terms of the GNU Lesser
    General Public License (LGPL) version 2.1 or later.  See the file
    doc/copying.txt for complete details on the licensing of NTL.

    Documentation is available in the file doc/tour.html, which can be viewed
    with a web browser.
    """

    homepage = "https://libntl.org"
    url = "https://github.com/libntl/ntl/archive/refs/tags/v11.5.1.tar.gz"

    maintainers("wohlbier")

    version("11.5.1", sha256="ef578fa8b6c0c64edd1183c4c303b534468b58dd3eb8df8c9a5633f984888de5")
    version("11.5.0", sha256="9e1e6488b177c3e5d772fdd6279c890937a9d1c3b694a904ac1cfbe9cab836db")
    version("11.4.4", sha256="2ce7a10fadbed6c3859d72c859612a4ca0dbdf6a9db99db4261422b7f0804bfa")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=False, description="Build shared library.")

    depends_on("gmp")

    # The configure script is a thin wrapper around perl
    depends_on("perl", type="build")

    build_directory = "src"

    def edit(self, spec, prefix):
        config_args = [
            "CXX={0}".format(self.compiler.cxx),
            "DEF_PREFIX={0}".format(prefix),
            "GMP_PREFIX={0}".format(spec["gmp"].prefix),  # gmp dependency
        ]
        if "+shared" in spec:
            config_args.append("SHARED=on")

        with working_dir(self.build_directory):
            configure = Executable("./configure")
            configure(*config_args)
