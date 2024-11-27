# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAwkward0(PythonPackage):
    """Manipulate arrays of complex data structures as easily as Numpy.

    Awkward Array is a pure Python+Numpy library for manipulating complex data
    structures as you would Numpy arrays."""

    homepage = "https://github.com/scikit-hep/awkward-0.x"
    pypi = "awkward0/awkward0-0.15.5.tar.gz"

    version("0.15.5", sha256="156e6e338c56d857a7bb53c4fcc8b0b2592a3470eff0d854e6d68777986359ad")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest-runner", type="build")
    depends_on("py-numpy@1.13.1:", type=("build", "run"))
