# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtraceevent(MakefilePackage):
    """Library to parse raw trace event formats."""

    homepage = "https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git"
    url = "https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/snapshot/libtraceevent-1.8.2.tar.gz"
    git = "https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git"

    maintainers("Jordan474")

    license("LGPL-2.1-or-later AND GPL-2.0-or-later")

    version("1.8.2", sha256="919f0c024c7b5059eace52d854d4df00ae7e361a4033e1b4d6fe01d97064a1b9")

    variant("doc", default=False, description="Build documentation")

    depends_on("c", type="build")
    depends_on("asciidoc", when="+doc", type="build")
    depends_on("xmlto", when="+doc", type="build")

    def patch(self):
        set_executable("Documentation/install-docs.sh.in")

    @property
    def common_targets(self):
        return [
            "prefix=" + self.prefix,
            "pkgconfig_dir=" + join_path(self.prefix.lib, "pkgconfig"),
        ]

    @property
    def build_targets(self):
        result = self.common_targets + ["all"]
        if self.spec.satisfies("+doc"):
            result.append("doc")
        return result

    @property
    def install_targets(self):
        result = self.common_targets + ["install"]
        if self.spec.satisfies("+doc"):
            result.append("doc-install")
        return result
