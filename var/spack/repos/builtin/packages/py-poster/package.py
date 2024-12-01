# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoster(PythonPackage):
    """Streaming HTTP uploads and multipart/form-data encoding."""

    homepage = "https://atlee.ca/software/poster"
    url = "https://atlee.ca/software/poster/dist/0.8.1/poster-0.8.1.tar.gz"

    license("MIT")

    version("0.8.1", sha256="af5bf45da4a916db2b638cffd9e9d6668b33020e2b8ca9f864db79b49331c6ff")

    depends_on("py-setuptools", type="build")

    # https://bitbucket.org/chrisatlee/poster/issues/24/not-working-with-python3
    # https://bitbucket.org/chrisatlee/poster/issues/25/poster-connot-work-in-python35
    # Patch created using 2to3
    patch("python3.patch", when="^python@3:")
