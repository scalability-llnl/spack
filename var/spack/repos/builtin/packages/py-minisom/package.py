# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMinisom(PythonPackage):
    """MiniSom is a minimalistic and Numpy based implementation of the Self
    Organizing Maps (SOM). SOM is a type of Artificial Neural Network able to
    convert complex, nonlinear statistical relationships between
    high-dimensional data items into simple geometric relationships on a
    low-dimensional display. Minisom is designed to allow researchers to easily
    build on top of it and to give students the ability to quickly grasp its
    details.

    The project initially aimed for a minimalistic implementation of the
    Self-Organizing Map (SOM) algorithm, focusing on simplicity in features,
    dependencies, and code style. Although it has expanded in terms of
    features, it remains minimalistic by relying only on the numpy library and
    emphasizing vectorization in coding style."""

    homepage = "https://github.com/JustGlowing/minisom"
    pypi = "MiniSom/MiniSom-2.3.1.tar.gz"

    version("2.3.1", sha256="c0f1411616d7614fbd440a811975c12c7dfc091baea33efb49f5f4eabad7b966")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
