# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFastjsonschema(PythonPackage):
    """Fast JSON schema validator for Python."""

    homepage = "https://github.com/horejsek/python-fastjsonschema"
    pypi = "fastjsonschema/fastjsonschema-2.15.1.tar.gz"

    license("BSD-3-Clause")

    version("2.16.3", sha256="4a30d6315a68c253cfa8f963b9697246315aa3db89f98b97235e345dedfb0b8e")
    version("2.16.2", sha256="01e366f25d9047816fe3d288cbfc3e10541daf0af2044763f3d0ade42476da18")
    version("2.15.1", sha256="671f36d225b3493629b5e789428660109528f373cf4b8a22bac6fa2f8191c2d2")

    depends_on("py-setuptools", type="build")
