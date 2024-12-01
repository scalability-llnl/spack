# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hal(MakefilePackage):
    """HAL is a structure to efficiently store and index multiple
    genome alignments and ancestral reconstructions.

    HAL is a graph-based representation which provides several advantages
    over matrix/block-based formats such as MAF, such as
    improved scalability and the ability to perform queries with
    respect to an arbitrary reference or subtree."""

    homepage = "https://github.com/ComparativeGenomicsToolkit/hal"
    url = "https://github.com/ComparativeGenomicsToolkit/hal/archive/release-V2.1.tar.gz"

    version("2.1", sha256="540255be1af55abf390359fe034b82d7e61bdf6c3277df3cc01259cd450994e5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    maintainers("ilbiondo")

    # HAL expects to be compiled alongside sonlib so we need both the
    # source version and python library version

    depends_on("hdf5+cxx~mpi")
    depends_on("sonlib", type="build")
    depends_on("python", type="run")
    depends_on("py-sonlib", type="run")

    # As we install sonlib seperately the include.mk needs
    # editing to comment out an include

    def patch(self):
        includemk = FileFilter("include.mk")
        includemk.filter(
            r"^include  \$\{sonLibRootDir\}/include\.mk", "# include  ${sonLibRootDir}/include.mk"
        )

    def setup_build_environment(self, env):
        env.set("sonLibRootDir", self.spec["sonlib"].prefix)

    def install(self, spec, prefix):
        # First the easy bit

        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)

        # Copy the rest of the "toolkit" as to a directory named hal
        # in order that the python libraries can be found and used

        haldirs = [
            "alignmentDepth",
            "analysis",
            "api",
            "assemblyHub",
            "benchmarks",
            "blockViz",
            "doc",
            "extra",
            "extract",
            "fasta",
            "liftover",
            "lod",
            "maf",
            "modify",
            "mutations",
            "objs",
            "phyloP",
            "randgen",
            "stats",
            "synteny",
            "testdata",
            "validate",
        ]

        for folder in haldirs:
            install_tree(folder, join_path(self.prefix, "hal", folder))

        install("__init__.py", join_path(self.prefix, "hal"))

        # Now in order to make things useful we copy some python tools to bin

        halpyfiles = [
            "analysis/halContiguousRegions.py",
            "assemblyHub/hal2assemblyHub.py",
            "liftover/halLiftoverStatus.py",
            "lod/halLodBenchmark.py",
            "lod/halLodInterpolate.py",
            "maf/hal2mafMP.py",
            "phyloP/halPhyloPMP.py",
        ]

        for pyfile in halpyfiles:
            install(pyfile, self.prefix.bin)

    # The hal directory is a python library so we set the path
    # to be the installation root

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix)
