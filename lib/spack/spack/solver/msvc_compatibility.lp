% Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% msvc compatibility rules for reusing solves.
%
% These rules are used on Windows w/ MSVC
%=============================================================================

% A package cannot be reused if the msvc is not compatible with it
error(100, "Cannot reuse {0} since we cannot determine msvc compatibility", ReusedPackage)
  :- provider(node(X, MsvcPackage), node(0, "msvc")),
     attr("version", node(X, MsvcPackage), MsvcVersion),
     attr("hash", node(R, ReusedPackage), Hash),
     % msvc packages can be reused without the "compatible_msvc" attribute
     ReusedPackage != MsvcPackage,
     not attr("compatible_msvc", node(R, ReusedPackage), MsvcPackage, MsvcVersion).

% A msvc is needed in the DAG
:- has_built_packages(), not provider(_, node(0, "msvc")).

% Non-msvc reused specs must be host msvc compatible. In case we build packages, we get a
% host compatible msvc provider from other rules. If nothing is built, there is no msvc provider,
% since it's pruned from reusable specs, meaning we have to explicitly impose reused specs are host
% compatible.
:- attr("hash", node(R, ReusedPackage), Hash),
   not provider(node(R, ReusedPackage), node(0, "msvc")),
   not attr("compatible_msvc", node(R, ReusedPackage), _, _).

% The msvc provider must be one that a compiler can target
:- has_built_packages(),
   provider(node(X, MsvcPackage), node(0, "msvc")),
   attr("node", node(X, MsvcPackage)),
   attr("version", node(X, MsvcPackage), msvcVersion),
   not host_msvc(MsvcPackage, msvcVersion).

% A built node must depend on msvc
:- build(PackageNode),
   provider(msvcNode, node(0, "msvc")),
   not external(PackageNode),
   not depends_on(PackageNode, msvcNode).
