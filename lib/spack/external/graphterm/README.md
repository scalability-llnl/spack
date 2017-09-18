graphterm
=========
graphterm provides basic support for interactive drawings of directed acyclic
graphs in ASCII.

Usage
-----
Create a TermDAG object and populate it with nodes and links. Call
`interactve()` to draw in interactive form and `printonly()` to output the ASCII
representation to `stdout`:

```
import graphterm as gt

dag = TermDAG()
dag.add_node('alpha')
dag.add_node('beta')
dag.add_node('gamma')
dag.add_node('delta')
dag.add_node('epsilon')
dag.add_node('zeta')

dag.add_link('alpha', 'beta')
dag.add_link('alpha', 'gamma')
dag.add_link('alpha', 'delta')
dag.add_link('beta', 'epsilon')
dag.add_link('gamma', 'epsilon')
dag.add_link('delta', 'epsilon')
dag.add_link('delta', 'zeta')

dag.printonly()
```

The resulting graph is shown below. As there is not enough room for the label
for `gamma`, it is collected in a list on the right.

```
        o alpha                    
        |                          
       /|\                         
      | | |                        
 beta o o o delta [ gamma ]        
      | | |                        
       \|/|                        
        | |                        
epsilon o o zeta      
```

In interactive mode, nodes can be highlighted by typing a `/` followed by
their name, for example `/gamma` would highlight the name and node for gamma
as well as its connected neighbors. The highlighting can walk through the
nodes from left to right, top to bottom with `n` and `p`. 

For larger graphs, scrolling is accomplished with the arrow keys or `w, a, s,
d`.

To quit the interactive mode, use `q`.


Authors
------- 
graphterm was written by Kate Isaacs.


License
-------
graphterm is released under the LGPL v3 license. For more details, see the
LICENSE file.
