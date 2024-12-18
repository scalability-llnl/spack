# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Otf2(AutotoolsPackage):
    """The Open Trace Format 2 is a highly scalable, memory efficient event
    trace data format plus support library.
    """

    homepage = "https://www.vi-hps.org/projects/score-p"
    url = "https://perftools.pages.jsc.fz-juelich.de/cicd/otf2/tags/otf2-3.0/otf2-3.0.tar.gz"

    version("3.0.3", sha256="18a3905f7917340387e3edc8e5766f31ab1af41f4ecc5665da6c769ca21c4ee8")
    version("3.0", sha256="6fff0728761556e805b140fd464402ced394a3c622ededdb618025e6cdaa6d8c")
    version("2.3", sha256="36957428d37c40d35b6b45208f050fb5cfe23c54e874189778a24b0e9219c7e3")
    version(
        "2.2",
        sha256="d0519af93839dc778eddca2ce1447b1ee23002c41e60beac41ea7fe43117172d",
        deprecated=True,
    )
    version(
        "2.1.1",
        sha256="01591b42e76f396869ffc84672f4eaa90ee8ec2a8939755d9c0b5b8ecdcf47d3",
        deprecated=True,
    )
    version(
        "2.1",
        sha256="8ad38ea0461099e34f00f2947af4409ce9b9c379e14c3f449ba162e51ac4cad3",
        deprecated=True,
    )
    version(
        "2.0",
        sha256="bafe0ac08e0a13e71568e5774dc83bd305d907159b4ceeb53d2e9f6e29462754",
        deprecated=True,
    )
    version(
        "1.5.1",
        sha256="a4dc9f6c99376030b43a4c7b1ee77cfb530b03928ea688c6d1a380b3f4e8e488",
        deprecated=True,
    )
    version(
        "1.4",
        sha256="fb5fe169003c01e40848e224f09c440014e9872e84d2ca02ce7fffdd3f879a2f",
        deprecated=True,
    )
    version(
        "1.3.1",
        sha256="c4605ace845d89fb1a19223137b92cc503b01e3db5eda8c9e0715d0cfcf2e4b9",
        deprecated=True,
    )
    version(
        "1.2.1",
        sha256="1db9fb0789de4a9c3c96042495e4212a22cb581f734a1593813adaf84f2288e4",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        if version < Version("2.3"):
            return f"https://www.vi-hps.org/cms/upload/packages/otf2/otf2-{version}.tar.gz"

        return f"https://perftools.pages.jsc.fz-juelich.de/cicd/otf2/tags/otf2-{version}/otf2-{version}.tar.gz"

    extends("python")

    # `imp` module required
    depends_on("python@:3.11", type=("build", "run"))

    with when("@2.2 %cce"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")

    # Fix missing initialization of variable resulting in issues when used by
    # APEX/HPX: https://github.com/STEllAR-GROUP/hpx/issues/5239
    patch("collective_callbacks.patch", when="@2.1:")

    # when using Cray's cs-prgenv, allow the build system to detect the systems as an XC
    patch("cray_ac_scorep_sys_detection-m4.patch", when="@2.2 %cce")

    @property
    def force_autoreconf(self):
        return self.spec.satisfies("@2.2 %cce")

    def flag_handler(self, name, flags):
        if name == "cflags":
            flags.append(self.compiler.cc_pic_flag)
        elif name == "cxxflags":
            flags.append(self.compiler.cxx_pic_flag)
        return (flags, None, None)

    def configure_args(self):
        return [
            "--enable-shared",
            f"CC={spack_cc}",
            f"CXX={spack_cxx}",
            f"F77={spack_f77}",
            f"FC={spack_fc}",
            "PYTHON_FOR_GENERATOR=:",
        ]
