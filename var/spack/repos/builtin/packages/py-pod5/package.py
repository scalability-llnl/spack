# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPod5(PythonPackage):
    """
    POD5 is a file format for storing nanopore dna data in an easily accessible way.
    The format is able to be written in a streaming manner which allows a sequencing
    instrument to directly write the format.
    """

    homepage = "https://github.com/nanoporetech/pod5-file-format"
    url = "https://files.pythonhosted.org/packages/40/7b/5baef5b0627a14d78ec511b9ea5776a0e99ab8c54fb59ff391836de6597e/pod5-0.3.10-py3-none-any.whl"

    maintainers("Pandapip1")

    license("MPL-2.0", checked_by="Pandapip1")

    version(
        "0.3.10",
        sha256="3ecfce9d4d4b2574242b1effc313f3fd25ef4651c44385beb68ad5ba8f539b11",
        expand=False,
    )

    depends_on("py-setuptools@61.0:", type="build")

    depends_on("py-lib-pod5@0.3.10", type=("build", "run"))
    depends_on("py-iso8601", type=("build", "run"))
    depends_on("py-importlib-metadata", type=("build", "run"))
    depends_on("py-more-itertools", type=("build", "run"))
    depends_on("py-numpy@1.21.0:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("py-pyarrow@14.0", type=("build", "run"))
    depends_on("py-pytz", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-polars", type=("build", "run"))
    depends_on("py-h5py@3.10", type=("build", "run"))
    depends_on("py-vbz-h5py-plugin", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
