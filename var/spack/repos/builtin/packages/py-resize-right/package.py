# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyResizeRight(PythonPackage):
    """This is a resizing packge for images or tensors, that supports both
    Numpy and PyTorch (fully differentiable) seamlessly. The main motivation
    for creating this is to address some crucial incorrectness issues (see item
    3 in the list below) that exist in all other resizing packages I am
    aware of. As far as I know, it is the only one that performs correctly
    in all cases.  ResizeRight is specially made for machine learning,
    image enhancement and restoration challenges."""

    homepage = "https://github.com/assafshocher/ResizeRight"
    pypi = "resize-right/resize-right-0.0.2.tar.gz"

    license("MIT", checked_by="alex391")

    version("0.0.2", sha256="7dc35b72ce4012b77f7cc9049835163793ab98a58ab8893610fb119fe59af520")

    depends_on("py-setuptools", type="build")
    # needs py-numpy, py-torch, or both. py-numpy is lighter to install, so
    # always use py-numpy
    depends_on("py-numpy", type=("build", "run"))
    # and optionally use py-torch
    variant("torch", default=True, description="Enable py-torch")
    depends_on("py-torch", type=("build", "run"), when="+torch")
