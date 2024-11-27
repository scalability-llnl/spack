# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ldc(CMakePackage):
    """The LDC project aims to provide a portable D programming language
    compiler with modern optimization and code generation capabilities.

    LDC is fully Open Source; the parts of the code not taken/adapted from
    other projects are BSD-licensed (see the LICENSE file for details).

    Consult the D wiki for further information: https://wiki.dlang.org/LDC
    """

    homepage = "https://dlang.org/"
    url = "https://github.com/ldc-developers/ldc/releases/download/v1.3.0/ldc-1.3.0-src.tar.gz"

    license("BSD-3-Clause AND BSL-1.0 AND ( Artistic-1.0 OR GPL-2.0-or-later ) AND NCSA AND MIT")

    version("1.3.0", sha256="efe31a639bcb44e1f5b752da21713376d9410a01279fecc8aab8572065a3050b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build runtime and tooling as shared libs")

    depends_on("llvm@3.9:")
    depends_on("zlib-api")
    depends_on("libconfig")
    depends_on("curl")
    depends_on("libedit")
    depends_on("binutils", type=("build", "link", "run"))
    depends_on("ldc-bootstrap", type=("build", "link"))

    provides("D@2")

    def cmake_args(self):
        ldmd2 = self.spec["ldc-bootstrap"].prefix.bin.ldmd2

        args = [
            "-DD_COMPILER:STRING={0}".format(ldmd2),
            "-DBUILD_SHARED_LIBS:BOOL={0}".format(
                "ON" if self.spec.satisfies("+shared") else "OFF"
            ),
            "-DLDC_INSTALL_LTOPLUGIN:BOOL=ON",
            "-DLDC_BUILD_WITH_LTO:BOOL=OFF",
        ]

        return args

    @run_after("install")
    def add_rpath_to_conf(self):
        # Here we modify the configuration file for ldc2 to inject flags
        # that will rpath the standard library location

        config_file = join_path(self.prefix.etc, "ldc2.conf")

        search_for = r"switches = \["
        substitute_with = "switches = [\n" + '        "-L-rpath={0}",'.format(self.prefix.lib)

        filter_file(search_for, substitute_with, config_file)
