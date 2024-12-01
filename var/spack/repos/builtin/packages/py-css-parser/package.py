# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCssParser(PythonPackage):
    """A CSS Cascading Style Sheets library for Python."""

    homepage = "https://github.com/ebook-utils/css-parser"
    pypi = "css-parser/css-parser-1.0.9.tar.gz"

    maintainers("LydDeb")

    license("LGPL-3.0-or-later")

    version("1.0.9", sha256="196db822cef22745af6a58d180cf8206949ced58b48f5f3ee98f1de1627495bb")

    depends_on("py-setuptools", type="build")
