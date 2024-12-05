# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArgs(PythonPackage):
    """Command Arguments for Humans."""

    homepage = "https://github.com/kennethreitz/args"
    pypi = "args/args-0.1.0.tar.gz"

    version("0.1.0", sha256="a785b8d837625e9b61c39108532d95b85274acd679693b71ebb5156848fcf814")

    depends_on("py-setuptools", type="build")
