.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _rpackage:

--
R
--

Like Python, R has its own built-in build system.

The R build system is remarkably uniform and well-tested.
This makes it one of the easiest build systems to create
new Spack packages for.

^^^^^^
Phases
^^^^^^

The ``RBuilder`` and ``RPackage`` base classes have a single phase:

#. ``install`` - install the package

By default, this phase runs the following command:

.. code-block:: console

   $ R CMD INSTALL --library=/path/to/installation/prefix/rlib/R/library .


^^^^^^^^^^^^^^^^^^
Finding R packages
^^^^^^^^^^^^^^^^^^

The vast majority of R packages are hosted on CRAN - The Comprehensive
R Archive Network. If you are looking for a particular R package, search
for "CRAN <package-name>" and you should quickly find what you want.
If it isn't on CRAN, try Bioconductor, another common R repository.

For the purposes of this tutorial, we will be walking through
`r-caret <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/r-caret/package.py>`_
as an example. If you search for "CRAN caret", you will quickly find what
you are looking for at https://cran.r-project.org/package=caret.
https://cran.r-project.org is the main CRAN website. However, CRAN also
has a https://cloud.r-project.org site that automatically redirects to
`mirrors around the world <https://cloud.r-project.org/mirrors.html>`_.
For stability and performance reasons, we will use https://cloud.r-project.org/package=caret.
If you search for "Package source", you will find the download URL for
the latest release. Use this URL with ``spack create`` to create a new
package.

^^^^^^^^^^^^
Package name
^^^^^^^^^^^^

The first thing you'll notice is that Spack prepends ``r-`` to the front
of the package name. This is how Spack separates R package extensions
from the rest of the packages in Spack. Without this, we would end up
with package name collisions more frequently than we would like. For
instance, there are already packages for both:

* ``ape`` and ``r-ape``
* ``curl`` and ``r-curl``
* ``gmp`` and ``r-gmp``
* ``jpeg`` and ``r-jpeg``
* ``openssl`` and ``r-openssl``
* ``uuid`` and ``r-uuid``
* ``xts`` and ``r-xts``

Many popular programs written in C/C++ are later ported to R as a
separate project.

^^^^^^^^^^^
Description
^^^^^^^^^^^

The first thing you'll need to add to your new package is a description.
The top of the homepage for ``caret`` lists the following description:

   Classification and Regression Training

   Misc functions for training and plotting classification and regression models.

The first line is a short description (title) and the second line is a long
description. In this case the description is only one line but often the
description is several lines. Spack makes use of both short and long
descriptions and convention is to use both when creating an R  package.

^^^^^^^^
Homepage
^^^^^^^^

If you look at the bottom of the page, you'll see:

   Linking:

   Please use the canonical form https://CRAN.R-project.org/package=caret to link to this page.

Please uphold the wishes of the CRAN admins and use
https://cloud.r-project.org/package=caret as the homepage instead of
https://cloud.r-project.org/web/packages/caret/index.html. The latter may
change without notice.

^^^
URL
^^^

As previously mentioned, the download URL for the latest release can be
found by searching "Package source" on the homepage.

^^^^^^^^
List URL
^^^^^^^^

CRAN maintains a single webpage containing the latest release of every
single package: https://cloud.r-project.org/src/contrib/

Of course, as soon as a new release comes out, the version you were using
in your package is no longer available at that URL. It is moved to an
archive directory. If you search for "Old sources", you will find:
https://cloud.r-project.org/src/contrib/Archive/caret

If you only specify the URL for the latest release, your package will
no longer be able to fetch that version as soon as a new release comes
out. To get around this, add the archive directory as a ``list_url``.

^^^^^^^^^^^^^^^^^^^^^
Bioconductor packages
^^^^^^^^^^^^^^^^^^^^^

Bioconductor packages are set up in a similar way to CRAN packages, but there
are some very important distinctions. Bioconductor packages can be found at:
https://bioconductor.org/. Bioconductor packages are R packages and so follow
the same packaging scheme as CRAN packages. What is different is that
Bioconductor itself is versioned and released. This scheme, using the
Bioconductor package installer, allows further specification of the minimum
version of R as well as further restrictions on the dependencies between
packages than what is possible with the native R packaging system. Spack can
not replicate these extra features and thus Bioconductor packages in Spack need
to be managed as a group during updates in order to maintain package
consistency with Bioconductor itself.

