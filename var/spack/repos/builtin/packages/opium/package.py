# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opium(AutotoolsPackage):
    """DFT pseudopotential generation project"""

    homepage = "https://opium.sourceforge.net"
    url = "https://downloads.sourceforge.net/project/opium/opium/opium-v3.8/opium-v3.8-src.tgz"

    license("GPL-2.0-or-later")

    version("4.1", sha256="e5a102b52601ad037d8a7b3e2dbd295baad23b8c1e4908b9014df2e432c23c60")
    version("3.8", sha256="edee6606519330aecaee436ee8cfb0a33788b5677861d59e38aba936e87d5ad3")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("external-lapack", default=False, description="Links to externally installed LAPACK")

    depends_on("lapack", when="+external-lapack")

    parallel = False

    def patch(self):
        if "+external-lapack" in self.spec:
            with working_dir("src"):
                filter_file(r"(^subdirs=.*) lapack", r"\1", "Makefile")

    def configure_args(self):
        options = []
        if "+external-lapack" in self.spec:
            options.append("LDFLAGS={0}".format(self.spec["lapack"].libs.ld_flags))

        return options

    def install(self, spec, prefix):
        # opium does not have a make install target :-((
        mkdirp(self.prefix.bin)
        install(join_path(self.stage.source_path, "opium"), self.prefix.bin)
