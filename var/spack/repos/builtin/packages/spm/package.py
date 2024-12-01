# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spm(Package):
    """Statistical Parametric Mapping refers to the construction and assessment
    of spatially extended statistical processes used to test hypotheses
    about functional imaging data. These ideas have been instantiated in
    software that is called SPM."""

    homepage = "https://www.fil.ion.ucl.ac.uk/spm/"
    url = "https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/spm12_r7219.zip"
    list_url = "https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/previous/"

    version(
        "12_r7219",
        sha256="b46fe8ce5ab537caeea7634c650f3a12fe2716f6a2e8ac15aa0d62b3652fe764",
        url="https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/previous/spm12_r7219_R2010a.zip",
    )

    depends_on("zip", type="build")
    depends_on("matlab", type="run")

    def install(self, spec, prefix):
        unzip = which("unzip")
        unzip("spm12.ctf")

        bash = which("bash")
        bash("./run_spm12.sh")

        install_tree("spm12", prefix)
