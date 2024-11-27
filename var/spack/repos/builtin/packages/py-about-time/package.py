# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAboutTime(PythonPackage):
    """A cool helper for tracking time and throughput of
    code blocks, with beautiful human friendly renditions."""

    homepage = "https://github.com/rsalmei/about-time"
    pypi = "about-time/about-time-4.1.0.tar.gz"

    license("MIT")

    version("4.2.1", sha256="6a538862d33ce67d997429d14998310e1dbfda6cb7d9bbfbf799c4709847fece")
    version("4.1.0", sha256="963b1f3739b0c9732eb205031762b76f1291d89b5d0c8220a8d5b154e32ce650")
    version("3.1.1", sha256="586b329450c9387d1ae8c42d2db4f5b4c57a54508d0f1b7bb00322ffd5ce9f9b")

    depends_on("python@3.7:3", type=("build", "run"), when="@4:")
    depends_on("py-setuptools", type="build")
