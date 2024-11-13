# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPillowBase(PythonPackage):
    """Base class for Pillow and its fork Pillow-SIMD."""

    license("HPND")
    maintainers("adamjstewart")
    provides("pil")

    # These defaults correspond to Pillow defaults
    # https://pillow.readthedocs.io/en/stable/installation/building-from-source.html
    VARIANTS = (
        "zlib",
        "jpeg",
        "tiff",
        "freetype",
        "raqm",
        "lcms",
        "webp",
        "webpmux",
        "jpeg2000",
        "imagequant",
        "xcb",
    )
    variant("zlib", default=True, description="Compressed PNG functionality")
    variant("jpeg", default=True, description="JPEG functionality")
    variant("tiff", default=False, description="Compressed TIFF functionality")
    variant("freetype", default=False, description="Type related services")
    variant("raqm", when="@8.2:+freetype", default=False, description="RAQM support")
    variant("lcms", default=False, description="Color management")
    variant("webp", default=False, description="WebP format")
    variant("webpmux", when="@:10+webp", default=False, description="WebP metadata")
    variant("jpeg2000", default=False, description="JPEG 2000 functionality")
    variant("imagequant", when="@3.3:", default=False, description="Improved color quantization")
    variant("xcb", when="@7.1:", default=False, description="X11 screengrab support")

    # Required dependencies
    # https://pillow.readthedocs.io/en/stable/installation/python-support.html
    with default_args(type=("build", "link", "run")):
        depends_on("python@3.9:3.13", when="@11:")
        depends_on("python@3.8:3.13", when="@10.4")
        depends_on("python@3.8:3.12", when="@10.1:10.3")
        depends_on("python@3.8:3.11", when="@10.0")
        depends_on("python@3.7:3.11", when="@9.3:9.5")
        depends_on("python@3.7:3.10", when="@9.0:9.2")
        depends_on("python@3.6:3.10", when="@8.3.2:8.4")
        depends_on("python@3.6:3.9", when="@8:8.3.1")
        depends_on("python@3.5:3.8", when="@7.0:7.2")
        depends_on("python@2.7:2.8,3.5:3.8", when="@6.2.1:6.2.2")

    # pyproject.toml
    with default_args(type="build"):
        depends_on("py-pip@22.1:", when="@10:")
        depends_on("py-setuptools@67.8:", when="@10:")
        depends_on("py-setuptools")

    # Optional dependencies
    # https://pillow.readthedocs.io/en/stable/installation/building-from-source.html
    depends_on("zlib-api", when="+zlib")
    depends_on("jpeg", when="+jpeg")
    depends_on("libtiff", when="+tiff")
    depends_on("freetype", when="+freetype")
    depends_on("libraqm", when="+raqm")
    depends_on("lcms@2:", when="+lcms")
    depends_on("libwebp", when="+webp")
    depends_on("libwebp+libwebpmux+libwebpdemux", when="+webpmux")
    depends_on("openjpeg", when="+jpeg2000")
    depends_on("libimagequant", when="+imagequant")
    depends_on("libxcb", when="+xcb")

    @when("@10:")
    def config_settings(self, spec, prefix):
        settings = {"parallel": make_jobs}

        for variant in self.VARIANTS:
            if spec.satisfies(f"+{variant}"):
                settings[variant] = "enable"
            elif spec.satisfies(f"~{variant}"):
                settings[variant] = "disable"

        return settings

    def patch(self):
        """Patch setup.py to provide library and include directories for dependencies."""
        library_dirs = []
        include_dirs = []
        for dep in self.spec.dependencies(deptype="link"):
            query = self.spec[dep.name]
            library_dirs.extend(query.libs.directories)
            include_dirs.extend(query.headers.directories)

        setup = FileFilter("setup.py")
        if self.version >= Version("11"):
            setup.filter(
                "library_dirs: list[str] = []",
                "library_dirs = {0}".format(library_dirs),
                string=True,
            )
            setup.filter(
                "include_dirs: list[str] = []",
                "include_dirs = {0}".format(include_dirs),
                string=True,
            )
        else:
            setup.filter(
                "library_dirs = []", "library_dirs = {0}".format(library_dirs), string=True
            )
            setup.filter(
                "include_dirs = []", "include_dirs = {0}".format(include_dirs), string=True
            )

        if self.spec.satisfies("@:9"):

            def variant_to_cfg(variant):
                able = "enable" if "+" + variant in self.spec else "disable"
                return "{0}_{1}=1\n".format(able, variant)

            with open("setup.cfg", "a") as setup:
                setup.write("[build_ext]\n")
                for variant in self.VARIANTS:
                    setup.write(variant_to_cfg(variant))

                setup.write("rpath={0}\n".format(":".join(self.rpath)))
                setup.write("[install]\n")

    @when("@:9")
    def setup_build_environment(self, env):
        env.set("MAX_CONCURRENCY", make_jobs)


