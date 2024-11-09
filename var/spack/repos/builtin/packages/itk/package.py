# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Itk(CMakePackage):
    """The Insight Toolkit (ITK) is an open-source, cross-platform toolkit for
    N-dimensional scientific image processing, segmentation, and registration.

    The Insight Toolkit (ITK) is an open-source, cross-platform toolkit for
    N-dimensional scientific image processing, segmentation, and registration.
    Segmentation is the process of identifying and classifying data found in a
    digitally sampled representation. Typically the sampled representation is
    an image acquired from such medical instrumentation as CT or MRI scanners.
    Registration is the task of aligning or developing correspondences between
    data. For example, in the medical environment, a CT scan may be aligned
    with a MRI scan in order to combine the information contained in both."""

    homepage = "https://itk.org/"
    url = "https://github.com/InsightSoftwareConsortium/ITK/releases/download/v5.1.1/InsightToolkit-5.1.1.tar.gz"

    license("Apache-2.0")

    version("5.3.0", sha256="57a4471133dc8f76bde3d6eb45285c440bd40d113428884a1487472b7b71e383")
    version("5.3rc02", sha256="163aaf4a6cecd5b70ff718c1a986c746581797212fd1b629fa81f12ae4756d14")
    version(
        "5.2.1",
        sha256="192d41bcdd258273d88069094f98c61c38693553fd751b54f8cda308439555db",
        preferred=True,
    )
    version("5.2.0", sha256="12c9cf543cbdd929330322f0a704ba6925a13d36d01fc721a74d131c0b82796e")
    version("5.1.2", sha256="f1e5a78e11125348f68f655c6b89b617c3a8b2c09f710081f621054811a70c98")
    version("5.1.1", sha256="39e2a63840054361b728878a35b21bbe38374682ffb4b5c4f8f8f7514dedb58e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("review", default=False, description="enable modules under review")
    variant("rtk", default=False, description="build the RTK (Reconstruction Toolkit module")
    variant("minc", default=False, description="enable support for MINC files")
    variant("antspy", default=False, description="enable support features for antspy")

    # TODO: This will not work if the resource is pulled from a spack mirror.
    # The build process will checkout the appropriate commit but it needs to be
    # a git repository. The copy pulled from the mirror is not a git
    # repository.
    # NOTE: This problem is reflected in issues #8746 and #14344 and PR #9436.
    # resource(
    #     name='RTK',
    #     git='https://github.com/SimonRit/RTK.git',
    #     get_full_repo=True,
    #     destination='Modules/Remote',
    #     when='+rtk',
    # )

    depends_on("git", type="build")
    depends_on("perl", type="build")

    depends_on("eigen")
    depends_on("expat")
    depends_on("fftw-api")
    depends_on("googletest")
    depends_on("hdf5+cxx+hl")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("zlib-api")

    patch(
        "https://github.com/InsightSoftwareConsortium/ITK/commit/9a719a0d2f5f489eeb9351b0ef913c3693147a4f.patch?full_index=1",
        sha256="ec1f7fa71f2b7f05d9632c6b0321e7d436fff86fca92c60c12839b13ea79bd70",
        when="@5.2.0:5.3.0",
    )

    def cmake_args(self):
        use_mkl = self.spec["fftw-api"].name in INTEL_MATH_LIBRARIES
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("ITK_USE_SYSTEM_LIBRARIES", True),
            self.define("ITK_USE_MKL", use_mkl),
            self.define_from_variant("Module_ITKReview", "review"),
            self.define_from_variant("Module_RTK", "rtk"),
            self.define_from_variant("Module_ITKIOMINC", "minc"),
            self.define_from_variant("Module_ITKIOTransformMINC", "minc"),
            self.define_from_variant("Module_MGHIO", "antspy"),
            self.define_from_variant("Module_GenericLabelInterpolator", "antspy"),
            self.define_from_variant("Module_AdaptiveDenoising", "antspy"),
        ]

        if not use_mkl:
            args.extend(
                [
                    self.define("USE_FFTWD", True),
                    self.define("USE_FFTWF", True),
                    self.define("USE_SYSTEM_FFTW", True),
                ]
            )

        return args
