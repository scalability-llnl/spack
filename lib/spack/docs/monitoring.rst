.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _monitoring:

==========
Monitoring
==========

You can use a `spack monitor <https://github.com/spack/spack-monitor>`_ "Spackmon"
server to store a database of your packages, builds, and associated metadata 
for provenance, research, or some other kind of development. You should
follow the instructions in the `spack monitor documentation <https://spack-monitor.readthedocs.org>`_
to first create a server along with a username and token for yourself.
You can then use this guide to interact with the server.

-------------------
Analysis Monitoring
-------------------

To read about how to monitor an analysis (meaning you want to send analysis results
to a server) see :ref:`analyze_monitoring`.

---------------------
Monitoring An Install
---------------------

Since an install is typically when you build packages, we logically want
to tell spack to monitor during this step. Let's start with an example
where we want to monitor the install of hdf5. Unless you have disabled authentication
for the server, we first want to export our spack monitor token and username to the environment:

.. code-block:: console
 
    $ export SPACKMON_TOKEN=50445263afd8f67e59bd79bff597836ee6c05438
    $ export SPACKMON_USER=spacky


By default, the host for your server is expected to be at ``http://127.0.0.1``
with a prefix of ``ms1``, and if this is the case, you can simply add the
``--monitor`` flag to the install command:

.. code-block:: console

    $ spack install --monitor hdf5


If you need to customize the host or the prefix, you can do that as well:

.. code-block:: console

    $ spack install --monitor --monitor-prefix monitor --monitor-host https://monitor-service.io hdf5


As a precaution, we cut out early in the spack client if you have not provided
authentication credentials. For example, if you run the command above without
exporting your username or token, you'll see:

.. code-block:: console

    ==> Error: You are required to export SPACKMON_TOKEN and SPACKMON_USER

This extra check is to ensure that we don't start any builds,
and then discover that you forgot to export your token. However, if 
your monitoring server has authentication disabled, you can tell this to
the client to skip this step:

.. code-block:: console

    $ spack install --monitor --monitor-disable-auth hdf5

If the service is not running, you'll cleanly exit early - the install will
not continue if you've asked it to monitor and there is no service.
For example, here is what you'll see if the monitoring service is not running:

.. code-block:: console

    [Errno 111] Connection refused


If you want to continue builds (and stop monitoring) you can set the ``--monitor-keep-going``
flag. 

.. code-block:: console

    $ spack install --monitor --monitor-keep-going hdf5

This could mean that if a request fails, you only have partial or no data
added to your monitoring database. This setting will not be applied to the
first request to check if the server is running, but to subsequent requests.
If you don't have a monitor server running and you want to build, simply
don't provide the ``--monitor`` flag!
