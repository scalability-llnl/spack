# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class Ffte(Package):
    """Fastest Fourier Transform in the East. Provides FFT for powers of 2, 3,
    and 5 lengths in one, two, and three dimensions. Support for vector
    hardware, MPI, and CUDA Fortran is also included."""

    homepage = "http://www.ffte.jp/"
    url = "http://www.ffte.jp/ffte-7.0.tgz"

    maintainers("luszczek")

    version("7.0", sha256="078d5f84a5f2479ca5c4a3bd777ad761fe98addf1642a045bac6602a0cae3da0")
    version("6.0", sha256="fc82595a8f8323b2796cc5eeb1cc9f7e50ca9e511a14365cc3984da6b7a9b8b4")
    version("5.0", sha256="1f46ca16badc3aca0ad13ca91a6a67829a57b403501cdc821b80cfa62b2a89c2")
    version("4.0", sha256="61680f73c48659ac45aec60ef5a725547f763bb9017edbd3f44a6a9ad0fda62f")
    version("3.0", sha256="dbaab8204a16072c8d572efa3733e9946a9be0d1a051fc19e2d9253be23247ff")
    version("2.0", sha256="f5cf1d1f880288e359f4d517191980ffca4420f817ecaa2d754ca5c5421271e3")
    version("1.0", sha256="35171e3324019018c25575b2807a6513fa85badad040f30f238fff03d4b4d1ab")

    depends_on("fortran", type="build")  # generated

    variant("mpi", default=False, description="Build MPI library")
    variant("cuda", default=False, description="Use CUDA Fortran")
    variant("vector", default=False, description="Use vectorized FFT")

    depends_on("mpi", when="+mpi")

    requires("%nvhpc", when="+cuda", msg="ffte+cuda must use NVHPC compiler")

    def edit(self, spec, prefix):
        "No make-file, must create one from scratch."

        open("mpi/param.h", "w").write(open("param.h").read())

        for fpfx in (".", "mpi"):
            vrs = "%sfftever" % ["", "", "", "p"][len(fpfx)]
            s6 = 6 * " "
            fd = open("%s/%s.f" % (fpfx, vrs), "w")
            fd.write("%ssubroutine %s(i,j,k)\n" % (s6, vrs))
            fd.write("%sinteger i,j,k\n" % s6)
            fd.write("%si=%s\n" % (s6, spec.version[0]))
            fd.write("%sj=%s\n" % (s6, spec.version[1]))
            fd.write("%sk=0\n%sreturn\n%send\n" % (3 * (s6,)))
            fd.close()

            ff, cuf, vf = [], [], []
            for f in glob.glob("%s/*.f" % fpfx):
                nf = f.replace(".f", ".o").replace("%s/" % fpfx, "")
                if "/cu" in f or "/pcu" in f:
                    cuf.append(nf)
                elif "/v" in f or "/pv" in f:
                    vf.append(nf)
                else:
                    ff.append(nf)

            if "." == fpfx:
                lbnm = "libffte.a"
            else:
                lbnm = "libfftempi.a"

            for spc, vrf, rs, ip in (("+vector", vf, "v", 2), ("+cuda", cuf, "cu", 3)):
                if spc in spec:
                    for f in vrf:  # replace with variant versions
                        orgf = f[:ip].replace(rs, "") + f[ip:]
                        if orgf in ff:  # already reference implementation?
                            del ff[ff.index(orgf)]
                    ff.extend(vrf)

            aff = " ".join(ff)
            fd = open("%s/Makefile" % fpfx, "w")
            fd.write("all: %s\n" % lbnm)
            if "+mpi" in spec and "." == fpfx:
                fd.write("\tcd mpi ; $(MAKE)\n")
            fd.write("\n%s: %s\n" % (lbnm, aff))
            fd.write("\tar rc %s %s\n" % (lbnm, aff))
            fd.write("\tranlib %s\n" % lbnm)
            fd.close()

    def install(self, spec, prefix):
        self.edit(spec, prefix)
        if spec.satisfies("+mpi"):
            env["CC"] = spec["mpi"].mpicc
            env["F77"] = spec["mpi"].mpif77
            env["FC"] = spec["mpi"].mpifc

        # allow real/complex aliasing in GNU Fortran 10 and up
        if spec.satisfies("%gcc@10:"):
            env["FFLAGS"] = "-fallow-argument-mismatch"

        # enable CUDA Fortran in NVHPC
        if spec.satisfies("%nvhpc"):
            env["FFLAGS"] = "-Mcuda"

        make()
        mkdirp(prefix.lib)
        install("libffte.a", prefix.lib)
        if spec.satisfies("+mpi"):
            install("mpi/libfftempi.a", prefix.lib)
