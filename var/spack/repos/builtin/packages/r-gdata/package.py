# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGdata(RPackage):
    """Various R Programming Tools for Data Manipulation.

    Various R programming tools for data manipulation, including:
    [1] medical unit conversions ('ConvertMedUnits', 'MedUnits'),
    [2] combining objects ('bindData', 'cbindX', 'combine', 'interleave'),
    [3] character vector operations ('centerText', 'startsWith', 'trim'),
    [4] factor manipulation ('levels', 'reorder.factor', 'mapLevels'),
    [5] obtaining information about R objects ('object.size', 'elem', 'env',
    'humanReadable', 'is.what', 'll', 'keep', 'ls.funs', 'Args','nPairs',
    'nobs'),
    [6] manipulating MS-Excel formatted files ('read.xls',
    'installXLSXsupport', 'sheetCount', 'xlsFormats'),
    [7] generating fixed-width format files ('write.fwf'),
    [8] extricating components of date & time objects ('getYear', 'getMonth',
    'getDay', 'getHour', 'getMin', 'getSec'),
    [9] operations on columns of data frames ('matchcols', 'rename.vars'),
    [10] matrix operations ('unmatrix', 'upperTriangle', 'lowerTriangle'),
    [11] operations on vectors ('case', 'unknownToNA', 'duplicated2',
    'trimSum'),
    [12] operations on data frames ('frameApply', 'wideByFactor'),
    [13] value of last evaluated expression ('ans'), and
    [14] wrapper for 'sample' that ensures consistent behavior for both scalar
    and vector arguments ('resample')."""

    cran = "gdata"

    license("GPL-2.0-only")

    version("3.0.0", sha256="a456b9921765a705fe8e51780dfbbc6ca005abc948b2f80effeccd468601b17f")
    version("2.18.0.1", sha256="5e2f3d5b9398d52a4c07a4d35f5f936450a44567c7db8d8f68b4cc6946e032d9")
    version("2.18.0", sha256="4b287f59f5bbf5fcbf18db16477852faac4a605b10c5284c46b93fa6e9918d7f")
    version("2.17.0", sha256="8097ec0e4868f6bf746f821cff7842f696e874bb3a84f1b2aa977ecd961c3e4e")

    depends_on("r@2.3.0:", type=("build", "run"))
    depends_on("r-gtools", type=("build", "run"))
    depends_on("perl@5.10.0:")
