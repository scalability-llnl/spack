# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiobbStructureUtils(PythonPackage):
    """Biobb_structure_utils is the Biobb module collection to modify or extract information
    from a PDB structure file, such as pulling out a particular model or chain, removing water
    molecules or ligands, or renumbering or sorting atoms or residues"""

    pypi = "biobb_structure_utils/biobb_structure_utils-4.1.0.tar.gz"

    maintainers("d-beltran")

    # Versions
    version("4.1.0", sha256="07c6268e2f40de595325aaf88839dd180950ba5bd7e51acbf726a9b982fe69cd")

    # Dependencies
    depends_on("py-setuptools", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-biobb-common@4.1.0", type=("build", "run"))
    depends_on("py-biobb-structure-checking@3.13.4", type=("build", "run"))
