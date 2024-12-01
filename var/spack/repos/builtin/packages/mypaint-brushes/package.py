# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MypaintBrushes(AutotoolsPackage):
    """Brushes used by MyPaint and other software using libmypaint."""

    homepage = "https://github.com/mypaint/mypaint-brushes"
    url = "https://github.com/mypaint/mypaint-brushes/releases/download/v2.0.2/mypaint-brushes-2.0.2.tar.xz"

    maintainers("benkirk")

    license("CC0-1.0")

    version("2.0.2", sha256="7984a74edef94571d872d0629b224abaa956a36f632f5c5516b33d22e49eb566")
    version("1.3.1", sha256="fef66ffc241b7c5cd29e9c518e933c739618cb51c4ed4d745bf648a1afc3fe70")
