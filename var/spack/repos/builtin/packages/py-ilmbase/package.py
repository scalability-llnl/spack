# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIlmbase(AutotoolsPackage):
    """The PyIlmBase libraries provides python bindings for the IlmBase libraries."""

    homepage = "https://github.com/AcademySoftwareFoundation/openexr/tree/v2.3.0/PyIlmBase"
    url = "https://github.com/AcademySoftwareFoundation/openexr/releases/download/v2.3.0/pyilmbase-2.3.0.tar.gz"

    version("2.3.0", sha256="9c898bb16e7bc916c82bebdf32c343c0f2878fc3eacbafa49937e78f2079a425")

    depends_on("cxx", type="build")  # generated

    depends_on("ilmbase")
    depends_on("boost+python")
    depends_on("py-numpy")

    # https://github.com/AcademySoftwareFoundation/openexr/issues/336
    parallel = False

    def configure_args(self):
        spec = self.spec

        args = [
            "--with-boost-python-libname=boost_python{0}".format(
                spec["python"].version.up_to(2).joined
            )
        ]

        return args
