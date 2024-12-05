# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTestfixtures(PythonPackage):
    """Testfixtures is a collection of helpers and mock objects that are useful
    when writing automated tests in Python."""

    homepage = "https://github.com/Simplistix/testfixtures"
    url = "https://github.com/Simplistix/testfixtures/archive/6.16.0.zip"

    license("MIT")

    version("6.16.0", sha256="6b5bbca4f7d5692ca4566c60c0383b121d9f1cfecbc3de8442c499a63c264eb8")

    depends_on("py-setuptools", type="build")
