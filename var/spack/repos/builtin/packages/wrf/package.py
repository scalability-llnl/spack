# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import re
import sys
import time
from os.path import basename
from pathlib import Path
from subprocess import PIPE, Popen

from llnl.util import tty

from spack.package import *

if sys.platform != "win32":
    from fcntl import F_GETFL, F_SETFL, fcntl
    from os import O_NONBLOCK

re_optline = re.compile(r"\s+[0-9]+\..*\((serial|smpar|dmpar|dm\+sm)\)\s+")
re_paroptname = re.compile(r"\((serial|smpar|dmpar|dm\+sm)\)")
re_paroptnum = re.compile(r"\s+([0-9]+)\.\s+\(")
re_nestline = re.compile(r"\(([0-9]+=[^)0-9]+)+\)")
re_nestoptnum = re.compile(r"([0-9]+)=")
re_nestoptname = re.compile(r"=([^,)]+)")


def setNonBlocking(fd):
    """
    Set the given file descriptor to non-blocking
    Non-blocking pipes are not supported on windows
    """
    flags = fcntl(fd, F_GETFL) | O_NONBLOCK
    fcntl(fd, F_SETFL, flags)


def collect_platform_options(stdoutpipe):
    # Attempt to parse to collect options
    optiondict = {}
    for line in stdoutpipe.splitlines():
        if re_optline.match(line):
            numbers = re_paroptnum.findall(line)
            entries = re_paroptname.findall(line)
            paropts = dict(zip(entries, numbers))
            platline = re_optline.sub("", line).strip()
            optiondict[platline] = paropts

    return optiondict


def collect_nesting_options(stdoutpipe):
    nestoptline = re_nestline.search(stdoutpipe)[0]
    nestoptnum = re_nestoptnum.findall(nestoptline)
    nestoptname = re_nestoptname.findall(nestoptline)
    nestoptname = [x.replace(" ", "_") for x in nestoptname]

    return dict(zip(nestoptname, nestoptnum))


