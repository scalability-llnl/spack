# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAniso8601(PythonPackage):
    """A library for parsing ISO 8601 strings."""

    homepage = "https://bitbucket.org/nielsenb/aniso8601"
    pypi = "aniso8601/aniso8601-9.0.1.tar.gz"

    license("BSD-3-Clause")

    version("9.0.1", sha256="72e3117667eedf66951bb2d93f4296a56b94b078a8a95905a052611fb3f1b973")
    version("7.0.0", sha256="513d2b6637b7853806ae79ffaca6f3e8754bdd547048f5ccc1420aec4b714f1e")

    depends_on("py-setuptools", type="build")