Another key difference is that, while previous versions of packages are
available, they are not available from a site that can be programmatically set,
thus a ``list_url`` attribute can not be used. However, each package is also
available in a git repository, with branches corresponding to each Bioconductor
release. Thus, it is always possible to retrieve the version of any package
corresponding to a Bioconductor release simply by fetching the branch that
corresponds to the Bioconductor release of the package repository. For this
reason, spack Bioconductor R packages use the git repository, with the commit
of the respective branch used in the ``version()`` attribute of the package.

^^^^^^^^^^^^^^^^^^^^^^^^
cran and bioc attributes
^^^^^^^^^^^^^^^^^^^^^^^^

Much like the ``pypi`` attribute for python packages, due to the fact that R
packages are obtained from specific repositories, it is possible to set up shortcut
attributes that can be used to set ``homepage``, ``url``, ``list_url``, and
``git``. For example, the following ``cran`` attribute:

.. code-block:: python

   cran = "caret"

is equivalent to:

.. code-block:: python

   homepage = "https://cloud.r-project.org/package=caret"
   url      = "https://cloud.r-project.org/src/contrib/caret_6.0-86.tar.gz"
   list_url = "https://cloud.r-project.org/src/contrib/Archive/caret"

Likewise, the following ``bioc`` attribute:

.. code-block:: python

   bioc = "BiocVersion"

is equivalent to:

.. code-block:: python

   homepage = "https://bioconductor.org/packages/BiocVersion/"
   git      = "https://git.bioconductor.org/packages/BiocVersion"


^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

As an extension of the R ecosystem, your package will obviously depend
on R to build and run. Normally, we would use ``depends_on`` to express
this, but for R packages, we use ``extends``. This implies a special
dependency on R, which is used to set environment variables such as
``R_LIBS`` uniformly. Since every R package needs this, the ``RPackage``
base class contains:

.. code-block:: python

   extends("r")


Take a close look at the homepage for ``caret``. If you look at the
"Depends" section, you'll notice that ``caret`` depends on "R (≥ 3.2.0)".
You should add this to your package like so:

.. code-block:: python

   depends_on("r@3.2.0:", type=("build", "run"))


^^^^^^^^^^^^^^
R dependencies
^^^^^^^^^^^^^^

R packages are often small and follow the classic Unix philosophy
of doing one thing well. They are modular and usually depend on
several other packages. You may find a single package with over a
hundred dependencies. Luckily, R packages are well-documented
and list all of their dependencies in the following sections:

* Depends
* Imports
* LinkingTo

As far as Spack is concerned, all 3 of these dependency types
correspond to ``type=("build", "run")``, so you don't have to worry
about the details. If you are curious what they mean,
https://github.com/spack/spack/issues/2951 has a pretty good summary:

   ``Depends`` is required and will cause those R packages to be *attached*,
   that is, their APIs are exposed to the user. ``Imports`` *loads* packages
   so that *the package* importing these packages can access their APIs,
   while *not* being exposed to the user. When a user calls ``library(foo)``
   s/he *attaches* package ``foo`` and all of the packages under ``Depends``.
   Any function in one of these package can be called directly as ``bar()``.
   If there are conflicts, user can also specify ``pkgA::bar()`` and
   ``pkgB::bar()`` to distinguish between them. Historically, there was only
   ``Depends`` and ``Suggests``, hence the confusing names. Today, maybe
   ``Depends`` would have been named ``Attaches``.

   The ``LinkingTo`` is not perfect and there was recently an extensive
   discussion about API/ABI among other things on the R-devel mailing
   list among very skilled R developers:

   * https://stat.ethz.ch/pipermail/r-devel/2016-December/073505.html
   * https://stat.ethz.ch/pipermail/r-devel/2017-January/073647.html

Some packages also have a fourth section:

* Suggests

These are optional, rarely-used dependencies that a user might find
useful. You should **NOT** add these dependencies to your package.
R packages already have enough dependencies as it is, and adding
optional dependencies can really slow down the concretization
process. They can also introduce circular dependencies.

A fifth rarely used section is:

* Enhances

This means that the package can be used as an optional dependency
for another package. Again, these packages should **NOT** be listed
as dependencies.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Core, recommended, and non-core packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you look at "Depends", "Imports", and "LinkingTo", you will notice
3 different types of packages:

"""""""""""""
Core packages
"""""""""""""