class Wrf(Package):
    """The Weather Research and Forecasting (WRF) Model
    is a next-generation mesoscale numerical weather prediction system designed
    for both atmospheric research and operational forecasting applications.
    """

    homepage = "https://www.mmm.ucar.edu/weather-research-and-forecasting-model"
    url = "https://github.com/wrf-model/WRF/archive/v4.2.tar.gz"
    maintainers("MichaelLaufer", "ptooley")
    tags = ["windows"]

    version(
        "4.5.2",
        sha256="408ba6aa60d9cd51d6bad2fa075a3d37000eb581b5d124162885b049c892bbdc",
        url="https://github.com/wrf-model/WRF/releases/download/v4.5.2/v4.5.2.tar.gz",
    )
    version(
        "4.5.1",
        sha256="9d557c34c105db4d41e727843ecb19199233c7cf82c5369b34a2ce8efe65e2d1",
        url="https://github.com/wrf-model/WRF/releases/download/v4.5.1/v4.5.1.tar.gz",
    )
    version(
        "4.5.0",
        sha256="14fd78abd4e32c1d99e2e97df0370030a5c58ec84c343591bdc5e74f163c5525",
        url="https://github.com/wrf-model/WRF/releases/download/v4.5/v4.5.tar.gz",
    )
    version(
        "4.4.2",
        sha256="488b992e8e994637c58e3c69e869ad05acfe79419c01fbef6ade1f624e50dc3a",
        url="https://github.com/wrf-model/WRF/releases/download/v4.4.2/v4.4.2.tar.gz",
    )
    version(
        "4.4",
        sha256="6b649e5ac5532f74d74ab913950b632777ce349d26ebfb7f0042b80f9f4ee83e",
        url="https://github.com/wrf-model/WRF/releases/download/v4.4/v4.4.tar.gz",
    )
    version("4.3.3", sha256="1b98b8673513f95716c7fc54e950dfebdb582516e22758cd94bc442bccfc0b86")
    version("4.3.2", sha256="2c682da0cd0fd13f57d5125eef331f9871ec6a43d860d13b0c94a07fa64348ec")
    version("4.3.1", sha256="6c9a69d05ee17d2c80b3699da173cfe6fdf65487db7587c8cc96bfa9ceafce87")
    version("4.2.2", sha256="7be2968c67c2175cd40b57118d9732eda5fdb0828edaa25baf57cc289da1a9b8")
    version("4.2", sha256="c39a1464fd5c439134bbd39be632f7ce1afd9a82ad726737e37228c6a3d74706")
    version("4.0", sha256="9718f26ee48e6c348d8e28b8bc5e8ff20eafee151334b3959a11b7320999cf65")
    version(
        "3.9.1.1",
        sha256="a04f5c425bedd262413ec88192a0f0896572cc38549de85ca120863c43df047a",
        url="https://github.com/wrf-model/WRF/archive/V3.9.1.1.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "build_type",
        default="dmpar",
        description="Build type",
        values=("serial", "smpar", "dmpar", "dm+sm"),
    )
    variant(
        "nesting",
        default="basic",
        description="Nesting",
        values=("no_nesting", "basic", "preset_moves", "vortex_following"),
    )
    variant(
        "compile_type",
        default="em_real",
        description="Compile type",
        values=(
            "em_real",
            "em_quarter_ss",
            "em_b_wave",
            "em_les",
            "em_heldsuarez",
            "em_tropical_cyclone",
            "em_hill2d_x",
            "em_squall2d_x",
            "em_squall2d_y",
            "em_grav2d_x",
            "em_seabreeze2d_x",
            "em_scm_xy",
        ),
    )
    variant("pnetcdf", default=True, description="Parallel IO support through Pnetcdf library")
    variant("chem", default=False, description="Enable WRF-Chem", when="@4:")
    variant("netcdf_classic", default=False, description="Use NetCDF without HDF5 compression")
    variant("adios2", default=False, description="Enable IO support through ADIOS2 library")

    patch("patches/3.9/netcdf_backport.patch", when="@3.9.1.1")
    patch("patches/3.9/tirpc_detect.patch", when="@3.9.1.1")
    patch("patches/3.9/add_aarch64.patch", when="@3.9.1.1")
    patch("patches/3.9/configure_aocc_2.3.patch", when="@3.9.1.1 %aocc@:2.4.0")
    patch("patches/3.9/configure_aocc_3.0.patch", when="@3.9.1.1 %aocc@3.0.0")
    patch("patches/3.9/configure_aocc_3.1.patch", when="@3.9.1.1 %aocc@3.1.0")
    patch("patches/3.9/fujitsu.patch", when="@3.9.1.1 %fj")

    # These patches deal with netcdf & netcdf-fortran being two diff things
    # Patches are based on:
    # https://github.com/easybuilders/easybuild-easyconfigs/blob/master/easybuild/easyconfigs/w/WRF/WRF-3.5_netCDF-Fortran_separate_path.patch
    patch("patches/4.0/arch.Config.pl.patch", when="@4.0")
    patch("patches/4.0/arch.configure.defaults.patch", when="@4.0")
    patch("patches/4.0/arch.conf_tokens.patch", when="@4.0")
    patch("patches/4.0/arch.postamble.patch", when="@4.0")
    patch("patches/4.0/configure.patch", when="@4.0")
    patch("patches/4.0/external.io_netcdf.makefile.patch", when="@4.0")
    patch("patches/4.0/Makefile.patch", when="@4.0")
    patch("patches/4.0/tirpc_detect.patch", when="@4.0")
    patch("patches/4.0/add_aarch64.patch", when="@4.0")

    patch("patches/4.2/arch.Config.pl.patch", when="@4.2:4.5.1")
    patch("patches/4.2/arch.configure.defaults.patch", when="@=4.2")
    patch("patches/4.2/4.2.2_arch.configure.defaults.patch", when="@4.2.2")
    patch("patches/4.2/arch.conf_tokens.patch", when="@4.2:")
    patch("patches/4.2/arch.postamble.patch", when="@4.2")
    patch("patches/4.2/configure.patch", when="@4.2:4.3.3")
    patch("patches/4.2/external.io_netcdf.makefile.patch", when="@4.2:4.5.1")
    patch("patches/4.2/var.gen_be.Makefile.patch", when="@4.2:")
    patch("patches/4.2/Makefile.patch", when="@4.2")
    patch("patches/4.2/tirpc_detect.patch", when="@4.2")
    patch("patches/4.2/add_aarch64.patch", when="@4.2:4.3.1 %gcc target=aarch64:")
    patch("patches/4.2/add_aarch64_acfl.patch", when="@4.2:4.3.1 %arm target=aarch64:")
    patch("patches/4.2/configure_aocc_2.3.patch", when="@4.2 %aocc@:2.4.0")
    patch("patches/4.2/configure_aocc_3.0.patch", when="@4.2 %aocc@3.0.0:3.2.0")
    patch("patches/4.2/hdf5_fix.patch", when="@4.2:4.5.1 %aocc")
    patch("patches/4.2/derf_fix.patch", when="@=4.2 %aocc")
    patch(
        "patches/4.2/add_tools_flags_acfl2304.patch",
        when="@4.2:4.4.2 %arm@23.04.1: target=aarch64:",
    )

    patch("patches/4.3/add_aarch64.patch", when="@4.3.2:4.4.2 %gcc target=aarch64:")
    patch("patches/4.3/add_aarch64_acfl.patch", when="@4.3.2:4.4.2 %arm target=aarch64:")

    patch("patches/4.4/arch.postamble.patch", when="@4.4:4.5.1")
    patch("patches/4.4/configure.patch", when="@4.4:4.4.2")
    patch("patches/4.4/ifx.patch", when="@4.4: %oneapi")

    patch("patches/4.5/configure.patch", when="@4.5:")
    # Fix WRF to remove deprecated ADIOS2 functions
    # https://github.com/wrf-model/WRF/pull/1860
    patch("patches/4.5/adios2-remove-deprecated-functions.patch", when="@=4.5.0 ^adios2@2.9:")

    # Various syntax fixes found by FPT tool
    patch(
        "https://github.com/wrf-model/WRF/commit/6502d5d9c15f5f9a652dec244cc12434af737c3c.patch?full_index=1",
        sha256="c5162c23a132b377132924f8f1545313861c6cee5a627e9ebbdcf7b7b9d5726f",
        when="@4.2 %fj",
    )
    patch("patches/4.2/configure_fujitsu.patch", when="@4 %fj")

    patch("patches/4.3/Makefile.patch", when="@4.3:4.5.1")
    patch("patches/4.3/arch.postamble.patch", when="@4.3:4.3.3")
    patch("patches/4.3/fujitsu.patch", when="@4.3:4.4 %fj")
    # Syntax errors in physics routines
    patch(
        "https://github.com/wrf-model/WRF/commit/7c6fd575b7a8fe5715b07b38db160e606c302956.patch?full_index=1",
        sha256="1ce97f4fd09e440bdf00f67711b1c50439ac27595ea6796efbfb32e0b9a1f3e4",
        when="@4.3.1",
    )
    patch(
        "https://github.com/wrf-model/WRF/commit/238a7d219b7c8e285db28fe4f0c96ebe5068d91c.patch?full_index=1",
        sha256="27c7268f6c84b884d21e4afad0bab8554b06961cf4d6bfd7d0f5a457dcfdffb1",
        when="@4.3.1",
    )
    # Add ARM compiler support
    patch(
        "https://github.com/wrf-model/WRF/commit/4a084e03575da65f254917ef5d8eb39074abd3fc.patch?full_index=1",
        sha256="2d06d709074ded9bd6842aa83c0dfdad5a4e4e2df99e2e5d4a82579f0486117e",
        when="@4.5: %arm",
    )
    patch(
        "https://github.com/wrf-model/WRF/commit/6087d9192f7f91967147e50f5bc8b9e49310cf98.patch?full_index=1",
        sha256="7c6487aefaa6cda0fff3976e78da07b09d2ba6c005d649f35a0f8f1694a0b2bb",
        when="@4.5: %arm",
    )

    depends_on("pkgconfig", type=("build"))
    depends_on("libtirpc")

    depends_on("mpi")
    # According to:
    # http://www2.mmm.ucar.edu/wrf/users/docs/user_guide_v4/v4.0/users_guide_chap2.html#_Required_Compilers_and_1
    # Section: "Required/Optional Libraries to Download"
    depends_on("parallel-netcdf", when="+pnetcdf")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("jasper")
    depends_on("libpng")
    depends_on("zlib-api")
    depends_on("perl")
    depends_on("jemalloc", when="%aocc")
    # not sure if +fortran is required, but seems like a good idea
    depends_on("hdf5+fortran+hl+mpi")
    # build script use csh
    depends_on("tcsh", type=("build"))
    # time is not installed on all systems b/c bash provides it
    # this fixes that for csh install scripts
    depends_on("time", type=("build"))
    depends_on("m4", type="build")
    depends_on("libtool", type="build")
    depends_on("adios2", when="@4.5: +adios2")

    conflicts(
        "%oneapi", when="@:4.3", msg="Intel oneapi compiler patch only added for version 4.4"
    )
    phases = ["configure", "build", "install"]

    def setup_run_environment(self, env):
        env.set("WRF_HOME", self.prefix)
        env.append_path("PATH", self.prefix.main)
        env.append_path("PATH", self.prefix.tools)

    def setup_build_environment(self, env):
        # From 4.5.2 the split-netcdf patches are not needed,
        # just tell the build system where netcdf and netcdf-c are:
        if self.spec.satisfies("@4.5.2:"):
            env.set("NETCDF", self.spec["netcdf-fortran"].prefix)
            env.set("NETCDF_C", self.spec["netcdf-c"].prefix)
        else:
            env.set("NETCDF", self.spec["netcdf-c"].prefix)
        if "+pnetcdf" in self.spec:
            env.set("PNETCDF", self.spec["parallel-netcdf"].prefix)
        # Add WRF-Chem module
        if "+chem" in self.spec:
            env.set("WRF_CHEM", 1)
        if "+netcdf_classic" in self.spec:
            env.set("NETCDF_classic", 1)
        # This gets used via the applied patch files
        env.set("NETCDFF", self.spec["netcdf-fortran"].prefix)
        env.set("PHDF5", self.spec["hdf5"].prefix)
        env.set("JASPERINC", self.spec["jasper"].prefix.include)
        env.set("JASPERLIB", self.spec["jasper"].prefix.lib)

        if self.spec.satisfies("%aocc"):
            env.set("WRFIO_NCD_LARGE_FILE_SUPPORT", 1)
            env.set("HDF5", self.spec["hdf5"].prefix)
            env.prepend_path("PATH", ancestor(self.compiler.cc))

        if "+adios2" in self.spec:
            env.set("ADIOS2", self.spec["adios2"].prefix)

    def flag_handler(self, name, flags):
        # Force FCFLAGS/FFLAGS by adding directly into spack compiler wrappers.
        if self.spec.satisfies("@3.9.1.1: %gcc@10:") and name == "fflags":
            flags.extend(["-fallow-argument-mismatch", "-fallow-invalid-boz"])
        return (flags, None, None)

    def patch(self):
        # Let's not assume csh is intalled in bin
        files = glob.glob("*.csh")

        filter_file("^#!/bin/csh -f", "#!/usr/bin/env csh", *files)
        filter_file("^#!/bin/csh", "#!/usr/bin/env csh", *files)

    @run_before("configure", when="%aocc@4:")
    def create_aocc_config(self):
        param = {
            "MPICC": self.spec["mpi"].mpicc,
            "MPIFC": self.spec["mpi"].mpifc,
            "CTSM_SUBST": (
                "-DWRF_USE_CLM" if self.spec.satisfies("@:4.2.2") else "CONFIGURE_D_CTSM"
            ),
            "NETCDFPAR_BUILD": (
                "CONFIGURE_NETCDFPAR_BUILD" if self.spec.satisfies("@4.4.0:") else ""
            ),
        }

        zen_conf = (Path(__file__).parent / "aocc_config.inc").read_text().format(**param)

        if self.spec.satisfies("@4.0:"):
            filter_file("#insert new stanza here", zen_conf, "arch/configure.defaults")
        else:
            filter_file("#insert new stanza here", zen_conf, "arch/configure_new.defaults")

    def answer_configure_question(self, outputbuf):
        # Platform options question:
        if "Please select from among the following" in outputbuf:
            options = collect_platform_options(outputbuf)
            comp_pair = "%s/%s" % (
                basename(self.compiler.fc).split("-")[0],
                basename(self.compiler.cc).split("-")[0],
            )
            compiler_matches = dict((x, y) for x, y in options.items() if comp_pair in x.lower())
            if len(compiler_matches) > 1:
                tty.warn("Found multiple potential build options")
            try:
                compiler_key = min(compiler_matches.keys(), key=len)
                tty.warn("Selected build option %s." % compiler_key)
                return (
                    "%s\n" % compiler_matches[compiler_key][self.spec.variants["build_type"].value]
                )
            except KeyError:
                InstallError(
                    "build_type %s unsupported for %s compilers"
                    % (self.spec.variants["build_type"].value, comp_pair)
                )

        if "Compile for nesting?" in outputbuf:
            options = collect_nesting_options(outputbuf)
            try:
                return "%s\n" % options[self.spec.variants["nesting"].value]
            except KeyError:
                InstallError("Failed to parse correct nesting option")

    def do_configure_fixup(self):
        # Fix mpi compiler wrapper aliases

        # In version 4.2 the file to be patched is called
        # configure.defaults, while in earlier versions
        # it's configure_new.defaults
        if self.spec.satisfies("@3.9.1.1"):
            config = FileFilter(join_path("arch", "configure_new.defaults"))
        else:
            config = FileFilter(join_path("arch", "configure.defaults"))

        if self.spec.satisfies("@3.9.1.1 %gcc"):
            # Compiling with OpenMPI requires using `-DMPI2SUPPORT`.
            other_flags = " -DMPI2SUPPORT" if self.spec.satisfies("^openmpi") else ""
            config.filter(
                r"^DM_FC.*mpif90 -f90=\$\(SFC\)",
                "DM_FC = {0}".format(self.spec["mpi"].mpifc) + other_flags,
            )
            config.filter(
                r"^DM_CC.*mpicc -cc=\$\(SCC\)",
                "DM_CC = {0}".format(self.spec["mpi"].mpicc) + other_flags,
            )

        if self.spec.satisfies("%aocc"):
            config.filter(
                "^DM_FC.*mpif90 -DMPI2SUPPORT",
                "DM_FC = {0}".format(self.spec["mpi"].mpifc + " -DMPI2_SUPPORT"),
            )
            config.filter(
                "^DM_.CC*mpicc -DMPI2SUPPORT",
                "DM_CC = {0}".format(self.spec["mpi"].mpicc) + " -DMPI2_SUPPORT",
            )

        if self.spec.satisfies("@4.2: %intel"):
            config.filter("^DM_FC.*mpif90", "DM_FC = {0}".format(self.spec["mpi"].mpifc))
            config.filter("^DM_CC.*mpicc", "DM_CC = {0}".format(self.spec["mpi"].mpicc))

        if self.spec.satisfies("@:4.0.3 %intel@2018:"):
            config.filter(r"-openmp", "-qopenmp")

        if self.spec.satisfies("%gcc@14:"):
            config.filter(
                "^CFLAGS_LOCAL(.*?)=([^#\n\r]*)(.*)$", r"CFLAGS_LOCAL\1= \2 -fpermissive \3"
            )
            config.filter("^CC_TOOLS(.*?)=([^#\n\r]*)(.*)$", r"CC_TOOLS\1=\2 -fpermissive \3")

    @run_before("configure")
    def fortran_check(self):
        if not self.compiler.fc:
            msg = "cannot build WRF without a Fortran compiler"
            raise RuntimeError(msg)

    def configure(self, spec, prefix):
        # Remove broken default options...
        self.do_configure_fixup()

        if self.spec.compiler.name not in ["intel", "gcc", "arm", "aocc", "fj", "oneapi"]:
            raise InstallError(
                "Compiler %s not currently supported for WRF build." % self.spec.compiler.name
            )

        p = Popen("./configure", stdin=PIPE, stdout=PIPE, stderr=PIPE)
        if sys.platform != "win32":
            setNonBlocking(p.stdout)
            setNonBlocking(p.stderr)

        # Because of WRFs custom configure scripts that require interactive
        # input we need to parse and respond to questions.  The details can
        # vary somewhat with the exact version, so try to detect and fail
        # gracefully on unexpected questions.
        stallcounter = 0
        outputbuf = ""
        while True:
            line = p.stderr.readline().decode()
            if not line:
                line = p.stdout.readline().decode()
            if not line:
                if p.poll() is not None:
                    returncode = p.returncode
                    break
                if stallcounter > 300:
                    raise InstallError(
                        "Output stalled for 30s, presumably an " "undetected question."
                    )
                time.sleep(0.1)  # Try to do a bit of rate limiting
                stallcounter += 1
                continue
            sys.stdout.write(line)
            stallcounter = 0
            outputbuf += line
            if "Enter selection" in outputbuf or "Compile for nesting" in outputbuf:
                answer = self.answer_configure_question(outputbuf)
                p.stdin.write(answer.encode())
                p.stdin.flush()
                outputbuf = ""

        if returncode != 0:
            raise InstallError("Configure failed - unknown error")

    @run_after("configure")
    def patch_for_libmvec(self):
        if self.spec.satisfies("@3.9.1.1 %aocc"):
            fp = self.package_dir + "/patches/3.9/aocc_lmvec.patch"
            which("patch")("-s", "-p1", "-i", "{0}".format(fp), "-d", ".")

    def run_compile_script(self):
        csh_bin = self.spec["tcsh"].prefix.bin.csh
        csh = Executable(csh_bin)

        # num of compile jobs capped at 20 in wrf
        num_jobs = str(min(int(make_jobs), 20))

        # Now run the compile script and track the output to check for
        # failure/success We need to do this because upstream use `make -i -k`
        # and the custom compile script will always return zero regardless of
        # success or failure
        result_buf = csh(
            "./compile",
            "-j",
            num_jobs,
            self.spec.variants["compile_type"].value,
            output=str,
            error=str,
        )

        print(result_buf)
        if "Executables successfully built" in result_buf:
            return True

        return False

    def build(self, spec, prefix):
        result = self.run_compile_script()

        if not result:
            tty.warn("Compilation failed first time (WRF idiosyncrasies?) " "- trying again...")
            result = self.run_compile_script()

        if not result:
            raise InstallError("Compile failed. Check the output log for details.")

    def install(self, spec, prefix):
        # Save all install files as many are needed for WPS and WRF runs
        install_tree(".", prefix)
