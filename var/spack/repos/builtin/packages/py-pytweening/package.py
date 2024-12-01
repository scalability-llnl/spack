# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytweening(PythonPackage):
    """A collection of tweening / easing functions implemented
    in Python."""

    homepage = "https://github.com/asweigart/pytweening"
    pypi = "PyTweening/PyTweening-1.0.3.zip"

    license("MIT")

    version("1.0.3", sha256="4b608a570f4dccf2201e898f643c2a12372eb1d71a3dbc7e778771b603ca248b")

    depends_on("py-setuptools", type="build")
