.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _racketpackage:

------
Racket
------

Much like Python, Racket packages and modules have their own special build system.
To learn more about the specifics of Racket package system, please refer to the
`Racket Docs <https://docs.racket-lang.org/pkg/cmdline.html>`_.

^^^^^^
Phases
^^^^^^

The ``RacketBuilder`` and ``RacketPackage`` base classes provides an ``install`` phase that
can be overridden, corresponding to the use of:

.. code-block:: console

   $ raco pkg install

^^^^^^^
Caveats
^^^^^^^

In principle, ``raco`` supports a second, ``setup`` phase; however, we have not
implemented this separately, as in normal circumstances, ``install`` also handles
running ``setup`` automatically.

Unlike Python, Racket currently on supports two installation scopes for packages, user
or system, and keeps a registry of installed packages at each scope in its configuration files.
This means we can't simply compose a "``RACKET_PATH``" environment variable listing all of the
places packages are installed, and update this at will.

Unfortunately this means that all currently installed packages which extend Racket via ``raco pkg install``
are accessible whenever Racket is accessible.

Additionally, because Spack does not implement uninstall hooks, uninstalling a Spack  ``rkt-`` package
will have no effect on the ``raco`` installed packages visible to your Racket installation.
Instead, you must manually run ``raco pkg remove`` to keep the two package managers in a mutually
consistent state.
