.. Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _cargopackage:

------------
CargoPackage
------------

Cargo is the typical build system for programs written using the `Rust
programming language <https://www.rust-lang.org/>`_. It is able to manage
dependencies, configure optional build features, and build executables and
libraries. Packages that are written in Rust are often referred to as "crates".

The ``CargoPackage`` base class will install any executables, static libraries,
and dynamic libraries in the target Cargo crate. Implementers of
``CargoPackage`` can additionally control which crate features to build by
overriding the ``cargo_features(self)`` method.

^^^^^^^^^^^^^^
Package Layout
^^^^^^^^^^^^^^
By default, ``CargoPackage`` will expect to find the crate's manifest
(``Cargo.toml``) in the root of the package. However, in the atypical case
where the manifest is not at the package root, this can be overridden by using
the ``cargo_manifest('relative/path/to/Cargo.toml')`` directive.

The ``cargo_manifest`` directive can also be used by other packages that use
Rust with a different top-level build system to easily vendor their Cargo
dependencies.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fetching and Building Crates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can specify the method for fetching crates
:ref:`just like any other package <versions-and-fetching>` - Cargo does not
care where the crate came from.

An additional fetch strategy is provided just for Cargo crates - the
``crates_io`` fetch strategy. This allows a package maintainer to import
packages directly from the `official package repoistory <https://crates.io>`_
into a Spack repo. For example, the ``ripgrep`` package can fetch straight from
``crates.io`` for published releases, or can fetch from GitHub for
in-development builds:

.. code-block:: python

   class Ripgrep(CargoPackage):
      """ripgrep is a line-oriented search tool that recursively searches
      your current directory for a regex pattern.  ripgrep is similar to
      other popular search tools like The Silver Searcher, ack and grep.
      """

      homepage = "https://github.com/BurntSushi/ripgrep"

      crates_io = "ripgrep"
      git = "https://github.com/BurntSushi/ripgrep.git"

      # In-Development Releases
      version('master', branch='master')

      # crates.io Releases
      version('12.1.0', sha256='4549a261aa8674d0ffdfe40c68bd282e8913f810bee728fac5441bbfe17aca45')

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Quickly Import Crates from crates.io
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``spack create`` recognizes ``crates.io`` and ``lib.rs`` (an alternative
``crates.io`` frontend) URLs, and can create a rich template for any crate
imported from ``crates.io``. For example:

.. code-block::

   spack create https://crates.io/crates/ripgrep

.. _cargo-dependencies:

^^^^^^^^^^^^
Dependencies
^^^^^^^^^^^^

Because Cargo is already proficient at managing dependencies, Spack delegates
the resolving, fetching, and building of Cargo dependencies to Cargo.
Therefore, Cargo dependencies do not appear as first-class dependencies in
Spack. Essentially, each Cargo crate has separate compilation `for the
Rust dependencies`, and all of those dependencies are linked statically.

Rust projects typically ship a ``Cargo.lock`` file that specifies checksums
for each Cargo dependency, meaning Spack can rely on cargo to verify each
dependency. Cargo will therefore fetch these dependencies, when not already
cached or mirrored, from a package repository or from source control. It's
important to emphasize that Spack implements proper caching and mirroring of
Cargo dependencies so you can build Cargo packages on reduced-connectivity or
air-gapped systems. Users will have to tell Rust to ignore checksums for any
``CargoPackage`` without a ``Cargo.lock`` file.

Package maintainers are encouraged to still build non-Rust dependencies using
Spack's existing mechanisms. For example, many Rust command line tools use
``libgit2``, and so these packages will specify the ``libgit2`` Spack package
as a dependency. Since the `libgit2 Rust bindings
<https://lib.rs/crates/git2>`_ will attempt to build a
vendored version of ``libgit2`` by default, you must specify an environment
variable to tell Cargo to search for an existing build of ``libgit2``. For
example, see this snippet from the ``exa`` package:

.. code-block:: python

    depends_on('libgit2', when='+git')

    def cargo_features(self):
        if '+git' in self.spec:
            return ['git']
        else:
            return []

    def setup_build_environment(self, env):
        if '+git' in self.spec:
            env.append_flags('LIBGIT2_SYS_USE_PKG_CONFIG', '1')

Note that there is no standard method in Rust for telling Cargo to search for
native dependencies, so you have to determine the correct approach on a
package-by-package basis.

^^^^^^^^
Features
^^^^^^^^

Just like Spack, Cargo crates can offer optional features. Unlike Spack
variants, Cargo features are purely boolean switches. Cargo crates have a set
of default features that can be disabled, but they cannot be disabled on a
feature-by-feature basis. Instead, you must disable `all` default features, and
then opt back into those feature which you want to build with one-by-one.

By default, ``CargoPackage`` will build with the default features in the crate.
This behavior can be overrided by implementing ``cargo_features(self)``. This
method must return either an array of feature names to build, in which case the
default Cargo features will NOT be built, unless individually specified, or
return ``None`` to build all of the default features in the crate.

An example of implementing `cargo_features` can be seen in the
:ref:`cargo-dependencies` section.

^^^^^^^^^^^^^^^^
Default Variants
^^^^^^^^^^^^^^^^

.. code-block:: python

    variant('build_type',
            default='release',
            description='Cargo build type',
            values=('debug', 'release'))

``build_type`` controls whether the Cargo crate is built with the ``--release``
flag. It is recommended to not override this variant.

.. code-block:: python

    variant(
        'prefer_dynamic',
        default=True,
        description='Link Rust standard library dynamically'
    )

``prefer_dynamic`` controls whether the Rust standard library is linked
dynamically vs. statically. This variant is set by default so as to conform
with the Spack preference for dynamic libraries. ``+prefer_dynamic`` is not
compatible with the ``panic = "abort"`` option that some crates set, and so a
package that uses ``panic = "abort"`` should override ``prefer_dynamic``'s
default to ``False``.

``CargoPackage`` does not currently provide a way to change a crate's ``abort``
setting as it could have potential safety implications - the crate might rely
on ``panic = "abort"`` to enforce some of Rust's safety guarantees.

.. code-block:: python

    variant(
        'lto',
        default='none',
        description='Link binaries with link-time optimization',
        values=('none', 'thin', 'fat')
    )

``lto`` controls whether the crate should be linked using link-time
optimization. This is set to ``none`` by default since it conflicts with
``prefer_dynamic``. ``thin`` and ``fat`` are different flavors of LTO that can
be applied.
