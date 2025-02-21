# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Unblur(AutotoolsPackage):
    """Unblur is used to align the frames of movies recorded on an electron
    microscope to reduce image blurring due to beam-induced motion."""

    homepage = "https://grigoriefflab.janelia.org/unblur"
    url = "http://grigoriefflab.janelia.org/sites/default/files/unblur_1.0.2.tar.gz"

    version("1.0.2", sha256="1aa72b1f944114987ede644e1866eaebc08e191ecc566b3461409449360931e2")

    variant("openmp", default=True, description="Enable OpenMP support")
    variant("shared", default=True, description="Dynamic linking")

    depends_on("zlib-api")
    depends_on("jpeg")
    depends_on("libtiff")
    depends_on("gsl")
    depends_on("jbigkit")
    depends_on("fftw@3:")
    # Requires Intel Fortran compiler
    conflicts("%gcc")
    conflicts("%apple-clang")
    conflicts("%clang")
    conflicts("%cce")
    conflicts("%xl")
    conflicts("%xl_r")
    conflicts("%nag")

    configure_directory = "src"

    def patch(self):
        filter_file(r"<<<<<<<.*", "", "src/missing")

    def configure_args(self):
        spec = self.spec
        return [
            "FC=ifort",
            "F77=ifort",
            "--enable-static={0}".format("yes" if "~shared" in spec else "no"),
            "--enable-openmp={0}".format("yes" if "+openmp" in spec else "no"),
            "--enable-optimisations=yes",
        ]

    def build(self, spec, prefix):
        with working_dir("src"):
            make(parallel=False)