If you look at the ``caret`` homepage, you'll notice a few dependencies
that don't have a link to the package, like ``methods``, ``stats``, and
``utils``. These packages are part of the core R distribution and are
tied to the R version installed. You can basically consider these to be
"R itself". These are so essential to R that it would not make sense for
them to be updated via CRAN. If you did, you would basically get a different
version of R. Thus, they're updated when R is updated.

You can find a list of these core libraries at:
https://github.com/wch/r-source/tree/trunk/src/library

""""""""""""""""""""
Recommended packages
""""""""""""""""""""

When you install R, there is an option called ``--with-recommended-packages``.
This flag causes the R installation to include a few "Recommended" packages
(legacy term). They are for historical reasons quite tied to the core R
distribution, developed by the R core team or people closely related to it.
The R core distribution "knows" about these package, but they are indeed
distributed via CRAN. Because they're distributed via CRAN, they can also be
updated between R version releases.

Spack explicitly adds the ``--without-recommended-packages`` flag to prevent
the installation of these packages. Due to the way Spack handles package
activation (symlinking packages to the R installation directory),
pre-existing recommended packages will cause conflicts for already-existing
files. We could either not include these recommended packages in Spack and
require them to be installed through ``--with-recommended-packages``, or
we could not install them with R and let users choose the version of the
package they want to install. We chose the latter.

Since these packages are so commonly distributed with the R system, many
developers may assume these packages exist and fail to list them as
dependencies. Watch out for this.

You can find a list of these recommended packages at:
https://github.com/wch/r-source/blob/trunk/share/make/vars.mk

"""""""""""""""""
Non-core packages
"""""""""""""""""

These are packages that are neither "core" nor "recommended". There are more
than 10,000 of these packages hosted on CRAN alone.

For each of these package types, if you see that a specific version is
required, for example, "lattice (≥ 0.20)", please add this information to
the dependency:

.. code-block:: python

   depends_on("r-lattice@0.20:", type=("build", "run"))


^^^^^^^^^^^^^^^^^^
Non-R dependencies
^^^^^^^^^^^^^^^^^^

Some packages depend on non-R libraries for linking. Check out the
`r-stringi <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/r-stringi/package.py>`_
package for an example: https://cloud.r-project.org/package=stringi.
If you search for the text "SystemRequirements", you will see:

   ICU4C (>= 52, optional)

This is how non-R dependencies are listed. Make sure to add these
dependencies. The default dependency type should suffice.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to the installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some R packages provide additional flags that can be passed to
``R CMD INSTALL``, often to locate non-R dependencies.
`r-rmpi <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/r-rmpi/package.py>`_
is an example of this, and flags for linking to an MPI library. To pass
these to the installation command, you can override ``configure_args``
like so:

.. code-block:: python

   def configure_args(self):
       mpi_name = self.spec["mpi"].name

       # The type of MPI. Supported values are:
       # OPENMPI, LAM, MPICH, MPICH2, or CRAY
       if mpi_name == "openmpi":
           Rmpi_type = "OPENMPI"
       elif mpi_name == "mpich":
           Rmpi_type = "MPICH2"
       else:
           raise InstallError("Unsupported MPI type")

       return [
           "--with-Rmpi-type={0}".format(Rmpi_type),
           "--with-mpi={0}".format(spec["mpi"].prefix),
       ]


There is a similar ``configure_vars`` function that can be overridden
to pass variables to the build.

^^^^^^^^^^^^^^^^^^^^^
Alternatives to Spack
^^^^^^^^^^^^^^^^^^^^^

CRAN hosts over 10,000 R packages, most of which are not in Spack. Many
users may not need the advanced features of Spack, and may prefer to
install R packages the normal way:

.. code-block:: console

   $ R
   > install.packages("ggplot2")


R will search CRAN for the ``ggplot2`` package and install all necessary
dependencies for you. If you want to update all installed R packages to
the latest release, you can use:

.. code-block:: console

   > update.packages(ask = FALSE)


This works great for users who have internet access, but those on an
air-gapped cluster will find it easier to let Spack build a download
mirror and install these packages for you.

Where Spack really shines is its ability to install non-R dependencies
and link to them properly, something the R installation mechanism
cannot handle.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on installing R packages, see:
https://stat.ethz.ch/R-manual/R-devel/library/utils/html/INSTALL.html

For more information on writing R packages, see:
https://cloud.r-project.org/doc/manuals/r-release/R-exts.html

In particular,
https://cloud.r-project.org/doc/manuals/r-release/R-exts.html#Package-Dependencies
has a great explanation of the difference between Depends, Imports,
and LinkingTo.
