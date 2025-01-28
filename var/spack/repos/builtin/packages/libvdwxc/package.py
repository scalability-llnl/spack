# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libvdwxc(AutotoolsPackage):
    """Portable C library of density functionals with van der Waals
    interactions for density functional theory"""

    homepage = "https://libvdwxc.gitlab.io/libvdwxc/"
    url = "https://launchpad.net/libvdwxc/stable/0.4.0/+download/libvdwxc-0.4.0.tar.gz"

    license("GPL-3.0-or-later")

    version("0.4.0", sha256="3524feb5bb2be86b4688f71653502146b181e66f3f75b8bdaf23dd1ae4a56b33")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")
    variant("pfft", default=False, description="Enable support for PFFT")

    depends_on("fftw-api@3")
    depends_on("mpi@2:", when="+mpi")
    depends_on("pfft", when="+pfft")

    # pfft needs MPI
    conflicts("~mpi", "+pfft")
    conflicts("^fftw~mpi", "+mpi")

    def configure_args(self):
        spec = self.spec

        args = [
            "--{0}-pfft".format("with" if self.spec.satisfies("+pfft") else "without"),
            "MPICC=",  # make sure both variables are always unset
            "MPIFC=",  # otherwise the configure scripts complains
        ]

        if spec.satisfies("+mpi"):
            # work around b0rken MPI detection: the MPI detection tests are
            # run with CC instead of MPICC, triggering an error. So, setting
            # CC/FC to the MPI compiler wrappers.
            args += [
                "--with-mpi",
                "CC={0}".format(spec["mpi"].mpicc),
                "FC={0}".format(spec["mpi"].mpifc),
            ]
        else:
            args += ["--without-mpi"]

        return args

    # misuse of fftw_plan in m4 for fftw detection (configure fails with gcc 14)
    # Only the configure script is patched, NOT the m4 macro (to avoid depending on aclocal),
    # so running autoreconf is not supported.
    # The relevant upstream fix for the m4 would be:
    # https://gitlab.com/libvdwxc/libvdwxc/-/commit/9340f857515c4a2e56d2aa7cf3a21c41ba8559c3.diff
    patch("fftw-detection.patch", when="@:0.4.0")
