# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPsych(RPackage):
    """Procedures for Psychological, Psychometric, and Personality Research.

    A general purpose toolbox for personality, psychometric theory and
    experimental psychology. Functions are primarily for multivariate analysis
    and scale construction using factor analysis, principal component analysis,
    cluster analysis and reliability analysis, although others provide basic
    descriptive statistics. Item Response Theory is done using factor analysis
    of tetrachoric and polychoric correlations.  Functions for analyzing data
    at multiple levels include within and between group statistics, including
    correlations and factor analysis.  Functions for simulating and testing
    particular item and test structures are included. Several functions serve
    as a useful front end for structural equation modeling. Graphical displays
    of path diagrams, factor analysis and structural equation models are
    created using basic graphics. Some of the functions are written to support
    a book on psychometric theory as well as publications in personality
    research.  For more information, see the <http://personality-project.org/r>
    web page."""

    cran = "psych"

    license("GPL-2.0-or-later")

    version("2.4.6.26", sha256="2d191a95e0107a7f402a17729916099dff201d20c4435f8bf43e6e8a2fbbd2be")
    version("2.3.3", sha256="94a9f3c39f8243573752709b89eb8068e11dbe809f86ecf0225fb429556efb6f")
    version("2.2.9", sha256="4cd518bff387fef95067696b0a0b323310e6f4a063c3d242f2a50bcb17675571")
    version("2.2.5", sha256="dcc3f9b30ed44dfd1de0366295a308e0b52959eb7ac9cb3bc3f32dc5b15fc321")
    version("2.1.9", sha256="1475e03a17f1ae6837834f01c2472aed68887c89d90a84a3e09a532ce218500c")
    version("2.0.12", sha256="8a71d4a1d8bc8c96703f9b4515cfb497e1947c6e017cb08270a7cfb36ce1ad4c")
    version("1.8.12", sha256="6e175e049bc1ee5b79a9e51ccafb22b962b4e6c839ce5c9cfa1ad83967037743")
    version("1.8.10", sha256="e8901ddab14729bfccbd82a8824fbb6523c10c2cd8fb7199b1ca56a7ffcb6e58")
    version("1.7.8", sha256="f328ea602e22b0e7e5f310a8d19f305d8e0a3a86040cdfb64863b68b56d55135")

    depends_on("r-gparotation", type=("build", "run"), when="@2.3.6:")
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-mnormt", type=("build", "run"))
    depends_on("r-nlme", type=("build", "run"))

    depends_on("r-foreign", type=("build", "run"), when="@:1.8.12")
