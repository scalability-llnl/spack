# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Rivet(AutotoolsPackage):
    """Rivet - the particle-physics MC analysis toolkit"""

    homepage = "https://rivet.hepforge.org/"
    url = "https://rivet.hepforge.org/downloads/?f=Rivet-3.1.4.tar.bz2"
    git = "https://gitlab.com/hepcedar/rivet.git"

    tags = ["hep"]

    license("GPL-3.0-or-later")

    version("4.0.2", sha256="65a3b36f42bff782ed2767930e669e09b140899605d7972fc8f77785b4a882c0")
    version("4.0.1", sha256="4e8692d6e8a53961c77983eb6ba4893c3765cf23f705789e4d865be4892eff79")
    version("4.0.0", sha256="d3c42d9b83ede3e7f4b534535345c2e06e6dafb851454c2b0a5d2331ab0f04d0")
    version("3.1.10", sha256="458b8e0df1de738e9972d24b260eaa087df12c99d4fe9dee5377d47ea6a49919")
    version("3.1.9", sha256="f6532045da61eeb2adc20a9abc4166b4b2d41ab2c1ca5b500cd616bb1b92e7b1")
    version("3.1.8", sha256="75b3f3d419ca6388d1fd2ec0eda7e1f90f324b996ccf0591f48a5d2e28dccc13")
    version("3.1.7", sha256="27c7dbbcb5fd7ee81caf136daf4e960bca0ec255d9fa1abe602f4d430861b27a")
    version("3.1.6", sha256="1cf6ebb6a79d181c441d1d0c7c6d623c423817c61093f36f21adaae23e679090")
    version("3.1.4", sha256="37edc80a2968ce1031589e43ba6b492877ca7901bea38f8bb7536a5c8cf8100d")
    version("3.1.3", sha256="53ddce41705b9c22b2eaa90603f6659aa9bf46c466d8772ca9dbe4430972e021")
    version("3.1.2", sha256="c041d09644f4eae7c212d82237033267fbc1583dfbb4e3e67377f86cece9577a")
    version("3.1.1", sha256="7c98b26af5f859bc65200499d15765e4b056b4cf233b34176f27a7e6bc4cf9b1")
    version("3.1.0", sha256="4e156daee5eb10bd1573ef32d4a6a6df74788cd9180fc977db93ef4cb281000c")
    version("3.0.2", sha256="9624d6cdcad77eafde40312cf6a1c97f4263f22faf9244b198c140b2c256d2f3")
    version("3.0.1", sha256="e7551168b86a05c9c029c319c313a0aa142a476195e7ff986c896c1b868f89dd")
    version("3.0.0", sha256="3944434d3791dccb54f7b2257589df6252cc7c065ce9deb57fbef466ff9e62b1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "hepmc",
        default="2",
        values=(conditional("2", when="@:3"), "3"),
        description="HepMC version to link against",
    )

    # According to A. Buckley (main Rivet developer):
    # "typically a given Rivet version will work with
    # all YODA releases of that middle-digit version,
    # and maybe older. Generally it's always a good idea
    # to be using the latest versions of both.". The versions below
    # are taken from LCG stack which, in most cases, is the definition
    # of "latest" at the moment of release.
    depends_on("yoda@1.7.7", when="@3.0.1")
    depends_on("yoda@1.8.0", when="@3.1.0")
    depends_on("yoda@1.8.2", when="@3.1.1")
    depends_on("yoda@1.8.3", when="@3.1.2")
    depends_on("yoda@1.8.5:", when="@3.1.3:")
    depends_on("yoda@1.9.6:", when="@3.1.6:")
    depends_on("yoda@1.9.7:", when="@3.1.7:")
    depends_on("yoda@1.9.8:", when="@3.1.8:")
    depends_on("yoda@1.9.9:", when="@3.1.9:")
    depends_on("yoda@1.9.10:", when="@3.1.10:")
    depends_on("yoda@:1", when="@:3")
    depends_on("yoda@2.0.1:", when="@4.0.0:")

    # The following versions were not a part of LCG stack
    # and thus the exact version of YODA is unknown
    depends_on("yoda@1.7.0:1.7", when="@3.0.0,3.0.2")

    depends_on("hepmc", when="hepmc=2")
    depends_on("hepmc3", when="hepmc=3")
    conflicts(
        "hepmc@3.3.0", when="@:4.0.0 hepmc=3", msg="patch-level zero requires at least 4.0.1"
    )
    depends_on("fastjet plugins=cxx")
    depends_on("fastjet@3.4.0:", when="@3.1.7:")
    depends_on("fjcontrib")
    depends_on("highfive", when="@4:")
    depends_on("python", type=("build", "run"))
    depends_on("py-cython@0.24.0:", type="build")
    depends_on("swig", type="build")

    depends_on("autoconf", type="build")
    depends_on("autoconf@2.71:", when="@3.1.7", type="build")
    depends_on("autoconf@2.68:", when="@3.1.7b:", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    extends("python")

    filter_compiler_wrappers("rivet-build", relative_root="bin")

    # fix missing headers in 4.0.x
    patch(
        "https://gitlab.com/hepcedar/rivet/-/merge_requests/973.diff",
        sha256="e1ff65c8dfe80c0b1bb8ad9960754932541064dd5334311a8bd5a377374a9926",
        when="@4:4.0.2",
    )

    patch("rivet-3.0.0.patch", when="@3.0.0", level=0)
    patch("rivet-3.0.1.patch", when="@3.0.1", level=0)
    patch("rivet-3.1.0.patch", when="@3.1.0", level=0)
    patch("rivet-3.1.1.patch", when="@3.1.1", level=0)

    @run_before("configure")
    def copy_gsl_m4(self):
        copy(join_path(os.path.dirname(__file__), "gsl.m4"), "m4/gsl.m4")

    @property
    def force_autoreconf(self):
        return True

    def setup_build_environment(self, env):
        # this avoids an "import site" error in the build
        env.unset("PYTHONHOME")

    def flag_handler(self, name, flags):
        if self.spec.satisfies("@3.1.2:") and name == "cxxflags":
            flags.append("-faligned-new")
            return (None, None, flags)
        return (flags, None, None)

    def configure_args(self):
        args = []
        if self.spec.variants["hepmc"].value == "2":
            args += ["--with-hepmc=" + self.spec["hepmc"].prefix]
        else:
            args += ["--with-hepmc3=" + self.spec["hepmc3"].prefix]
            args += ["--with-hepmc3-libpath=" + self.spec["hepmc3"].libs.directories[0]]

        args += ["--with-fastjet=" + self.spec["fastjet"].prefix]
        args += ["--with-yoda=" + self.spec["yoda"].prefix]

        args += ["--with-fjcontrib=" + self.spec["fjcontrib"].prefix]

        if self.spec.satisfies("^highfive"):
            args += ["--with-highfive=" + self.spec["highfive"].prefix]

        args += ["--disable-pdfmanual"]

        return args
