# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCellprofilerCore(PythonPackage):
    """Core classes and components used by CellProfiler."""

    homepage = "https://github.com/CellProfiler/core"
    pypi = "cellprofiler-core/cellprofiler-core-4.2.6.tar.gz"

    maintainers("omsai")

    license("BSD-3-Clause", checked_by="omsai")

    version("4.2.6", sha256="91993485783bbab87d89a728260f10e57fda3f7335e6057393702cea774db2d7")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-boto3@1.12.28:", type=("build", "run"))
    depends_on("py-centrosome@1.2.2:", type=("build", "run"))
    depends_on("py-docutils@0.15.2:", type=("build", "run"))
    depends_on("py-h5py@3.6:3.7~mpi", type=("build", "run"))
    depends_on("py-matplotlib@3.1.3:", type=("build", "run"))
    depends_on("py-numpy@1.18.2:", type=("build", "run"))
    depends_on("py-prokaryote@2.4.4:", type=("build", "run"))
    depends_on("py-psutil@5.7:", type=("build", "run"))
    depends_on("py-python-bioformats@4.0.7:", type=("build", "run"))
    depends_on("py-python-javabridge@4.0.3:", type=("build", "run"))
    depends_on("py-pyzmq@22.3:22", type=("build", "run"))
    depends_on("py-scikit-image@0.18.3:0", type=("build", "run"))
    depends_on("py-scipy@1.4.1:", type=("build", "run"))
