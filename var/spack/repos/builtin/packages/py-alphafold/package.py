# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class PyAlphafold(PythonPackage, CudaPackage):
    """AlphaFold is an AI system developed by DeepMind that predicts a
    protein's 3D structure from its amino acid sequence. It regularly
    achieves accuracy competitive with experiment."""

    homepage = "https://github.com/deepmind/alphafold"
    url = "https://github.com/deepmind/alphafold/archive/refs/tags/v2.1.1.tar.gz"
    maintainers("aweits")

    license("Apache-2.0")

    version("2.2.4", sha256="8d756e16f6dc7897331d834aade8493820d0ff6a03bf60ce511bac4756c1b1e8")
    version("2.1.1", sha256="1adb6e213ba9ac321fc1acb1c563ba9b4fc054c1cebe1191bc0e2aaa671dadf7")

    conflicts("platform=darwin", msg="alphafold is only supported on Linux")

    # lots of hints on versions and patching taken from docker/Dockerfile
    # and requirements.txt
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-absl-py@0.13.0:", type=("build", "run"), when="@2.1.1")
    depends_on("py-absl-py@1.0.0:", type=("build", "run"), when="@2.2.4")
    depends_on("py-biopython@1.79:", type=("build", "run"))
    depends_on("py-chex@0.0.7:", type=("build", "run"))
    depends_on("py-dm-haiku@0.0.4:", type=("build", "run"), when="@2.1.1")
    depends_on("py-dm-haiku@0.0.7:", type=("build", "run"), when="@2.2.4")
    depends_on("py-dm-tree@0.1.6:", type=("build", "run"))
    depends_on("py-docker", type=("build", "run"))
    depends_on("py-immutabledict@2.0.0:", type=("build", "run"))
    depends_on("py-jax@0.2.14:", type=("build", "run"), when="@2.1.1")
    depends_on("py-jax@0.3.17:", type=("build", "run"), when="@2.2.4")
    depends_on("py-ml-collections@0.1.0:", type=("build", "run"))
    depends_on("py-numpy@1.19.5:", type=("build", "run"), when="@2.1.1")
    depends_on("py-numpy@1.21.6:", type=("build", "run"), when="@2.2.4")
    depends_on("py-pandas@1.3.4:", type=("build", "run"))
    depends_on("py-protobuf@3.19:", type=("build", "run"), when="@2.2.4")
    depends_on("py-scipy@1.7.0:", type=("build", "run"))
    depends_on("py-pdbfixer@1.7", type=("build", "run"))
    depends_on("py-tensorflow@2.5:", type=("build", "run"), when="@2.1.1")
    depends_on("py-tensorflow@2.9:", type=("build", "run"), when="@2.2.4")
    depends_on(
        "openmm@7.5.1+cuda",
        type="run",
        patches=[
            patch(
                "https://raw.githubusercontent.com/google-deepmind/alphafold/2819de4ddd075340b81d36bcf7932a0ff0fbe404/docker/openmm.patch",
                sha256="a5a0ced820f3ecc56ae634c3111f80614863559b0587954a2658c8d4b2a07ae3",
                working_dir="wrappers/python",
                level=0,
            )
        ],
    )
    depends_on("hmmer", type="run")
    depends_on("kalign", type="run")
    depends_on("hh-suite", type="run")
    depends_on("aria2", type="run")

    resource(
        name="chemprops",
        url="https://git.scicore.unibas.ch/schwede/openstructure/-/raw/7102c63615b64735c4941278d92b554ec94415f8/modules/mol/alg/src/stereo_chemical_props.txt",
        destination="",
        sha256="24510899eeb49167cffedec8fa45363a4d08279c0c637a403b452f7d0ac09451",
        expand=False,
        placement="chemprops",
    )

    @run_after("install")
    def install_scripts(self):
        mkdirp(self.prefix.bin)
        shebang = f"#!{python.path}\n"
        for fname in glob.glob("run_alphafold*.py"):
            destfile = join_path(self.prefix.bin, fname)
            with open(fname, "r") as src:
                srcdata = src.read()
            with open(destfile, "w") as dest:
                dest.write(shebang + srcdata)
                set_executable(destfile)

        python_dir = join_path(self.prefix, python_platlib, "alphafold", "common")
        install("chemprops/stereo_chemical_props.txt", python_dir)
        install_tree("scripts", self.prefix.scripts)
