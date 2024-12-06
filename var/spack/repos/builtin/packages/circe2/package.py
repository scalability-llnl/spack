# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Circe2(AutotoolsPackage):
    """Circe2 is a beam spectrum generator that provides efficient, realistic
    and reproducible parametrizations of the correlated e+/e- and gamma beam
    spectra for linear colliders and photon colliders.
    """

    homepage = "https://whizard.hepforge.org/circe.html"
    url = "https://git.physik.uni-wuerzburg.de/ohl/circe2-public/-/raw/main/circe2-3.1.2.1.tar.gz"

    tags = ["hep"]

    maintainers("tmadlener")

    license("GPL-2.0-or-later")

    version("3.1.2.1", sha256="8bb09e6f566adefcf7b5b1cf9d9fe4536dd3dd11ed3674861de29e177ee0bb04")

    depends_on("fortran", type="build")  # generated

    variant("doc", default=False, description="Create the latex documentation")

    depends_on("ocaml@4.05:")
    depends_on("texlive", when="+doc")

    conflicts(
        "%gcc@:5.0",
        msg="gfortran needs to support Fortran 2008. For more detailed information see https://whizard.hepforge.org/compilers.html",
    )
    conflicts(
        "%gcc@6.5.0",
        msg="Due to severe regressions, gfortran 6.5.0 can not be used. See https://whizard.hepforge.org/compilers.html",
    )

    conflicts(
        "%intel@:17",
        msg="The fortran compiler needs to support Fortran 2008. For more detailed information see https://whizard.hepforge.org/compilers.html",
    )
