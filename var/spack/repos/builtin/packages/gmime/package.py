# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gmime(AutotoolsPackage):
    """GMime is a C/C++ library which may be used for the creation and
    parsing of messages using the Multipurpose Internet Mail Extension (MIME).
    """

    homepage = "https://spruce.sourceforge.net/gmime/"
    url = "https://download.gnome.org/sources/gmime/2.6/gmime-2.6.23.tar.xz"

    license("LGPL-2.1-or-later")

    version("2.6.23", sha256="7149686a71ca42a1390869b6074815106b061aaeaaa8f2ef8c12c191d9a79f6a")

    depends_on("c", type="build")  # generated

    depends_on("glib@2.18.0:")
    depends_on("libgpg-error")
