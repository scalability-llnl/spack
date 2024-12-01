# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySystemdPython(PythonPackage):
    """Python interface for libsystemd"""

    homepage = "https://github.com/systemd/python-systemd"
    pypi = "systemd-python/systemd-python-234.tar.gz"

    license("LGPL-2.1-or-later")

    version("235", sha256="4e57f39797fd5d9e2d22b8806a252d7c0106c936039d1e71c8c6b8008e695c0a")
    version("234", sha256="fd0e44bf70eadae45aadc292cb0a7eb5b0b6372cd1b391228047d33895db83e7")

    depends_on("c", type="build")  # generated

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("pkgconfig", type="build")
    # depends on system installed systemd and systemd-devel packages
