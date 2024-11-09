# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyImagecodecs(PythonPackage):
    """Imagecodecs is a Python library that provides block-oriented,
    in-memory buffer transformation, compression, and decompression
    functions for use in the tifffile, czifile, zarr, and other
    scientific image input/output modules.."""

    homepage = "https://www.lfd.uci.edu/~gohlke/"
    pypi = "imagecodecs/imagecodecs-2022.2.22.tar.gz"

    license("BSD-3-Clause")

    version("2022.2.22", sha256="062bef6b003290a8163abed2744b406854238208dfdd41cf7165253c6e01c0bd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-numpy@1.19.2:", type=("build", "run"))
    # https://github.com/cgohlke/imagecodecs/issues/100
    depends_on("py-numpy@:1", when="@:2024.6.0", type=("build", "run"))
    depends_on("py-setuptools@18.0:", type="build")
    depends_on("py-cython@0.29.27:", type="build")
    depends_on("py-bitshuffle@0.3.5:", type=("build", "run"))

    depends_on("brotli@1.0.9:")
    depends_on("bzip2@1.0.8:")
    depends_on("c-blosc@1.21.1:")
    depends_on("cfitsio@3.49:")
    depends_on("giflib@5.2.1:")
    depends_on("jxrlib-debian@1.1: +shared")
    depends_on("lcms@2.13.1:")
    depends_on("libaec@1.0.6:")
    depends_on("libdeflate@1.10:")
    depends_on("jpeg")
    depends_on("liblzf@3.6:")
    depends_on("xz@5.2.5:")
    depends_on("libpng@1.6.37:")
    depends_on("libspng@0.7.2:")
    depends_on("libtiff@4.3.0:")
    depends_on("libwebp@1.2.2:")
    depends_on("openjpeg@2.4.0:")
    depends_on("snappy@1.1.9:")
    depends_on("zlib-api")
    depends_on("zlib@1.2.11:", when="^[virtuals=zlib-api] zlib")
    depends_on("zopfli@1.0.3: +shared")
    depends_on("zstd@1.5.2:")

    def patch(self):
        spec = self.spec

        filter_file(
            "'/usr/include/openjpeg-2.3', '/usr/include/openjpeg-2.4'",
            "'{0}',".format(
                join_path(
                    spec["openjpeg"].prefix.include,
                    "openjpeg-{0}".format(spec["openjpeg"].version.up_to(2)),
                )
            ),
            "setup.py",
        )
        # 238
        filter_file(
            "'/usr/include/zopfli'", "'{0}'".format(spec["zopfli"].prefix.include), "setup.py"
        )
        # 239
        filter_file(
            "append('/usr/include/jxrlib')",
            "extend(('{0}/libjxr/image', '{0}/libjxr/common', '{0}/libjxr/glue'))".format(  # noqa: E501
                spec["jxrlib-debian"].prefix.include
            ),
            "setup.py",
            string=True,
        )

        # 367
        filter_file(
            "'os.path.join(include_base_path, 'zopfli')'",
            "'{0}'".format(spec["zopfli"].prefix.include),
            "setup.py",
        )
        # 377
        filter_file(
            "'os.path.join(include_base_path, 'libjxr')'",
            "'{0}/libjxr'".format(spec["jxrlib-debian"].prefix.include),
            "setup.py",
        )
        # 397
        filter_file(
            "'os.path.join(libjpeg12_base_path, 'include')'",
            "'{0}'".format(spec["jpeg"].prefix.include),
            "setup.py",
        )
        # 454
        filter_file(
            "'os.path.join(os.environ['LIBRARY_INC'], 'openjpeg-' + os.environ['openjpeg'])'",  # noqa: E501
            "'{0}'".format(spec["openjpeg"].prefix.include),
            "setup.py",
        )
        # 473
        filter_file(
            "'os.path.join(os.environ['PREFIX'], 'include', 'zopfli')'",
            "'{0}'".format(spec["zopfli"].prefix.include),
            "setup.py",
        )
        # 476
        filter_file(
            "'os.path.join(os.environ['PREFIX'], 'include', 'jxrlib')'",
            "'{0}/libjxr'".format(spec["jxrlib-debian"].prefix.include),
            "setup.py",
        )
