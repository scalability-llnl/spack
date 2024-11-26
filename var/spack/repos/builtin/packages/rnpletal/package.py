# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Rnpletal(AutotoolsPackage):
    """The acronym RNPL stands for Rapid Numerical Prototyping Language. It is
    a language for expressing time-dependent systems of partial differential
    equations and the information necessary for solving them using
    finite-difference techniques. It has advantages over traditional
    programming languages such as C and FORTRAN because it only requires the
    user to enter the essential structure of the program while it fills in the
    details."""

    homepage = "http://laplace.physics.ubc.ca/People/matt/Rnpl/index.html"
    url = "ftp://laplace.physics.ubc.ca/pub/rnpletal/rnpletal.tar.gz"

    # RNPL is distributed via tarballs that are updated from time to time, but
    # which carry no version number.
    version("develop", sha256="2886f96393b64703fccf61b3dbc34e0fa45a79297232be76352f29cb83863d4d")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    maintainers("eschnett")

    variant(
        "packages",
        multi=True,
        description="Packages to enable",
        values=(
            # "rvs",
            # "cliser",
            "rnpl",
            # "svs",
            # "vutil",
            # "utilmath",
            # "visutil",
            # "utilio",
            # "cvtestsdf",
            # "netlib_linpack",
            # "netlib_odepack",
            # "netlib_fftpack",
            # "netlib_lapack3.0",
        ),
        default="rnpl",
    )

    patch("corrections.diff")

    depends_on("bison", type="build")
    depends_on("flex", type="build")

    parallel = False

    # This is only one of the configure scripts. (We will use other scripts as
    # well, depending on which packages will be installed.) We define this so
    # that Spack does not try to create a configure script.
    @property
    def configure_abs_path(self):
        return os.path.join(os.path.abspath(self.configure_directory), "rnpl", "configure")

    def configure(self, spec, prefix):
        options = ["--prefix={0}".format(prefix)]
        for package in self.spec.variants["packages"].value:
            with working_dir(package):
                configure(*options)

    def build(self, spec, prefix):
        for package in self.spec.variants["packages"].value:
            with working_dir(package):
                make()

    def install(self, spec, prefix):
        for package in self.spec.variants["packages"].value:
            with working_dir(package):
                make("install")

    @property
    def libs(self):
        return find_libraries(
            ["libbbhutil", "librnpl"], root=self.prefix, shared=False, recursive=True
        )
