# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonXlib(PythonPackage):
    """The Python X Library is intended to be a fully
    functional X client library for Python programs. It is
    written entirely in Python, in contrast to earlier X
    libraries for Python (the ancient X extension and the newer
    plxlib) which were interfaces to the C Xlib."""

    homepage = "https://github.com/python-xlib/python-xlib"
    pypi = "python-xlib/python-xlib-0.30.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.30", sha256="74131418faf9e7b83178c71d9d80297fbbd678abe99ae9258f5a20cd027acb5f")

    depends_on("python@2.7,3.3:", type=("build", "run"))
    depends_on("py-setuptools@30.3.0:", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-six@1.10.0:", type=("build", "run"))
