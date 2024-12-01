# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPebble(PythonPackage):
    """Threading and multiprocessing eye-candy."""

    homepage = "https://github.com/noxdafox/pebble"
    pypi = "Pebble/Pebble-5.0.3.tar.gz"

    license("LGPL-3.0-only")

    version("5.0.3", sha256="bdcfd9ea7e0aedb895b204177c19e6d6543d9962f4e3402ebab2175004863da8")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
