# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTorchsummary(PythonPackage):
    """Keras has a neat API to view the visualization of the model
    which is very helpful while debugging your network. Here is a
    barebone code to try and mimic the same in PyTorch. The aim is to
    provide information complementary to, what is not provided by
    print(your_model) in PyTorch."""

    homepage = "https://github.com/sksq96/pytorch-summary"
    pypi = "torchsummary/torchsummary-1.5.1.tar.gz"

    version("1.5.1", sha256="981bf689e22e0cf7f95c746002f20a24ad26aa6b9d861134a14bc6ce92230590")

    depends_on("py-setuptools", type="build")
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
