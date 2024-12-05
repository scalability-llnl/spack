# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBoltons(PythonPackage):
    """When they're not builtins, they're boltons.

    Functionality that should be in the standard library. Like builtins,
    but Boltons.

    Otherwise known as, "everyone's util.py," but cleaned up and tested.
    """

    homepage = "https://boltons.readthedocs.io/"
    pypi = "boltons/boltons-16.5.1.tar.gz"

    version("23.0.0", sha256="8c50a71829525835ca3c849c7ed2511610c972b4dddfcd41a4a5447222beb4b0")
    version("16.5.1", sha256="fcded58596fa79bd1ada4488178e79fd11c7cb449f29ff9a6532411fb2db19b7")

    depends_on("py-setuptools", type="build")
