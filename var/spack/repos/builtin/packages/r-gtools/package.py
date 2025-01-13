# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGtools(RPackage):
    """Various R Programming Tools.

    Functions to assist in R programming.
    Including:
    [1] assist in developing, updating, and maintaining R and R packages
    ('ask', 'checkRVersion', 'getDependencies', 'keywords', 'scat');
    [2] calculate the logit and inverse logit transformations ('logit',
    'inv.logit');
    [3] test if a value is missing, empty or contains only NA and NULL values
    ('invalid');
    [4] manipulate R's .Last function ('addLast');
    [5] define macros ('defmacro');
    [6] detect odd and even integers ('odd', 'even');
    [7] convert strings containing non-ASCII characters (like single
     quotes) to plain ASCII ('ASCIIfy');
    [8] perform a binary search ('binsearch');
    [9] sort strings containing both numeric and character components
    ('mixedsort');
    [10] create a factor variable from the quantiles of a continuous variable
    ('quantcut');
    [11] enumerate permutations and combinations ('combinations',
    'permutation');
    [12] calculate and convert between fold-change and log-ratio ('foldchange',
    'logratio2foldchange', 'foldchange2logratio');
    [13] calculate probabilities and generate random numbers from Dirichlet
    distributions ('rdirichlet', 'ddirichlet');
    [14] apply a function over adjacent subsets of a vector ('running');
    [15] modify the TCP_NODELAY ('de-Nagle') flag for socket objects;
    [16] efficient 'rbind' of data frames, even if the column names don't match
    ('smartbind');
    [17] generate significance stars from p-values ('stars.pval');
    [18] convert characters to/from ASCII codes;
    """

    cran = "gtools"

    license("GPL-2.0-only")

    version("3.9.5", sha256="dee9b6c1152db1a5dc427d074b32bbbb738708683f17a95e0e95e4d79fdf174b")
    version("3.9.4", sha256="59cf8b194fe98b1cc05dbb4d686810a1068f59d8b402b731548a898ece85f111")
    version("3.9.3", sha256="7afb53277b382d5752f4597ae433f3c0addf5e8eb24d01a9562faf2a01e33133")
    version("3.9.2.1", sha256="ec5febad7bb33812684b39679b0bce8a668361b87714f7388546e0f4ac02af5f")
    version("3.9.2", sha256="03b1898bf581f6d12fa90e23ff700cfa7c834ac10c6654bdac42d7ec943fa953")
    version("3.8.2", sha256="503ba60a41f3c61b8129c25de62c74dab29761d2e661d4addd106e2e02f1dcde")
    version("3.8.1", sha256="051484459bd8ad1b03425b8843d24f6828fea18f7357cfa1c192198cc3f4ba38")
    version("3.5.0", sha256="86b6a51a92ddb3c78095e0c5dc20414c67f6e28f915bf0ee11406adad3e476f6")

    depends_on("r@2.10:", type=("build", "run"))
