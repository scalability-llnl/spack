# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWesanderson(PythonPackage):
    """color palettes from Wes Anderson films, based on Karthik Ram's R version."""

    homepage = "https://pypi.org/project/wesanderson"
    pypi = "wesanderson/wesanderson-0.0.3.tar.gz"

    version("0.0.3", sha256="76f5df93b51babcb6e4ca47776846aeefa0234054fee76cbbbae74f9658aabfa")

    depends_on("py-setuptools", type="build")
