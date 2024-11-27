# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libqrencode(AutotoolsPackage):
    """libqrencode - a fast and compact QR Code encoding library."""

    homepage = "https://fukuchi.org/works/qrencode/"
    url = "https://github.com/fukuchi/libqrencode/archive/v4.1.1.tar.gz"
    git = "https://github.com/fukuchi/libqrencode.git"

    maintainers("cessenat")

    license("LGPL-2.1-or-later")

    version("master", branch="master")
    version("4.1.1", sha256="5385bc1b8c2f20f3b91d258bf8ccc8cf62023935df2d2676b5b67049f31a049c")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    # We assume a reasonably recent libtool is necessary
    depends_on("libtool@2.4.2:", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    # https://fukuchi.org/works/qrencode/ requires libpng-dev
    depends_on("libpng@1.2.0:", type="link")

    def autoreconf(self, spec, prefix):
        # We had to call for autoreconf as well:
        # https://stackoverflow.com/questions/3096989/libtool-version-mismatch-error
        # There appears $LIBTOOLIZE --force --automake --copy is not necessary
        args = ["autoreconf --force --install"]
        with open("autogen.sh", "a") as fh:
            fh.write("\n".join(args))
        # https://fukuchi.org/works/qrencode/
        # If there is no "configure" script in the source code directory,
        # run "autogen.sh" at first to generate it - this is mandatory if
        # you downloaded the source from GitHub
        Executable("./autogen.sh")()
