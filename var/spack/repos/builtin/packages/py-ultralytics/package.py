# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUltralytics(PythonPackage):
    """Ultralytics YOLOv8, developed by Ultralytics, is a cutting-edge, state-of-the-art
    (SOTA) model that builds upon the success of previous YOLO versions and introduces new
    features and improvements to further boost performance and flexibility. YOLOv8 is
    designed to be fast, accurate, and easy to use, making it an excellent choice for a
    wide range of object detection, image segmentation and image classification tasks."""

    homepage = "https://github.com/ultralytics/ultralytics"
    pypi = "ultralytics/ultralytics-8.0.50.tar.gz"

    license("AGPL-3.0")

    version("8.0.50", sha256="fdcb22300b63b72aa52da1713c33c01741aca031a61f15327eb6f02615bb4b97")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-matplotlib@3.2.2:", type=("build", "run"))
    depends_on("py-numpy@1.18.5:", type=("build", "run"))
    depends_on("opencv@4.6.0:+python3", type=("build", "run"))
    depends_on("pil@7.1.2:", type=("build", "run"))
    depends_on("py-pyyaml@5.3.1:", type=("build", "run"))
    depends_on("py-requests@2.23.0:", type=("build", "run"))
    depends_on("py-scipy@1.4.1:", type=("build", "run"))
    depends_on("py-torch@1.7.0:", type=("build", "run"))
    depends_on("py-torchvision@0.8.1:", type=("build", "run"))
    depends_on("py-tqdm@4.64.0:", type=("build", "run"))
    depends_on("py-tensorboard@2.4.1:", type=("build", "run"))
    depends_on("py-pandas@1.1.4:", type=("build", "run"))
    depends_on("py-seaborn@0.11.0:", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-thop@0.1.1:", type=("build", "run"))
    depends_on("py-certifi@2022.12.7:", type=("build", "run"))
    depends_on("py-sentry-sdk", type=("build", "run"))
