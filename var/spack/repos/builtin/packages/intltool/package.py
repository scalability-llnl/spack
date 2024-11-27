# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Intltool(AutotoolsPackage):
    """intltool is a set of tools to centralize translation of many different
    file formats using GNU gettext-compatible PO files."""

    homepage = "https://freedesktop.org/wiki/Software/intltool/"
    url = "https://launchpad.net/intltool/trunk/0.51.0/+download/intltool-0.51.0.tar.gz"
    list_url = "https://launchpad.net/intltool/+download"

    license("GPL-2.0-or-later")

    version("0.51.0", sha256="67c74d94196b153b774ab9f89b2fa6c6ba79352407037c8c14d5aeb334e959cd")

    # requires XML::Parser perl module
    depends_on("perl-xml-parser", type=("build", "run"))
    depends_on("perl@5.8.1:", type=("build", "run"))

    # patch for "Unescaped left brace in regex is illegal here in regex"
    # warnings witn perl 5.22 and errors with perl 5.26 and newer
    patch(
        "https://launchpadlibrarian.net/216052398/intltool-perl-5.22.patch",
        sha256="ca9d6562f29f06c64150f50369a24402b7aa01a3a0dc73dce55106f3224330a1",
        level=0,
    )

    def check(self):
        # `make check` passes but causes `make install` to fail
        pass

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name))

    def setup_dependent_package(self, module, dependent_spec):
        # intltool is very likely to be a build dependency,
        # so we add the tools it provides to the dependent module
        executables = [
            "intltool-extract",
            "intltoolize",
            "intltool-merge",
            "intltool-prepare",
            "intltool-update",
        ]

        for name in executables:
            setattr(module, name, self._make_executable(name))
