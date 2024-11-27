# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxGallery(PythonPackage):
    """A `Sphinx` extension that builds an HTML version of any Python script
    and puts it into an examples gallery.
    """

    homepage = "https://sphinx-gallery.github.io"
    pypi = "sphinx-gallery/sphinx-gallery-0.7.0.tar.gz"

    license("BSD-3-Clause")

    version("0.7.0", sha256="05ead72c947718ab4183c33a598e29743e771dcf75aec84c53048423bd2f4580")
    version("0.4.0", sha256="a286cf2eea47ce838a0754ecef617616afb1f40e41e52fe765723464f52e0c2f")

    depends_on("py-setuptools")
    depends_on("py-matplotlib")
    depends_on("pil")
    depends_on("py-sphinx")
