# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMne(PythonPackage):
    """MNE python project for MEG and EEG data analysis."""

    homepage = "https://mne.tools/"
    pypi = "mne/mne-0.23.4.tar.gz"
    git = "https://github.com/mne-tools/mne-python.git"

    maintainers("ChristopherChristofi")

    license("BSD-3-Clause")

    version("1.7.1", sha256="a87bbc998b792532d2c87add8b0f7bbf28a4d8cf5db1bdfb6d6e260791754498")
    version("1.6.1", sha256="e4f5683d01cef675eddad788bdb6b44cc015dff0fb1ddfca3c4105edfb757ef8")
    version("1.4.2", sha256="dd2bf35a90d951bef15ff3a651045b0373eff26018a821667109c727d55c7d63")
    version("1.4.0", sha256="7834f5b79c2c9885ca601bbddd8db3c2b2f37c34443fc0caf0447751f6c37a2a")
    version("1.3.1", sha256="0d0626d3187dd0ee6f8740d054660a1b5fce4c879f814b745b13c5a587baf32b")
    version("1.2.3", sha256="b300dcee69ffb878cdbc5c02490e877df385c1b9482622e3aa1da06a604a6e37")
    version("1.2.2", sha256="d40743d6ca7ae3919a557166fd5fc4c00a9719e40c07346baad57964e15f02bb")
    version("0.23.4", sha256="ecace5caacf10961ebb74cc5e0ead4d4dbc55fed006eab1e644da144092354e9")
    version("0.18.2", sha256="aa2e72ad3225efdad39b05e67cd5c88dbd5c3fabf5e1705e459347131f114bc6")

    # don't support full variant for newer versions (for now) because dependencies get out of hand
    variant("full", default=False, when="@:0.23", description="Enable full functionality.")
    variant("hdf5", default=False, when="@1:", description="Enable hdf5 functionality.")

    depends_on("python@3.9:", when="@1.7:", type=("build", "run"))
    depends_on("python@3.8:", when="@1.4:", type=("build", "run"))
    depends_on("py-hatchling", when="@1.7:", type="build")
    depends_on("py-hatch-vcs", when="@1.7:", type="build")

    # requirements_base.txt with versions specified in README.rst (marked with *)
    depends_on("py-numpy@1.21.2:", when="@1.6.1:", type=("build", "run"))
    depends_on("py-numpy@1.20.2:", when="@1.4:", type=("build", "run"))  # *
    depends_on("py-numpy@1.18.1:", when="@1:", type=("build", "run"))  # *
    depends_on("py-numpy@1.15.4:", when="@0.23:", type=("build", "run"))
    depends_on("py-numpy@1.11.3:", type=("build", "run"))
    depends_on("py-numpy@:1", when="@:1.6", type=("build", "run"))
    depends_on("py-scipy@1.7.1:", when="@1.6.1:", type=("build", "run"))
    depends_on("py-scipy@1.6.3:", when="@1.4:", type=("build", "run"))
    depends_on("py-scipy@1.4.1:", when="@1:", type=("build", "run"))  # *
    depends_on("py-scipy@1.1.0:", when="@0.23:", type=("build", "run"))
    depends_on("py-scipy@0.17.1:", type=("build", "run"))
    depends_on("py-matplotlib@3.5:", when="@1.6.1:", type=("build", "run"))
    depends_on("py-matplotlib@3.4:", when="@1:", type=("build", "run"))  # *
    depends_on("py-matplotlib@3.1:", when="@1:", type=("build", "run"))  # *
    depends_on("py-tqdm", when="@1:", type=("build", "run"))
    depends_on("py-pooch@1.5:", when="@1:", type=("build", "run"))
    depends_on("py-decorator", when="@1:", type=("build", "run"))
    depends_on("py-packaging", when="@1:", type=("build", "run"))
    depends_on("py-jinja2", when="@1:", type=("build", "run"))
    depends_on("py-lazy-loader@0.3:", when="@1.6.1:", type=("build", "run"))

    with when("+hdf5"):
        depends_on("py-h5io", type=("build", "run"))
        depends_on("py-pymatreader", type=("build", "run"))

    # Historical dependencies
    depends_on("py-setuptools@45:", when="@1.4:1.6", type="build")
    depends_on("py-setuptools", when="@:1.6", type="build")
    depends_on("py-setuptools-scm@6.2:", when="@1.4:1.6", type="build")
    depends_on(
        "py-importlib-resources@5.10.2:", when="@1.4:1.6 ^python@:3.9", type=("build", "run")
    )

    with when("+full"):
        # requirements.txt with versions specified in README.rst (marked with *)
        depends_on("py-matplotlib@3.0.3:", type=("build", "run"))  # *
        depends_on("py-pyqt5@5.10:,:5.15.1,5.15.4:", when="platform=linux", type=("build", "run"))
        depends_on("py-pyqt5@5.10:,:5.13", when="platform=darwin", type=("build", "run"))
        depends_on("py-pyqt5@5.10:,:5.15.2,5.15.4:", when="platform=win32", type=("build", "run"))
        depends_on("py-pyqt5-sip", type=("build", "run"))
        depends_on("py-sip", type=("build", "run"))
        depends_on("py-scikit-learn@0.20.2:", type=("build", "run"))  # *
        depends_on("py-nibabel@2.1.0:", type=("build", "run"))  # *
        depends_on("py-numba@0.40:", type=("build", "run"))  # *
        depends_on("py-h5py", type=("build", "run"))
        depends_on("py-pandas@0.23.4:", type=("build", "run"))  # *
        depends_on("py-numexpr", type=("build", "run"))
        depends_on("py-jupyter", type=("build", "run"))
        depends_on("py-python-picard@0.3:", type=("build", "run"))  # *
        depends_on("py-statsmodels", type=("build", "run"))
        depends_on("py-joblib", type=("build", "run"))
        depends_on("py-psutil", type=("build", "run"))
        depends_on("py-dipy@0.10.1:", type=("build", "run"))  # *
        depends_on("vtk+python", type=("build", "run"))
        depends_on("vtk+python@:8.1", when="platform=darwim", type=("build", "run"))
        depends_on("py-mayavi", type=("build", "run"))
        depends_on("py-pysurfer+save_movie", type=("build", "run"))
        depends_on("py-nilearn", type=("build", "run"))
        depends_on("py-xlrd", type=("build", "run"))
        depends_on("py-imageio@2.6.1:", type=("build", "run"))  # *
        depends_on("py-imageio-ffmpeg@0.4.1:", type=("build", "run"))
        depends_on("py-pyvista@0.24:", type=("build", "run"))  # *
        depends_on("py-pyvistaqt@0.2.0:", type=("build", "run"))  # *
        depends_on("py-tqdm", type=("build", "run"))
        depends_on("py-mffpy@0.5.7:", type=("build", "run"))  # *
        depends_on("py-ipywidgets", type=("build", "run"))
        depends_on("py-ipyvtk-simple", type=("build", "run"))

        # README.rst
        # depends_on('py-cupy@4.0:', type=('build', 'run'))  # not yet in spack
