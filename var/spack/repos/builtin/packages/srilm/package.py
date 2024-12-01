# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Srilm(MakefilePackage):
    """SRILM (SRI Language Modeling Toolkit) is a toolkit for building
    and applying statistical language models (LMs), primarily for
    use in speech recognition, statistical tagging and segmentation,
    and machine translation."""

    homepage = "http://www.speech.sri.com/projects/srilm/"
    url = "file://{0}/srilm-1.7.3.tar.gz".format(os.getcwd())
    manual_download = True

    maintainers("RemiLacroix-IDRIS")

    version("1.7.3", sha256="01eaf12d0f35b96d2b28ad0d41c9f915dd22b534a7abde3fbb9e35fb6c19200e")

    variant("openmp", default=False, description="Enable OpenMP")
    variant("pic", default=False, description="Build position independent code")
    variant("liblbfgs", default=False, description="Enable libLBFGS")

    depends_on("iconv")
    depends_on("liblbfgs", when="+liblbfgs")
    depends_on("gawk", type=("build", "run"))
    depends_on("perl", type=("build", "run"))
    depends_on("binutils", type="build")  # for c++filt

    @property
    def machine_type(self):
        return Executable("sbin/machine-type")(output=str, error=str).strip()

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter(r"# SRILM\s*=.*", "SRILM = {0}".format(self.build_directory))

        makefile_common = FileFilter("common/Makefile.common.variables")
        makefile_common.filter(r"GAWK\s*=.*", "GAWK = {0}".format(which("gawk")))
        makefile_common.filter(r"PERL\s*=.*", "PERL = {0}".format(which("perl")))
        makefile_common.filter(
            r"PIC_FLAG\s*=.*", "PIC_FLAG = {0}".format(self.compiler.cc_pic_flag)
        )

        makefile_machine_fn = "common/Makefile.machine.{0}".format(self.machine_type)

        makefile_machine = FileFilter(makefile_machine_fn)
        makefile_machine.filter(r"CC\s*=.*", "CC = {0}".format(spack_cc))
        makefile_machine.filter(
            r"CXX\s*=.*", "CXX = {0} -DINSTANTIATE_TEMPLATES".format(spack_cxx)
        )

        omp_flag = self.compiler.openmp_flag if "+openmp" in spec else ""
        makefile_machine.filter(
            r"ADDITIONAL_CFLAGS\s*=.*", "ADDITIONAL_CFLAGS = {0}".format(omp_flag)
        )
        makefile_machine.filter(
            r"ADDITIONAL_CXXFLAGS\s*=.*", "ADDITIONAL_CXXFLAGS = {0}".format(omp_flag)
        )
        makefile_machine.filter(r"(SYS_LIBRARIES\s*=.*)", r"\1 -liconv")

        # Make sure the machine specific Makefile doesn't override those
        makefile_machine.filter(r"GAWK\s*=.*", "")
        makefile_machine.filter(r"PERL\s*=.*", "")
        makefile_machine.filter(r"PIC_FLAG\s*=.*", "")

        with open(makefile_machine_fn, "a") as makefile_machine:
            # Tcl is only needed for tests so disable it
            makefile_machine.write("\nNO_TCL = 1\n")
            if "+pic" in spec:
                makefile_machine.write("MAKE_PIC = 1\n")
            if "+liblbfgs" in spec:
                makefile_machine.write("HAVE_LIBLBFGS = 1\n")

    @property
    def build_targets(self):
        return ["MACHINE_TYPE={0}".format(self.machine_type)]

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("include", prefix.include)
        install_tree("man", prefix.man)

    def setup_run_environment(self, env):
        # Most executable files are in a subfolder named based on
        # the detected machine type. Unfortunately we cannot use
        # `machine_type` at this point but we can just guess as
        # there is only one subfolder.
        env.prepend_path("PATH", glob.glob(join_path(self.prefix.bin, "*", ""))[0])
