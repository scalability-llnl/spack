# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUriTemplate(PythonPackage):
    """RFC 6570 URI Template Processor."""

    homepage = "https://github.com/plinss/uri_template"
    pypi = "uri_template/uri_template-1.2.0.tar.gz"

    license("MIT")

    version("1.2.0", sha256="934e4d09d108b70eb8a24410af8615294d09d279ce0e7cbcdaef1bd21f932b06")

    depends_on("py-setuptools", type="build")
