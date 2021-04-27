# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RFf(RPackage):
    """Memory-Efficient Storage of Large Data on Disk and Fast Access Functions

    The ff package provides data structures that are stored on disk but behave
    (almost) as if they were in RAM by transparently  mapping only a section
    (pagesize) in main memory - the effective  virtual memory consumption per
    ff object. ff supports R's standard  atomic data types 'double', 'logical',
    'raw' and 'integer' and  non-standard atomic types boolean (1 bit), quad (2
    bit unsigned),  nibble (4 bit unsigned), byte (1 byte signed with NAs),
    ubyte (1 byte  unsigned), short (2 byte signed with NAs), ushort (2 byte
    unsigned),  single (4 byte float with NAs). For example 'quad' allows
    efficient  storage of genomic data as an 'A','T','G','C' factor. The
    unsigned  types support 'circular' arithmetic. There is also support for
    close-to-atomic types 'factor', 'ordered', 'POSIXct', 'Date' and  custom
    close-to-atomic types.  ff not only has native C-support for vectors,
    matrices and arrays  with flexible dimorder (major column-order, major
    row-order and  generalizations for arrays). There is also a ffdf class not
    unlike  data.frames and import/export filters for csv files. ff objects
    store raw data in binary flat files in native encoding, and complement this
    with metadata stored in R as physical and virtual attributes. ff objects
    have well-defined hybrid copying semantics,  which gives rise to certain
    performance improvements through  virtualization. ff objects can be stored
    and reopened across R  sessions. ff files can be shared by multiple ff R
    objects  (using different data en/de-coding schemes) in the same process
    or from multiple R processes to exploit parallelism. A wide choice of
    finalizer options allows to work with 'permanent' files as well as
    creating/removing 'temporary' ff files completely transparent to the  user.
    On certain OS/Filesystem combinations, creating the ff files works without
    notable delay thanks to using sparse file allocation. Several access
    optimization techniques such as Hybrid Index  Preprocessing and
    Virtualization are implemented to achieve good  performance even with large
    datasets, for example virtual matrix  transpose without touching a single
    byte on disk. Further, to reduce  disk I/O, 'logicals' and non-standard
    data types get stored native and  compact on binary flat files i.e.
    logicals take up exactly 2 bits to  represent TRUE, FALSE and NA.  Beyond
    basic access functions, the ff package also provides  compatibility
    functions that facilitate writing code for ff and ram  objects and support
    for batch processing on ff objects (e.g. as.ram,  as.ff, ffapply). ff
    interfaces closely with functionality from package  'bit': chunked looping,
    fast bit operations and coercions between  different objects that can store
    subscript information ('bit',  'bitwhich', ff 'boolean', ri range index, hi
    hybrid index). This allows to work interactively with selections of large
    datasets and quickly  modify selection criteria.  Further high-performance
    enhancements can be made available upon request.x """

    homepage = "http://ff.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/ff_2.2-13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ff"

    version('4.0.4', sha256='22ecf1811263f27c9fd9f7e13e77f97dcbc0b8ae6f59b76dbaed77569c13d2e5')
    version('2.2-14', sha256='1c6307847275b1b8ad9e2ffdce3f4df3c9d955dc2e8a45e3fd7bfd2b0926e2f0')
    version('2.2-13', sha256='8bfb08afe0651ef3c23aaad49208146d5f929af5af12a25262fe7743fa346ddb')

    depends_on('r@2.10.1:', type=('build', 'run'))
    depends_on('r-bit@1.1-13:', type=('build', 'run'))
    depends_on('r-bit@4.0.0:', when='@4.0.4:', type=('build', 'run'))

    patch('utk_platform_macros.hpp.patch', when='target=aarch64:')
