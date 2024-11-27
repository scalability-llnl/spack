.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _sourceforgepackage:

-----------
Sourceforge
-----------

``SourceforgePackage`` is a
`mixin-class <https://en.wikipedia.org/wiki/Mixin>`_. It automatically
sets the URL based on a list of Sourceforge mirrors listed in
`sourceforge_mirror_path`, which defaults to a half dozen known mirrors.
Refer to the package source
(`<https://github.com/spack/spack/blob/develop/lib/spack/spack/build_systems/sourceforge.py>`__) for the current list of mirrors used by Spack.


^^^^^^^
Methods
^^^^^^^

This package provides a method for populating mirror URLs.

**urls**

    This method returns a list of possible URLs for package source.
    It is decorated with `property` so its results are treated as
    a package attribute.

    Refer to
    `<https://spack.readthedocs.io/en/latest/packaging_guide.html#mirrors-of-the-main-url>`__
    for information on how Spack uses the `urls` attribute during
    fetching.

^^^^^
Usage
^^^^^

This helper package can be added to your package by adding it as a base
class of your package and defining the relative location of an archive
file for one version of your software.

.. code-block:: python
   :emphasize-lines: 1,3

    class MyPackage(AutotoolsPackage, SourceforgePackage):
        ...
        sourceforge_mirror_path = "my-package/mypackage.1.0.0.tar.gz"
        ...

Over 40 packages are using ``SourceforcePackage`` this mix-in as of
July 2022 so there are multiple packages to choose from if you want
to see a real example.