class PyPillow(PyPillowBase):
    """Pillow is a fork of the Python Imaging Library (PIL). It adds image
    processing capabilities to your Python interpreter. This library supports
    many file formats, and provides powerful image processing and graphics
    capabilities."""

    homepage = "https://python-pillow.org/"
    pypi = "pillow/pillow-10.2.0.tar.gz"

    version("11.0.0", sha256="72bacbaf24ac003fea9bff9837d1eedb6088758d41e100c1552930151f677739")
    version("10.4.0", sha256="166c1cd4d24309b30d61f79f4a9114b7b2313d7450912277855ff5dfd7cd4a06")
    version("10.3.0", sha256="9d2455fbf44c914840c793e89aa82d0e1763a14253a000743719ae5946814b2d")
    version("10.2.0", sha256="e87f0b2c78157e12d7686b27d63c070fd65d994e8ddae6f328e0dcf4a0cd007e")
    version("10.1.0", sha256="e6bf8de6c36ed96c86ea3b6e1d5273c53f46ef518a062464cd7ef5dd2cf92e38")
    version("10.0.1", sha256="d72967b06be9300fed5cfbc8b5bafceec48bf7cdc7dab66b1d2549035287191d")
    version("10.0.0", sha256="9c82b5b3e043c7af0d95792d0d20ccf68f61a1fec6b3530e718b688422727396")
    version("9.5.0", sha256="bf548479d336726d7a0eceb6e767e179fbde37833ae42794602631a070d630f1")
    version("9.4.0", sha256="a1c2d7780448eb93fbcc3789bf3916aa5720d942e37945f4056680317f1cd23e")
    version("9.3.0", sha256="c935a22a557a560108d780f9a0fc426dd7459940dc54faa49d83249c8d3e760f")
    version("9.2.0", sha256="75e636fd3e0fb872693f23ccb8a5ff2cd578801251f3a4f6854c6a5d437d3c04")
    version("9.1.1", sha256="7502539939b53d7565f3d11d87c78e7ec900d3c72945d4ee0e2f250d598309a0")
    version("9.1.0", sha256="f401ed2bbb155e1ade150ccc63db1a4f6c1909d3d378f7d1235a44e90d75fb97")
    version("9.0.1", sha256="6c8bc8238a7dfdaf7a75f5ec5a663f4173f8c367e5a39f87e720495e1eed75fa")
    version("9.0.0", sha256="ee6e2963e92762923956fe5d3479b1fdc3b76c83f290aad131a2f98c3df0593e")
    version("8.4.0", sha256="b8e2f83c56e141920c39464b852de3719dfbfb6e3c99a2d8da0edf4fb33176ed")
    version("8.0.0", sha256="59304c67d12394815331eda95ec892bf54ad95e0aa7bc1ccd8e0a4a5a25d4bf3")
    version("7.2.0", sha256="97f9e7953a77d5a70f49b9a48da7776dc51e9b738151b22dacf101641594a626")
    version("7.0.0", sha256="4d9ed9a64095e031435af120d3c910148067087541131e82b3e8db302f4c8946")
    version("6.2.2", sha256="db9ff0c251ed066d367f53b64827cc9e18ccea001b986d08c265e53625dab950")
    version("6.2.1", sha256="bf4e972a88f8841d8fdc6db1a75e0f8d763e66e3754b03006cbc3854d89f1cb1")

    depends_on("c", type="build")

    for ver in [
        "11.0.0",
        "10.4.0",
        "10.3.0",
        "10.2.0",
        "10.1.0",
        "10.0.1",
        "10.0.0",
        "9.5.0",
        "9.4.0",
        "9.3.0",
        "9.2.0",
        "9.1.1",
        "9.1.0",
        "9.0.1",
        "9.0.0",
        "8.4.0",
        "8.0.0",
        "7.2.0",
        "7.0.0",
        "6.2.2",
        "6.2.1",
    ]:
        provides("pil@" + ver, when="@" + ver)

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/{0}/{0}illow/{0}illow-{1}.tar.gz"
        if version >= Version("10.2"):
            letter = "p"
        else:
            letter = "P"
        return url.format(letter, version)
