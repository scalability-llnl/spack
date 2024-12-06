# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPmw(PythonPackage):
    """Pmw is a toolkit for building high-level compound widgets, or
    megawidgets, constructed using other widgets as component parts."""

    pypi = "Pmw/Pmw-2.0.0.tar.gz"

    version("2.0.1", sha256="0b9d28f52755a7a081b44591c3dd912054f896e56c9a627db4dd228306ad1120")
    version("2.0.0", sha256="2babb2855feaabeea1003c6908b61c9d39cff606d418685f0559952714c680bb")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
