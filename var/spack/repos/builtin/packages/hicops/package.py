# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hicops(CMakePackage):
    """HiCOPS is a software framework for accelerating database peptide search
    workflows on supercomputers. HiCOPS provided algorithm-independent
    parallelizations and optimizations can be extended into new HPC database search
    algorithms or scalably accelerate the existing ones.
    """

    homepage = "https://hicops.github.io/index"
    git = "https://github.com/hicops/hicops.git"
    maintainers("pcdslab", "mhaseeb123", "nessiecancode")

    version("release", branch="release")
    version("develop", branch="develop")

    depends_on("cxx", type="build")  # generated

    # Build Options
    variant("mpi", default=True, description="Enable MPI support.")
    variant(
        "timemory",
        default=False,
        description="Enable timemory interface. Requires timemory " "installation.",
    )
    variant(
        "mpip",
        default=False,
        description="Enables the MPIP data_tracker via Timemory. "
        "Requires timemory installation.",
    )
    variant(
        "tailfit",
        default=True,
        description="Use the tailfit method instead of Gumbelfit " "for e-value computation.",
    )
    variant("progress", default=True, description="Display HiCOPS progress marks.")
    variant(
        "seqlen",
        default="60",
        description="Allowed maximum peptide sequence length.",
        values=int,
        multi=False,
    )
    variant(
        "qalen",
        default="100",
        description="Maximum number of top K peaks to keep when " "spectrum preprocess.",
        values=int,
        multi=False,
    )
    variant(
        "qchunk",
        default="10000",
        description="Max size of each batch extracted from the " "dataset.",
        values=int,
        multi=False,
    )
    variant(
        "hyperscore",
        default="100",
        description="Maximum allowed hyperscore computed.",
        values=int,
        multi=False,
    )
    variant(
        "shdpeaks",
        default="80",
        description="Maximum shared b- or y-ions allowed.",
        values=int,
        multi=False,
    )
    variant("cxx_std", default="14", description="C++ standard", values=("14", "17"), multi=False)

    depends_on("py-numpy")
    depends_on("py-python-dateutil")
    depends_on("py-setuptools")
    depends_on("py-bottleneck")
    depends_on("py-pyparsing")
    depends_on("py-six")
    depends_on("py-setuptools-scm")
    depends_on("py-et-xmlfile")
    depends_on("py-cython")
    depends_on("py-cycler")
    depends_on("py-pytz")
    depends_on("py-kiwisolver")
    depends_on("py-numexpr")
    depends_on("py-matplotlib")
    depends_on("py-jdcal")
    depends_on("py-pandas")
    depends_on("py-openpyxl")
    depends_on("python@3.7:3.9")
    depends_on("boost")
    depends_on("mpich")
    depends_on("git", type="build", when="@release")
    depends_on("git", type="build", when="@develop")
    depends_on("cmake@3.11:", type="build")
    depends_on("pkgconfig", type="build")
    # TODO: Add timemory and mpip depends_on()

    conflicts("+timemory")
    # Build failing when added. Creating a conflict as a workaround
    conflicts("%gcc@:7.2.0")
    conflicts("+mpip -timemory")
    conflicts("+mpip -mpi")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.tools)
        env.prepend_path("PATH", self.prefix.bin.tools)
        env.set("HICOPS_INSTALL", self.prefix)
        env.prepend_path("INCLUDE", self.prefix.include)

    def cmake_args(self):
        args = [
            self.define("USE_MPI", True),
            self.define("CMAKE_INSTALL_PREFIX", self.prefix),
            self.define_from_variant("USE_TIMEMORY", "timemory"),
            self.define_from_variant("USE_MPIP_LIBRARY", "mpip"),
            self.define_from_variant("TAILFIT", "tailfit"),
            self.define_from_variant("PROGRESS", "progress"),
            self.define_from_variant("MAX_SEQ_LEN", "seqlen"),
            self.define_from_variant("QALEN", "qalen"),
            self.define_from_variant("QCHUNK", "qchunk"),
            self.define_from_variant("MAX_HYPERSCORE", "hyperscore"),
            self.define_from_variant("MAX_SHDPEAKS", "shdpeaks"),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxx_std"),
        ]

        return args
