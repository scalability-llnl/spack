# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gts(AutotoolsPackage):
    """GTS stands for the GNU Triangulated Surface Library.

    It is an Open Source Free Software Library intended to provide a set of
    useful functions to deal with 3D surfaces meshed with interconnected
    triangles. The source code is available free of charge under the Free
    Software LGPL license.

    The code is written entirely in C with an object-oriented approach
    based mostly on the design of GTK+. Careful attention is paid to
    performance related issues as the initial goal of GTS is to provide a
    simple and efficient library to scientists dealing with 3D computational
    surface meshes.
    """

    homepage = "https://gts.sourceforge.net/index.html"
    url = "https://gts.sourceforge.net/tarballs/gts-snapshot-121130.tar.gz"

    license("LGPL-2.0-only")

    version("121130", sha256="c23f72ab74bbf65599f8c0b599d6336fabe1ec2a09c19b70544eeefdc069b73b")

    depends_on("c", type="build")  # generated

    depends_on("glib")
    depends_on("pkgconfig", type=("build"))
