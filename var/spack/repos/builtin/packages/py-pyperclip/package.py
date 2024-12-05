# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyperclip(PythonPackage):
    """A cross-platform clipboard module for Python."""

    homepage = "https://github.com/asweigart/pyperclip"
    pypi = "pyperclip/pyperclip-1.7.0.tar.gz"

    license("BSD-3-Clause")

    version("1.8.2", sha256="105254a8b04934f0bc84e9c24eb360a591aaf6535c9def5f29d92af107a9bf57")
    version("1.7.0", sha256="979325468ccf682104d5dcaf753f869868100631301d3e72f47babdea5700d1c")

    depends_on("py-setuptools", type="build")
    depends_on("xclip", type="run", when="platform=linux")
