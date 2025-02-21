# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLabeling(RPackage):
    """Axis Labeling.

    Provides a range of axis labeling algorithms."""

    cran = "labeling"

    license("MIT OR custom")

    version("0.4.3", sha256="c62f4fc2cc74377d7055903c5f1913b7295f7587456fe468592738a483e264f2")
    version("0.4.2", sha256="e022d79276173e0d62bf9e37d7574db65ab439eb2ae1833e460b1cff529bd165")
    version("0.3", sha256="0d8069eb48e91f6f6d6a9148f4e2dc5026cabead15dd15fc343eff9cf33f538f")
