# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenslidePython(PythonPackage):
    """OpenSlide Python is a Python interface to the OpenSlide library."""

    homepage = "https://github.com/openslide/openslide-python"
    url = "https://github.com/openslide/openslide-python/archive/v1.1.1.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.1.2", sha256="83e064ab4a29658e7ddf86bf1d3e54d2508cc19ece35d55b55519c826e45d83f")
    version("1.1.1", sha256="33c390fe43e3d7d443fafdd66969392d3e9efd2ecd5d4af73c3dbac374485ed5")

    depends_on("c", type="build")  # generated

    depends_on("openslide@3.4.0:")
    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))
    # https://github.com/openslide/openslide-python/pull/76
    depends_on("py-setuptools@:45", type="build", when="@1.1.1")
    depends_on("py-setuptools", type="build", when="@1.1.2:")
    depends_on("pil", type=("build", "run"))
