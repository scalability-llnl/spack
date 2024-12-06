# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Ffb(MakefilePackage):
    """Computational Fluid Dynamics Software for aeroacoustics"""

    homepage = "http://www.ciss.iis.u-tokyo.ac.jp/dl/index.php"
    url = "file://{0}/FrontFlow_blue.8.1.tar.gz".format(os.getcwd())
    manual_download = True

    version("8.1", sha256="1ad008c909152b6c27668bafbad820da3e6ec3309c7e858ddb785f0a3d6e43ae")

    patch("revocap_refiner.patch")
    patch("revocap_refiner-size_t.patch")
    patch("fortran-format.patch")
    patch("xvx.patch")
    patch("gffv3tr.patch")

    depends_on("mpi")
    depends_on("blas")
    depends_on("scalapack")

    parallel = False

    def flag_handler(self, name, flags):
        opt_flag_found = any(f in self.compiler.opt_flags for f in flags)
        if name == "cflags":
            if not opt_flag_found:
                flags.append("-O3")
        elif name == "cxxflags":
            if not opt_flag_found:
                flags.append("-O2")
            flags.append(self.compiler.cxx_pic_flag)
        if name == "fflags":
            if not opt_flag_found:
                flags.append("-O3")
            flags.append("-mcmodel=large")
        if name in ("cflags", "cxxflags", "fflags"):
            return (None, flags, None)
        else:
            return (flags, None, flags)

    def edit(self, spec, prefix):
        workdir = os.getcwd()
        cflags = env["CFLAGS"]
        cxxflags = env["CXXFLAGS"]
        fflags = env["FFLAGS"]

        make = join_path("make", "makefile")
        m = FileFilter(make)
        m.filter(r"#LES3DHOME   =", "LES3DHOME= {0}\n".format(workdir))
        make = join_path("make", "OPTION")
        m = FileFilter(make)
        m.filter(r"CPP\s*=.*$", "CPP = /usr/bin/cpp")
        m.filter(r"CCOM\s*=.*$", "CCOM = {0}".format(spack_cc))
        m.filter(r"COPT\s*=.*$", "COPT = {0}".format(cflags))
        m.filter(r"FCOM\s*=.*$", "FCOM = {0}\n".format(spack_fc))
        m.filter(r"FOPT\s*=.*$", "FOPT = {0}\n".format(fflags))
        m.filter(r"INCDIR\s*=.*$", "INCDIR = {0}\n".format(spec["mpi"].headers.directories[0]))
        m.filter(r"LIBDIR\s*=.*$", "LIBDIR = {0}\n".format(spec["mpi"].libs.directories[0]))

        srcdir = join_path("lib", "src")
        utildir = join_path(workdir, "util")
        with open(join_path("make", "Makeall"), "w") as m:
            m.write("#!/bin/csh -f\n")
            m.write("setenv LES3DHOME {0}\n".format(workdir))
            m.write("cd {0}\n".format(srcdir))
            m.write("./Makeall\n")
            m.write("cd {0}\n".format(utildir))
            m.write("./Makeall\n")

        makeall = join_path("lib", "src", "dd_mpi", "Makeall")
        dd_mpi_dir = join_path("lib", "src", "dd_mpi")
        with open(makeall, "w") as m:
            m.write("#!/bin/csh -f\n")
            m.write("setenv LES3DHOME {0}\n".format(workdir))
            m.write("cd {0}\n".format(dd_mpi_dir))
            m.write("make lib FCOM={0}\n".format(spec["mpi"].mpifc))
        os.chmod(makeall, 0o755)

        makeall = join_path(".", "Makeall.les")
        les3d_dir = join_path("util", "les3d.mpi")
        les3c_dir = join_path("util", "les3c.mpi")
        les3ct_dir = join_path("util", "les3ct.mpi")
        les3x_dir = join_path("util", "les3x.mpi")
        with open(makeall, "w") as m:
            m.write("#!/bin/csh -f\n")
            m.write("setenv LES3DHOME {0}\n".format(workdir))
            m.write("cd {0}\n".format(join_path(workdir, les3d_dir)))
            m.write("make CCOM={0}".format(spec["mpi"].mpicc))
            m.write(" FCOM={0}\n".format(spec["mpi"].mpifc))
            m.write("cd {0}\n".format(join_path(workdir, les3c_dir)))
            m.write("make CCOM={0}".format(spec["mpi"].mpicc))
            m.write(" FCOM={0}\n".format(spec["mpi"].mpifc))
            m.write("cd {0}\n".format(join_path(workdir, les3ct_dir)))
            m.write("make CCOM={0}".format(spec["mpi"].mpicc))
            m.write(" FCOM={0}\n".format(spec["mpi"].mpifc))
            m.write("cd {0}\n".format(join_path(workdir, les3x_dir)))
            m.write("make CCOM={0}".format(spec["mpi"].mpicc))
            m.write(" FCOM={0}\n".format(spec["mpi"].mpifc))

            for d in [les3c_dir, les3ct_dir, les3d_dir]:
                editfile = join_path(d, "FILES")
                m = FileFilter(editfile)
                m.filter(r"-lmpi_f77", "")
        os.chmod(makeall, 0o755)

        editfile = join_path("lib", "src", "Makeall")
        m = FileFilter(editfile)
        m.filter(r"x86_64-linux", "{0}-linux".format(spec.target.family))

        editfile = join_path("lib", "src", "REVOCAP_Refiner-0.4.3", "OPTIONS")
        m = FileFilter(editfile)
        m.filter(r"ARCH\s*=.*$", "ARCH= $(shell arch)-linux")
        m.filter(r"CC\s*=.*$", "CC={0}".format(spack_cc))
        m.filter(r"CFLAGS\s*=.*$", "CFLAGS={0}".format(cflags))
        m.filter(r"CXX\s*=.*$", "CXX={0}".format(spack_cxx))
        m.filter(r"CXXFLAGS\s*=.*$", "CXXFLAGS={0}".format(cxxflags))
        m.filter(r"F90\s*=.*$", "CC={0}".format(spack_fc))
        m.filter(r"LD\s*=.*$", "LD={0}".format(spack_fc))
        m.filter(r"LIBPATH\s*=.*$", "LIBPATH= ")
        m.filter(r"FFLAGS\s*=.*$", "FFLAGS={0}".format(fflags))
        m.filter(r"LDFLAGS\s*=.*$", "LDFLAGS={0}".format(fflags))

        editfile = join_path("lib", "src", "ParMetis-3.1", "Makefile.in")
        m = FileFilter(editfile)
        m.filter(r"CC \s*=.*$", "CC ={0}".format(spack_cc))
        m.filter(r"INCDIR\s*=.*$", "INCDIR = \n")

        editfile = join_path("util", "xvx2gf", "Makefile")
        m = FileFilter(editfile)
        m.filter(r"#LES3DHOME   =", "LES3DHOME= {0}\n".format(workdir))
        m.filter(r"g\+\+", (spack_cxx))

        editfile = join_path("util", "les3x.mpi", "FILES")
        m = FileFilter(editfile)
        m.filter(r"LIBS = -lfort -lgf2 -ldd_mpi -lmpi_f77", "LIBS = -lfort -lgf2  -ldd_mpi")

        editfile = join_path("util", "xvx2gf", "FILES")
        cxx_fortran_flags = []
        if spec.satisfies("%gcc"):
            cxx_fortran_flags.append("-lgfortran")
            m = FileFilter(editfile)
            m.filter("-lifcore -limf", " ".join(cxx_fortran_flags))
        elif spec.satisfies("%fj"):
            cxx_fortran_flags.append("--linkfortran")
            m = FileFilter(editfile)
            m.filter("-lifcore -limf", " ".join(cxx_fortran_flags))
        elif spec.satisfies("%intel"):
            pass

    def build(self, spec, prefix):
        for m in [
            join_path("make", "Makeall"),
            join_path("lib", "src", "dd_mpi", "Makeall"),
            join_path(".", "Makeall.les"),
        ]:
            Executable(m)()

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("macro", prefix.macro)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", prefix.macro)
