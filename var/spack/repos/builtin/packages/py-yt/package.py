# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyYt(PythonPackage):
    """Volumetric Data Analysis

    yt is a python package for analyzing and visualizing
    volumetric, multi-resolution data from astrophysical
    simulations, radio telescopes, and a burgeoning
    interdisciplinary community.
    """

    homepage = "https://yt-project.org"
    git = "https://github.com/yt-project/yt.git"
    pypi = "yt/yt-4.1.2.tar.gz"

    maintainers("charmoniumq")

    license("BSD-3-Clause")

    version("4.1.2", sha256="0ae03288b067721baad14c016f253dc791cd444a1f2dd5d804cf91da622a0c76")
    version("3.6.1", sha256="be454f9d05dcbe0623328b4df43a1bfd1f0925e516be97399710452931a19bb0")
    version("3.6.0", sha256="effb00536f19fd2bdc18f67dacd5550b82066a6adce5b928f27a01d7505109ec")
    version("3.5.1", sha256="c8ef8eceb934dc189d63dc336109fad3002140a9a32b19f38d1812d5d5a30d71")
    version("3.5.0", sha256="ee4bf8349f02ce21f571654c26d85c1f69d9678fc8f5c7cfe5d1686c7ed2e3ca")
    version("3.4.1", sha256="a4cfc47fe21683e7a3b680c05fe2a25fb774ffda6e3939a35755e5bf64065895")
    version("3.4.0", sha256="de52057d1677473a83961d8a1119a9beae3121ec69a4a5469c65348a75096d4c")
    version("3.3.5", sha256="4d5c751b81b0daf6dcaff6ec0faefd97138c008019b52c043ab93403d71cedf6")
    version("3.3.4", sha256="64c109ba4baf5afc0e1bc276ed2e3de13f1c5ce85c6d8b4c60e9a47c54bf3bcb")
    version("3.3.3", sha256="edf6453927eee311d4b51afacb52cd5504b2b57cc6d3d92dab9c6bfaf6d883df")
    version("3.3.2", sha256="a18e4cf498349804c64eec6509ec4d3a6beaa34ea63366543290c35774337f0e")
    version("3.3.1", sha256="01e3b3398d43b8eab698d55ba37ef3d701ea026b899c0940a1ee34b215e25a31")
    version("3.3.0", sha256="537c67e85c8f5cc5530a1223a74d27eb7f11c459651903c3092c6a97b450d019")
    version("3.2.3", sha256="4d6ccf345d9fab965335c9faf8708c7eea79366b81d77f0f302808be3e82c0ed")
    version("3.2.2", sha256="78866f51e4751534ad60987000f149a8295952b99b37ca249d45e4d11095a5df")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("astropy", default=True, description="enable astropy support")
    variant("h5py", default=True, description="enable h5py support")
    variant("scipy", default=True, description="enable scipy support")
    variant("rockstar", default=False, description="enable rockstar support")

    # Main dependencies:
    # See https://github.com/yt-project/yt/blob/yt-4.1.2/setup.cfg#L40
    depends_on("py-cmyt@0.2.2:", type=("build", "run"), when="@4.1.2:")
    depends_on("py-ipywidgets@8:", type=("build", "run"), when="@4.1.2")
    depends_on("py-matplotlib@1.5.3:", type=("build", "run"))
    depends_on("py-matplotlib@:3.2.2", type=("build", "run"), when="@:3.6.0")
    depends_on("py-matplotlib@3.1:", type=("build", "run"), when="@4.1.2:")
    conflicts("^py-matplotlib@3.4.2", when="@4.1.2:")
    depends_on("py-more-itertools@8.4:", when="@4.1.2:")
    depends_on("py-numpy@1.10.4:", type=("build", "run"))
    depends_on("py-numpy@1.14.5:", type=("build", "run"), when="@4.1.2:")
    # https://github.com/yt-project/yt/pull/4859
    depends_on("py-numpy@:1", when="@:4.3.0", type=("build", "run"))
    depends_on("py-packaging@20.9:", type=("build", "run"), when="@4.1.2:")
    # PIL/pillow and pyparsing dependency is handled by matplotlib
    depends_on("py-tomli-w@0.4:", type=("build", "run"), when="@4.1.2:")
    depends_on("py-tqdm@3.4.0:", type=("build", "run"), when="@4.1.2:")
    depends_on("py-unyt@2.8:2", type=("build", "run"), when="@4.1.2:")
    depends_on("py-importlib-metadata@1.4:", type=("build", "run"), when="@4.1.2: ^python@:3.7")
    depends_on("py-tomli@1.2.3:", type=("build", "run"), when="@4.1.2: ^python@:3.10")
    depends_on("py-typing-extensions@4.2:", type=("build", "run"), when="@4.1.2: ^python@:3.7")
    # See https://github.com/spack/spack/pull/30418#discussion_r863962805
    depends_on("py-ipython@1.0:", type=("build", "run"), when="@:3")

    # Extras:
    # See https://github.com/yt-project/yt/blob/yt-4.1.2/setup.cfg#L80
    depends_on("py-h5py@3.1:3", type=("build", "run"), when="+h5py")
    depends_on("py-scipy@1.5.0:", type=("build", "run"), when="+scipy")
    depends_on("rockstar@yt", type=("build", "run"), when="+rockstar")
    depends_on("py-astropy@4.0.1:5", type=("build", "run"), when="+astropy")

    # Build dependencies:
    # See https://github.com/yt-project/yt/blob/yt-4.1.2/pyproject.toml#L2
    depends_on("py-cython@0.24:", type="build")
    depends_on("py-cython@0.29.21:2", type="build", when="@4.1.2:")
    depends_on("py-wheel@0.36.2:", type="build", when="@4.1.2:")
    depends_on("py-setuptools@19.6:", type=("build", "run"))
    depends_on("py-setuptools@59.0.1:", type=("build", "run"), when="@4.1.2:")

    @run_before("install")
    def prep_yt(self):
        if "+rockstar" in self.spec:
            with open("rockstar.cfg", "w") as rockstar_cfg:
                rockstar_cfg.write(self.spec["rockstar"].prefix)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        # The Python interpreter path can be too long for this
        # yt = Executable(join_path(prefix.bin, "yt"))
        # yt("--help")
        python(join_path(self.prefix.bin, "yt"), "--help")
