# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xforms(AutotoolsPackage):
    """This is the Free Software distribution of the XForms Library, a
    graphical user interface toolkit for X Window Systems."""

    homepage = "https://www.nongnu.org/xforms/"
    url = "http://download.savannah.gnu.org/releases/xforms/xforms-1.0.91.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.2.4", sha256="78cc6b07071bbeaa1f906e0a22d5e9980e48f8913577bc082d661afe5cb75696")
    version("1.2.3", sha256="7989b39598c769820ad451ad91e5cb0de29946940c8240aac94ca8238c2def61")
    version("1.0.91", sha256="88684237c77489bcb1fbc9a794621a2919aa800e1c0a6d83d679b97980e3441d")

    depends_on("c", type="build")  # generated

    depends_on("libx11", type="link")
    depends_on("libxpm", type="link")
    depends_on("jpeg", type="link")
    patch("xformsPatch.patch")

    def configure_args(self):
        args = ["--enable-static"]
        return args
