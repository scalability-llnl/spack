# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Psrchive(AutotoolsPackage):
    """PSRCHIVE is a library for the analysis of pulsar astronomical data.
    PSRCHIVE is an Open Source C++ development library for the analysis of
    pulsar astronomical data.  It implements an extensive range of algorithms
    for use in pulsar timing, scintillation studies, polarimetric calibration,
    single-pulse work, RFI mitigation, etc. These tools are utilized by a
    powerful suite of user-end programs that come with the library."""

    homepage = "https://psrchive.sourceforge.net/"
    url = "https://sourceforge.net/projects/psrchive/files/psrchive/2022-05-14/psrchive-2022-05-14.tar.gz/download"
    git = "https://git.code.sf.net/p/psrchive/code.git"

    license("AFL-2.1")

    version(
        "2022-05-14", sha256="4d25609837cba1be244fa8adc8f105afe31972f2650bc0b90438862cf35395e1"
    )

    # version specified in
    # https://github.com/lwa-project/pulsar/blob/master/SoftwareStack.md
    # as of Nov 23 2022
    version("2020-10-17", commit="ca12b4a279f3d4adcca223508116d9d270df8cc6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Compile with MPI")
    variant("mkl", default=False, description="Compile with MKL")
    variant("armadillo", default=False, description="Compile with armadillo")
    variant("cfitsio", default=False, description="Compile with cfitsio")
    variant("eigen", default=False, description="Compile with eigen")
    variant("xml", default=False, description="Compile with libxml2")
    variant("x11", default=False, description="Compile with X11")
    variant("qt", default=False, description="Compile with QT")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("psrcat")
    depends_on("epsic")
    depends_on("tempo")
    depends_on("fftw@3:")
    depends_on("python")
    depends_on("pgplot")

    depends_on("mpi", when="+mpi")
    depends_on("mkl", when="+mkl")
    depends_on("armadillo", when="+armadillo")
    depends_on("cfitsio", when="+cfitsio")
    depends_on("eigen", when="+eigen")
    depends_on("libxml2", when="+xml")
    depends_on("libx11", when="+x11")
    depends_on("qt", when="+qt")

    def configure_args(self):
        spec = self.spec
        args = ["--enable-shared"]
        args.append("--with-python_prefix={0}".format(spec["python"].prefix))
        args.append("--with-epsic-dir={}".format(spec["epsic"].prefix))
        args.append("--with-epsic-include-dir={}".format(spec["epsic"].prefix.include))
        args.append("--with-epsic-lib-dir={}".format(spec["epsic"].prefix.lib))
        args.append("--with-psrcat={0}".format(spec["psrcat"].prefix.bin.psrcat))
        args.append("--with-fftw3-dir={0}".format(spec["fftw"].prefix))

        if spec.satisfies("+mpi"):
            args.append("--with-mpi-dir={0}".format(spec["mpi"].prefix))
        else:
            args.append("--without-mpi")
        if spec.satisfies("+mkl"):
            args.append("--with-mkl-dir={0}".format(spec["mkl"].prefix))
        else:
            args.append("--without-mkl")
        if spec.satisfies("+armadillo"):
            args.append("--with-armadillo-dir={0}".format(spec["armadillo"].prefix))
        else:
            args.append("--without-armadillo")
        if spec.satisfies("+cfitsio"):
            args.append("--with-cfitsio-dir={0}".format(spec["cfitsio"].prefix))
        else:
            args.append("--without-cfitsio")
        if spec.satisfies("+eigen"):
            args.append("--with-eigen-dir={0}".format(spec["eigen"].prefix))
        else:
            args.append("--without-eigen")
        if spec.satisfies("+xml"):
            args.append("--with-xml-prefix={0}".format(spec["libxml2"].prefix))
        else:
            args.append("--without-xml")
        if spec.satisfies("+qt"):
            args.append("--with-qt-dir={0}".format(spec["qt"].prefix))
        else:
            args.append("--without-qt")
        return args
