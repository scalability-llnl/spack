# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.qt_base import QtBase, QtPackage


class Qt5compat(QtPackage):
    """The Qt5compat module contains unsupported Qt 5 APIs for use in Qt 6 projects."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)

    maintainers("wdconinc")

    license("LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only")

    version("6.7.3", sha256="959634d1a6a53f9a483882e81da87ec182ff44d7747a0cc771c786b0f2cf52e0")
    version("6.7.2", sha256="331a1e617952217868beeef7964828500388abeeb502ea3436f16eec816426c4")

    depends_on("cxx", type="build")

    depends_on("qt-base")

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)
