# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOntFast5Api(PythonPackage):
    """This project provides classes and utility functions for working with
    read fast5 files. It provides an abstraction layer between the underlying
    h5py library and the various concepts central to read fast5 files, such as
    "reads", "analyses", "analysis summaries", and "analysis datasets".
    Ideally all interaction with a read fast5 file should be possible via this
    API, without having to directly invoke the h5py library."""

    homepage = "https://github.com/nanoporetech/ont_fast5_api"
    pypi = "ont-fast5-api/ont-fast5-api-0.3.2.tar.gz"

    license("MPL-2.0")

    version("4.1.0", sha256="afa58fb0a73ac33161fe0d13d32698b3325756c370f2f440a8a43b4b68c75f32")
    version("0.3.2", sha256="ae44b1bcd812e8acf8beff3db92456647c343cf19340f97cff4847de5cc905d8")

    depends_on("python@3.6:", type=("build", "run"), when="@4:")
    depends_on("py-setuptools", type="build")
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-h5py@2.10:", type=("build", "run"), when="@4.0.1:")
    depends_on("py-numpy@1.8.1:", type=("build", "run"))
    depends_on("py-numpy@1.16:", type=("build", "run"), when="@3.2.0:")
    depends_on("py-packaging", type=("build", "run"), when="@3.0.2:")
    depends_on("py-progressbar33@2.3.1:", type=("build", "run"), when="@1.0.1:")
