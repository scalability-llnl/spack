# This file implements graphterm, an interactive, ASCII representation for
# directed acyclic graphs.
#
# To Use:
#   1. Create a TermDAG object and populate with node and link information
#      using the add_node(name) and add_link(source_name, sink_name) methods.
#   2. Call interactive() for an interactive curses screen with the DAG,
#      or Call printonly() to print the layout to screen with the top node
#      highlighted.
#
# Dependencies
# * The interactivity is managed through the curses library.
# * The ASCII layout modifies a graphical layout (TermLayout) translated from 
#   the Tulip graph drawing library: http://tulip.labri.fr/
#
# File: Kate Isaacs
# License: LGPL v.3

from __future__ import print_function
import heapq
from heapq import *
import curses
import curses.ascii
import math

class TermDAG(object):
    """Class to store DAG layout and manage interactions.

       This class stores its own copy of the graph.
    """

    def __init__(self, logfile = None, question = None):
        """Constructor. Nodes and links should be added after construction
           using the add_node and add_link methods.

           @param logifle: filename/path to store interaction log
           @param question: question text that should be displayed above graph
        """
        # Display question, keep logs for studies
        self.logfile = logfile
        if logfile:
            self.logfile = open(logfile, 'a')
        self.question = question

        # Graph and layout
        self._nodes = dict()
        self._nodes_list = list()
        self._links = list()
        self._positions_set = False
        self.gridsize = [0,0]
        self.gridedge = [] # the last char per row
        self.grid = []
        self.grid_colors = []
        self.row_max = 0
        self.row_names = dict()
        self.left_offset = 0
        self.right_offset = 0

        self.TL = None
        self.placers = set()

        # Interactive behavior
        self.highlight_full_connectivity = False

        self.layout = False # Is layout valid?

        # Pad containing layout
        self.pad = None
        self.pad_pos_x = 0
        self.pad_pos_y = 0
        self.pad_extent_x = 0
        self.pad_extent_y = 0
        self.pad_corner_x = 0
        self.pad_corner_y = 0
        self.height = 0
        self.width = 0
        self.offset = 0

        # Color defaults
        self.maxcolor = 7
        self.default_color = 0 # whatever is the true default
        self.select_color = 2 # red
        self.neighbor_color = 2 # red

        self.initialize_help()

        self.qpad = None
        if self.question:
            self.initialize_question()


    def reset(self):
        """Resets the layout data structures for re-running the layout.

           This can be used in multi-layout comparison.
        """
        self._positions_set = False
        self.gridsize = [0,0]
        self.gridedge = [] # the last char per row
        self.grid = []
        self.grid_colors = []
        self.row_max = 0
        self.row_names = dict()
        self.placers = set()
        self.left_offset = 0
        self.right_offset = 0

        # Delete extra layout nodes
        toDelete = list()
        for node in self._nodes.values():
            if not node.real:
                toDelete.append(node)
            else:
                node.reset()

        for node in toDelete:
            del self._nodes[node.name]
            del node

        for link in self._links:
            link.reset()

        self.qpad = None
        if self.question:
            self.initialize_question()


    def log_character(self, ch):
        """Write a character to the interaction log.

           @param ch: character to write
        """
        if isinstance(ch, unicode):
            self.logfile.write(str(ch).decode('utf-8').encode('utf-8'))
        elif isinstance(ch, int) and ch < 128:
            self.logfile.write(str(unichr(ch)))
        elif isinstance(ch, int):
            self.logfile.write(str(ch).decode('utf-8').encode('utf-8'))


    def initialize_question(self):
        """Initialize the pad that displays the question."""
        self.qpad_pos_x = 0
        self.qpad_pos_y = 0
        self.qpad_extent_x = len(self.question)
        self.qpad_extent_y = 1
        self.qpad_corner_x = 0
        self.qpad_corner_y = 0
        self.qpad_max_x = self.qpad_extent_x + 1
        self.qpad_max_y = 2


    def initialize_help(self):
        """Initializes the help menu, both the pad and the items."""
        self.hpad = None # Help Pad
        self.hpad_default_cmds = []
        self.hpad_default_cmds.append('h')
        self.hpad_default_cmds.append('q')
        self.hpad_default_msgs = []
        self.hpad_default_msgs.append('toggle help')
        self.hpad_default_msgs.append('quit')
        self.hpad_pos_x = 0
        self.hpad_pos_y = 0
        self.hpad_extent_x = len(self.hpad_default_cmds[0]) + len(self.hpad_default_msgs[0]) + 5
        self.hpad_extent_y = 3
        self.hpad_corner_x = 0
        self.hpad_corner_y = 0
        self.hpad_collapsed = False

        self.hpad_cmds = []
        self.hpad_msgs = []
        self.hpad_cmds.extend(self.hpad_default_cmds)
        self.hpad_cmds.append('/foo')
        self.hpad_cmds.append('ctrl-v')
        self.hpad_cmds.append('')
        self.hpad_cmds.append('n')
        self.hpad_cmds.append('p')
        self.hpad_cmds.append('w,a,s,d')
        self.hpad_cmds.append('arrow keys')
        self.hpad_msgs.extend(self.hpad_default_msgs)
        self.hpad_msgs.append('highlight node "foo"')
        self.hpad_msgs.append('change highlight mode:')
        self.hpad_msgs.append('  neighbors or reachability')
        self.hpad_msgs.append('advance highlighted node')
        self.hpad_msgs.append('move back highlighted node')
        self.hpad_msgs.append('scroll up, left, down, right')
        self.hpad_msgs.append('scroll directions')

        self.hpad_max_y = len(self.hpad_cmds)
        self.hpad_max_cmd = 0
        self.hpad_max_msg = 0
        for i in range(len(self.hpad_cmds)):
            self.hpad_max_cmd = max(len(self.hpad_cmds[i]), self.hpad_max_cmd)
            self.hpad_max_msg = max(len(self.hpad_msgs[i]), self.hpad_max_msg)
        hpad_collapse_max_cmd = 0
        hpad_collapse_max_msg = 0
        for i in range(len(self.hpad_default_cmds)):
            hpad_collapse_max_cmd = max(len(self.hpad_default_cmds[i]), hpad_collapse_max_cmd)
            hpad_collapse_max_msg = max(len(self.hpad_default_msgs[i]), hpad_collapse_max_msg)

        # The 2 is for the prefix and suffix space
        self.hpad_max_x = self.hpad_max_cmd + self.hpad_max_msg + len(' - ') + 2
        self.hpad_max_collapse_x = hpad_collapse_max_msg + hpad_collapse_max_cmd + len(' - ') + 2


    def add_node(self, name):
        """Add a node to the internal graph.

           @param name: name of node to add.
        """
        node = TermNode(name)
        self._nodes[name] = node
        self._nodes_list.append(name)
        self.layout = False


    def add_link(self, source, sink):
        """Add a link to the internal graph.

           @param source: name of source node to add
           @param sink: name of sink node to add
        """
        link = TermLink(len(self._links), source, sink)
        self._links.append(link)
        self._nodes[source].add_out_link(link)
        self._nodes[sink].add_in_link(link)
        self.layout = False


    def interactive(self):
        """Layout the graph and show interactively via curses."""
        self.layout_hierarchical()
        curses.wrapper(termdag_interactive_helper, self)

        # Persist the depiction with stdout:
        self.print_grid(True)


    def printonly(self):
        """Layout the graph and print to stdout. Highlights the first node."""
        self.layout_hierarchical()
        self.grid_colors = []
        for row in range(self.gridsize[0]):
            self.grid_colors.append([self.default_color for x
                in range(self.gridsize[1])])

        import sys
        if sys.stdout.isatty():
            selected = self.node_order[0].name
            self.select_node(None, selected, self.offset)

            for i in range(self.gridsize[0]):
                print(self.print_color_row(i, 0, self.gridsize[1] + 1))
        else:
            for row in self.grid:
                print(''.join(row))


    def report(self):
        """Report on the success of the layout algorithm."""
        return self.layout_hierarchical()


    def layout_hierarchical(self):
        """Layout the graph into an ASCII Grid."""

        # Run graphical space layout
        self.TL = TermLayout(self)
        self.TL.layout()

        # Data structures
        xset = set() # set of seen x coords
        yset = set() # set of seen y coords
        node_yset = set() # set of y coords pertaining to nodes
        segments = set() # set of seen segments
        segment_lookup = dict()
        self.segment_ids = dict()
        coord_to_node = dict() # lookup a node from its coord
        coord_to_placer = dict() # lookup a placer node from its coord

        # Convert graphical layout to something we can manipulate for 
        # both nodes and links.

        # Find set of all node coordinates from graphical layout.
        # Also keep track of coordinate extents
        maxy = -1e9
        self.min_tulip_x = 1e9
        self.max_tulip_x = -1e9
        for node in self._nodes.values():
            coord = self.TL._nodes[node.name].coord
            node._x = coord[0]
            node._y = coord[1]
            xset.add(coord[0])
            yset.add(coord[1])
            node_yset.add(coord[1])
            coord_to_node[(coord[0], coord[1])] = node
            if coord[1] > maxy:
                maxy = coord[1]
            self.max_tulip_x = max(self.max_tulip_x, coord[0])
            self.min_tulip_x = min(self.min_tulip_x, coord[0])

        # Convert segments calculated in graphical layout to internal segments
        # and update or seen x and y coords.
        # Create placer nodes as necessary between segments.
        # TODO: Make better use of TL which has already done some of this
        # work.
        # TODO: Factor some of the repeat code.
        segmentID = 0
        for link in self._links:
            link._coords = self.TL._link_dict[link.id].segments
            last = (self._nodes[link.source]._x, self._nodes[link.source]._y)
            for coord in link._coords:
                xset.add(coord[0])
                yset.add(coord[1])
                if (last[0], last[1], coord[0], coord[1]) in segment_lookup:
                    segment = segment_lookup[(last[0], last[1], coord[0], coord[1])]
                else:
                    segment = TermSegment(last[0], last[1], coord[0], coord[1], segmentID)
                    self.segment_ids[segmentID] = segment
                    segmentID += 1
                    segments.add(segment)
                    segment_lookup[(last[0], last[1], coord[0], coord[1])] = segment
                    segment.paths.add((link.source, link.sink))
                link.segments.append(segment)
                segment.links.append(link)
                segment.start = coord_to_node[last]

                if (coord[0], coord[1]) in coord_to_node:
                    placer = coord_to_node[(coord[0], coord[1])]
                    segment.end = placer
                    segment.original_end = placer
                    placer.add_in_segment(segment)
                else:
                    placer = TermNode("", False)
                    self.placers.add(placer)
                    coord_to_node[(coord[0], coord[1])] = placer
                    coord_to_placer[(coord[0], coord[1])] = placer
                    placer._x = coord[0]
                    placer._y = coord[1]
                    segment.end = placer
                    segment.original_end = placer
                    placer.add_in_segment(segment)

                last = (coord[0], coord[1])

            if (last[0], last[1], self._nodes[link.sink]._x, self._nodes[link.sink]._y) in segment_lookup:
                segment = segment_lookup[(last[0], last[1], self._nodes[link.sink]._x, self._nodes[link.sink]._y)]
            else:
                segment = TermSegment(last[0], last[1], self._nodes[link.sink]._x,
                    self._nodes[link.sink]._y, segmentID)
                self.segment_ids[segmentID] = segment
                segment.paths.add((link.source, link.sink))
                segmentID += 1
                segments.add(segment)
                segment_lookup[(last[0], last[1], self._nodes[link.sink]._x, self._nodes[link.sink]._y)] = segment
            link.segments.append(segment)
            segment.links.append(link)
            placer = coord_to_node[last]
            segment.start = placer
            segment.end = self._nodes[link.sink]
            segment.original_end = self._nodes[link.sink]


        # Find crossings between segments in graphical layout.
        self.find_crossings(segments)

        # Consolidate crossing points so that fewer segment crossings will
        # have to be dealt with. This keeps track of the x and y values of
        # the crossings.
        crossings_points = dict() # (x, y) -> set of segments
        for k, v in self.crossings.items(): # crossings is (seg1, seg2) -> (x, y)
            if v not in crossings_points:
                crossings_points[v] = set()
            crossings_points[v].add(k[0])
            crossings_points[v].add(k[1])
            self.segment_ids[k[0]].addCrossing(self.segment_ids[k[1]], v)
            self.segment_ids[k[1]].addCrossing(self.segment_ids[k[0]], v)

        # Based on the set of all crossings coming into a placer node,
        # calculate appropriate crossing heights.
        for placer in self.placers:
            placer.findCrossingHeights(self.min_tulip_x, self.max_tulip_x)

        # For each crossing, figure out if the end point of either already has
        # a set of height for that y value. Cases:
        #     Neither has one: proceed as normal
        #     One has one: shift the crossing to that y value
        #     More than one has them: Ignore for now
        for v, k in crossings_points.items():
            x, y = v
            special_heights = list()
            for name in k:
                segment = self.segment_ids[name]
                if segment.y1 in segment.origin.original_end.crossing_heights:
                    special_heights.append(segment.origin.original_end.crossing_heights[segment.y1])


            # Determine where to bundle depending on special heights.
            placer_y = y
            bundle = False
            if len(special_heights) == 1:
                placer_y = special_heights[0]
                bundle = True
            elif len(special_heights) > 1:
                continue

            # Get placer
            if (x,placer_y) in coord_to_node:
                placer = coord_to_node[(x,placer_y)]
            else:
                placer = TermNode('', False)
                placer._x = x
                placer._y = placer_y
                coord_to_node[(x,placer_y)] = placer
                coord_to_placer[(x,placer_y)] = placer

            # Create segment break
            for name in k:
                segment = self.segment_ids[name]
                new_segment = segment.split(placer, bundle)
                segments.add(new_segment)
            xset.add(x)
            yset.add(placer_y)


        # Convert found x and y coords in graphical layout to positions in
        # the ASCII grid.
        xsort = sorted(list(xset))
        ysort = sorted(list(yset))
        ysort.reverse()
        segment_pos = dict() # Lookup of graphical y position to ASCII y position
        column_multiplier = 2
        row_multiplier = 2
        self.gridsize = [len(ysort) - len(node_yset) + len(node_yset) * row_multiplier,
            len(xsort) * column_multiplier]
        y = 0
        for ypos in ysort:
            segment_pos[ypos] = y
            if ypos in node_yset:
                y += 1
            y += 1

        # Setup lookups from x-coord to col and y-coord to row
        row_lookup = dict()
        col_lookup = dict()
        row_nodes = dict()
        for i, x in enumerate(xsort):
            col_lookup[x] = i
        for i, y in enumerate(ysort):
            row_lookup[y] = i

        # Figure out how nodes map to rows so we can figure out label
        # placement allowances
        self.row_last = [0 for x in range(self.gridsize[0])]
        self.row_last_mark = [0 for x in range(self.gridsize[0])]
        self.row_first = [self.gridsize[1] for x in range(self.gridsize[0])]
        self.row_first_mark = [self.gridsize[1] for x in range(self.gridsize[0])]
        for coord, node in coord_to_node.items():
            node._row = segment_pos[coord[1]]
            node._col = column_multiplier * col_lookup[coord[0]]
            if node.real:
                if node._row not in row_nodes:
                    row_nodes[node._row] = []
                row_nodes[node._row].append(node)
                if node._col > self.row_last[node._row]:
                    self.row_last[node._row] = node._col
                    self.row_last_mark[node._row] = node._col
                if node._col < self.row_first[node._row]:
                    self.row_first[node._row] = node._col
                    self.row_first_mark[node._row] = node._col

        # Sort the labels by left-right position
        for row, nodes in row_nodes.items():
            row_nodes[row] = sorted(nodes, key = lambda node: node._col)

        # Find the node order per row.
        self.node_order = sorted(self._nodes.values(),
            key = lambda node: node._row * 1e6 + node._col)
        for i, node in enumerate(self.node_order):
            node.order = i

        # Create the grid
        self.grid = []
        for i in range(self.gridsize[0]):
            self.grid.append([' ' for j in range(self.gridsize[1])])
            self.gridedge.append(0)

        # Add the nodes in the grid
        for coord, node in coord_to_node.items():
            node._row = segment_pos[coord[1]]
            node._col = column_multiplier * col_lookup[coord[0]]
            if node.real:
                self.grid[node._row][self.left_offset + node._col] = 'o'


        # Sort segments on drawing difficulty. This is used in the collision
        # policy to determine which character to draw.
        segments = sorted(segments, key = lambda x: x.for_segment_sort())

        # Add segments to the grid. Status meaning:
        #     passed: Drawn with only |, /, \, _
        #     failed: Failed to draw for some reason
        #     drawing: Drawing uses X
        status = 'passed'
        for segment in segments:
            segment.gridlist =  self.draw_line(segment)
            err = self.set_to_grid(segment) #, self.row_last)
            if not err:
                status = 'drawing'

        # Determine max grid size with labels and reset grid.
        self.grid = []
        self.gridedge = []
        self.grid_colors = []
        self.calculate_max_labels(row_nodes)

        # Max number of columns needed -- we add one for a space
        # between the graph and the labels.
        self.gridsize[1] = self.row_max + 1

        # Re-create the grid for labels
        for i in range(self.gridsize[0]):
            self.grid.append([' ' for j in range(self.gridsize[1])])
            self.gridedge.append(0)

        # Re-Add the nodes in the grid
        for coord, node in coord_to_node.items():
            node._row = segment_pos[coord[1]]
            node._col = column_multiplier * col_lookup[coord[0]]
            if node.real:
                self.grid[node._row][self.left_offset + node._col] = 'o'

        # Re-Add segments to the grid
        status = 'passed'
        for segment in segments:
            segment.gridlist =  self.draw_line(segment)
            err = self.set_to_grid(segment) #, self.row_last)
            if not err:
                status = 'drawing'

        # Add labels to the grid
        self.place_labels(row_nodes)

        self.layout = True
        return status


    def place_label_left(self, node):
        """Attempt to place a label to the left of the node on the grid.

           @param node: node with label to place.
           @return True if successful, False if there is a collision.
        """
        y = node._row
        x = self.left_offset + node._col - 2 # start one space before node
        characters = len(node.name) + 1 # include space before node
        while characters > 0:
            if self.grid[y][x] != '' and self.grid[y][x] != ' ':
                return False
            x -= 1
            characters -= 1

        x = self.left_offset + node._col - 1 - len(node.name)
        node.label_pos = x
        node.use_offset = False
        for ch in node.name:
            self.grid[y][x] = ch
            x += 1
        return True


    def place_label_right(self, node):
        """Attempt to place a label to the right of the node on the grid.

           @param: node: node with label to place.
           @return True if successful, False if there is a collision.
        """
        y = node._row
        x = self.left_offset + node._col + 2 # start one space after node
        characters = len(node.name) + 1 # include space after node
        while characters > 0:
            if self.grid[y][x] != '' and self.grid[y][x] != ' ':
                return False
            x += 1
            characters -= 1

        x = self.left_offset + node._col + 2
        node.label_pos = x
        node.use_offset = False
        for ch in node.name:
            self.grid[y][x] = ch
            x += 1

        return True


    def place_label_bracket(self, node, left_bracket, right_bracket,
        left_pos, right_pos, left_nodes, half_row):
        """Place a label in the bracketed space. Presently the left_bracket
           is not used.

           @returns left_bracket: string representing the running left_bracket
           @returns right_bracket: string representing the running right_bracket
           @returns left_pos: the offset into the left bracket
           @returns right_pos: the offset into the right bracket
        """

        # First attempt to place the label next to the node.
        if self.place_label_right(node):
            return left_bracket, right_bracket, left_pos, right_pos
        if self.place_label_left(node):
            return left_bracket, right_bracket, left_pos, right_pos

        node.use_offset = True
        # Logic for unused left bracket
        #if node._col < half_row:
        #    if left_bracket == '':
        #        left_bracket = ' [ ' + node.name
        #        node.label_pos = left_pos + 3
        #        left_pos += len(node.name) + 3
        #    else:
        #        left_bracket += ', ' + node.name
        #        node.label_pos = left_pos + 2
        #        left_pos += len(node.name) + 2
        #    left_nodes.append(node)
        #else:
        if right_bracket == '':
            right_bracket = ' [ ' + node.name
            node.label_pos = right_pos + 3
            right_pos += len(node.name) + 3
        else:
            right_bracket += ', ' + node.name
            node.label_pos = right_pos + 2
            right_pos += len(node.name) + 2

        return left_bracket, right_bracket, left_pos, right_pos


    def place_labels(self, row_nodes):
        """Places labels for all nodes in a grid row.

           @param row_nodes: mapping from row to list of nodes on that row
        """
        # Place the labels on the grid
        for row, nodes in row_nodes.items():
            half_row = math.floor(self.row_last_mark[row] / 2) - 1 # subtract for indexing at 0
            left_pos = 0
            right_pos = 0
            left_bracket = ''
            right_bracket = ''
            left_nodes = []
            right_name = ''
            left_name = ''

            # Special case: Last node
            last = nodes[-1]
            if self.place_label_right(last):
                if last._col == self.row_last_mark[row]:
                    right_pos += len(last.name)
                    right_name = last.name
            elif not self.place_label_left(last):
                if right_name == '':
                    last.use_offset = True
                    last.label_pos = right_pos
                    right_pos += len(last.name)
                    right_name = last.name
                else:
                    left_bracket, right_bracket, left_pos, right_pos \
                        = self.place_label_bracket(last, left_bracket, right_bracket,
                            left_pos, right_pos, left_nodes, half_row)

            # Draw the rest 
            if len(nodes) > 1:
                for node in nodes[0:-1]:
                    if not self.place_label_right(node) and not self.place_label_left(node):
                        if right_name == '':
                            node.use_offset = True
                            node.label_pos = right_pos
                            right_pos += len(node.name)
                            right_name = node.name
                        else:
                            left_bracket, right_bracket, left_pos, right_pos \
                                = self.place_label_bracket(node, left_bracket, right_bracket,
                                    left_pos, right_pos, left_nodes, half_row)


            if right_bracket != '':
                right_bracket += ' ]'
                right_pos += 2

            row_left_offset = self.left_offset + self.row_first_mark[row] - left_pos
            #- len(left_name) - len(left_bracket)

            # Absolute positioning of the left bracket labels
            for node in left_nodes:
                node.use_offset = False
                node.label_pos += row_left_offset - len(left_name) - 1


            # Place bracketed elements
            start = self.left_offset + self.row_last_mark[row] + 2 # Space between
            right_names = right_name + right_bracket
            for ch in right_names:
                self.grid[row][start] = ch
                start += 1

            start = row_left_offset
            left_names = left_bracket
            for ch in left_names:
                self.grid[row][start] = ch
                start += 1


    def calculate_max_labels(self, row_nodes):
        """Calculates the maximum amount of space needed to place labels
           for a row of nodes.

           @param row_nodes: mapping from row to list of nodes on that row
        """
        self.row_max = 0

        # For use in two-pracket case
        #half_row = math.floor(self.gridsize[1] / 2) - 1 # subtract for indexing at 0

        bracket_len = len(' [ ') + len(' ]')
        comma_len = len(', ')
        self.left_offset = 0
        self.right_offset = 0
        for row, nodes in row_nodes.items():
            for node in nodes:
                if len(node.name) - node._col >= 0:
                    self.left_offset = max(self.left_offset, 1 + len(node.name) - node._col)

            if len(nodes) == 1:
                self.right_offset = max(self.right_offset, 1 + len(nodes[0].name))
            else:
                # Figure out what bracket sides there are
                right_side = 0
                for node in nodes[:-1]:
                    if right_side == 0:
                        right_side = bracket_len
                    else:
                        right_side += comma_len
                    right_side += len(node.name)

                self.right_offset = max(self.right_offset, 1 + len(nodes[-1].name) + right_side)
        self.row_max = self.gridsize[1] + self.left_offset + self.right_offset


    def set_to_grid(self, segment): #, row_last):
        """Converts calculated link segments into positions on the grid.
           Implements rules for character collisions.

           @param segment: segment to be drawn on ASCII grid.
        """
        success = True
        start = segment.start
        end = segment.end
        last_x = start._col
        last_y = start._row
        for i, coord in enumerate(segment.gridlist):
            x, y, char, draw = coord
            if x > self.row_last_mark[y]:
                self.row_last_mark[y] = x
            if x < self.row_first_mark[y]:
                self.row_first_mark[y] = x
            x += self.left_offset
            if not draw or char == '':
                continue
            if self.grid[y][x] == ' ':
                self.grid[y][x] = char
            elif char != self.grid[y][x]:
                # Precedence:
                #   Slash
                #   Pipe
                #   Underscore
                #   
                #   Crossing slashes get an X
                if char == '_' and (self.grid[y][x] == '|'
                    or self.grid[y][x] == '/' or self.grid[y][x] == '\\'):
                    segment.gridlist[i] = (x, y, char, False)
                elif (char == '|' or char == '/' or char == '\\') \
                    and self.grid[y][x] == '_':
                    self.grid[y][x] = char
                elif char == '|' and (self.grid[y][x] == '/' or self.grid[y][x] == '\\'):
                    segment.gridlist[i] = (x, y, char, False)
                elif (char == '/' or char == '\\') \
                    and self.grid[y][x] == '|':
                    self.grid[y][x] = char
                else:
                    success = False
                    self.grid[y][x] = 'X'
            #if x > row_last[y]:
            #    row_last[y] = x
            last_x = x
            last_y = y

        #return row_last, success
        return success


    def draw_line(self, segment):
        """Determine grid positions for a line segment.

           @param segment: segment to be converted to grid positions.
        """
        x1 = segment.start._col
        y1 = segment.start._row
        x2 = segment.end._col
        y2 = segment.end._row

        if segment.start.real:
            y1 += 1

        if x2 > x1:
            xdir = 1
        else:
            xdir = -1

        ydist = y2 - y1
        xdist = abs(x2 - x1)

        moves = []

        currentx = x1
        currenty = y1
        if ydist >= xdist:
            # We don't ever quite travel the whole xdist -- so it's 
            # xdist - 1 ... except in the pure vertical case where 
            # xdist is already zero. Kind of strange isn't it?
            for y in range(y1, y2 - max(0, xdist - 1)):
                moves.append((x1, y, '|', True))
                currenty = y
        else:
            currenty = y1 - 1
            # Starting from currentx, move until just enough 
            # room to go the y direction (minus 1... we don't go all the way)
            for x in range(x1, x2 - xdir * (ydist), xdir):
            #for x in range(x1 + xdir, x2 - xdir * (ydist), xdir):
                moves.append((x, y1 - 1, '_', True))
                currentx = x

        for y in range(currenty + 1, y2):
            currentx += xdir
            if xdir == 1:
                moves.append((currentx, y, '\\', True))
            else:
                moves.append((currentx, y, '/', True))

        return moves


    def print_grid(self, with_colors = False):
        """Print grid to stdout.

           @param with_colors: True if ANSI colors should be used. Otherwise
                               prints whatever terminal default is.
        """
        if not self.layout:
            self.layout_hierarchical()

        row_begin = self.pad_corner_x
        row_end = min(self.gridsize[1], self.pad_corner_x + self.width - 1)
        if not with_colors or not self.grid_colors:
            for row in self.grid:
                if self.width == 0 or self.width > self.gridsize[1]:
                    print(''.join(row))
                else:
                    window = row[rowbegin:rowend]
                    print(''.join(window))
            return

        for i in range(self.gridsize[0]):
            print(self.print_color_row(i, row_begin, row_end))


    def print_color_row(self, i, start, end):
        """Print a single text row using ANSI color escape codes.

           @param i: row to print
           @param start: start column in row to print in color
           @param end: end column in row to print in color
        """
        text = self.grid[i]
        colors = self.grid_colors[i]

        color = -1
        string = ''
        for i, ch in enumerate(text):
            if i >= start and i <= end:
                if colors[i] != color:
                    color = colors[i]
                    if color > self.maxcolor:
                        string += '\x1b[' + str(self.to_ansi_foreground(color - self.maxcolor + 10))
                    else:
                        string += '\x1b[' + str(self.to_ansi_foreground(color))
                    string += 'm'
                string += ch

        string += '\x1b[0m'
        return string


    def to_ansi_foreground(self, color):
        """Convert curses color to ANSI color.

           @param color: curses color code to convert
           @return color code of equivalent ANSI color
        """

        # Note ANSI offset for foreground color is 30 + ANSI lookup.
        # However, we are off by 1 due to curses, hence the minus one.
        if color != 0:
            color += 30 - 1
        return color


    def resize(self, stdscr):
        """Handle curses resize event.

           @param stdscr: curses window.
        """
        old_height = self.height
        self.height, self.width = stdscr.getmaxyx()
        self.offset = self.height - self.gridsize[0] - 1


        self.pad_extent_y = self.height - 1 # lower left of pad winndow
        if self.gridsize[0] < self.height:
            self.pad_pos_y = self.height - self.gridsize[0] - 1 # upper left of pad window
            self.pad_corner_y = 0
        else:
            self.pad_pos_y = 0

            # Maintain the bottom of the graph in the same place
            if old_height == 0:
                self.pad_corner_y = self.gridsize[0] - self.height
            else:
                bottom = self.pad_corner_y + old_height
                self.pad_corner_y = max(0, bottom - self.height)

        self.pad_pos_x = 0 # position of pad window upper left
        if self.gridsize[1] + 1 < self.width:
            self.pad_extent_x = self.gridsize[1] + 1
        else:
            self.pad_extent_x = self.width - 1

        self.hpad_pos_x = self.width - self.hpad_extent_x - 1
        if self.qpad:
            if self.gridsize[0] + 3 < self.height:
                self.qpad_pos_y = self.height - self.gridsize[0] - 3
            else:
                self.qpad_pos_y = 0


    def center_xy(self, stdscr, x, y):
        """Center the pad around (x,y). If this moved the pad off the screen,
           shift show screen is as full as possible with pad while still showing
           (x,y).

            @param stdscr: curses window
            @param x: x position to be centered
            @param y: y position to be centered
        """
        ideal_corner_x = self.pad_corner_x
        ideal_corner_y = self.pad_corner_y
        move_x = False
        move_y = False

        if x < self.pad_corner_x or x > self.pad_corner_x + self.width:
            ideal_corner_x = max(0, min(x - self.width / 2, self.gridsize[1] - self.width))
            move_x = True
        if y < self.pad_corner_y or y > self.pad_corner_y + self.height:
            ideal_corner_y = max(0, min(y - self.height / 2, self.gridsize[0] - self.height))
            move_y = True

        while move_x or move_y:
            if move_x:
                if self.pad_corner_x < ideal_corner_x:
                    self.scroll_left()
                else:
                    self.scroll_right()
                if self.pad_corner_x == ideal_corner_x:
                    move_x = False
            if move_y:
                if self.pad_corner_y < ideal_corner_y:
                    self.scroll_up()
                else:
                    self.scroll_down()
                if self.pad_corner_y == ideal_corner_y:
                    move_y = False
            stdscr.refresh()
            self.refresh_pad()


    def scroll_up(self, amount = 1):
        """Performs upwards scroll by moving the main pad.

           @param amount: number of rows to be scrolled.
        """
        if self.pad_corner_y + (self.pad_extent_y - self.pad_pos_y) < self.gridsize[0]:
            self.pad_corner_y += amount
            self.pad_corner_y = min(self.pad_corner_y, self.gridsize[0] + self.pad_pos_y - self.pad_extent_y)


    def scroll_down(self, amount = 1):
        """Performs downwards scroll by moving the main pad.

           @param amount: number of rows to be scrolled.
        """
        if self.pad_corner_y > 0:
            self.pad_corner_y -= amount
            self.pad_corner_y = max(self.pad_corner_y, 0)


    def scroll_left(self, amount = 1):
        """Performs left scroll by moving the main pad.

           @param amount: number of colums to be scrolled.
        """
        if self.pad_corner_x + self.width < self.gridsize[1]:
            self.pad_corner_x += amount
            self.pad_corner_x = min(self.pad_corner_x, self.gridsize[1])


    def scroll_right(self, amount = 1):
        """Performs right scroll by moving the main pad.

           @param amount: number of colums to be scrolled.
        """
        if self.pad_corner_x > 0:
            self.pad_corner_x -= amount
            self.pad_corner_x = max(self.pad_corner_x, 0)


    def refresh_pad(self):
        """Refresh the main pad. Used for redrawing.
        """
        self.pad.refresh(self.pad_corner_y, self.pad_corner_x,
            self.pad_pos_y, self.pad_pos_x,
            self.pad_extent_y, self.pad_extent_x)
        self.refresh_hpad()
        if self.qpad:
            self.refresh_qpad()


    def toggle_help(self, stdscr):
        """Change the state of the help menu between collapsed and expanded.

           @param stdscr: curses window.
        """
        if self.hpad_collapsed:
            self.expand_help()
            self.refresh_hpad()
        else:
            self.collapse_help()
            stdscr.clear()
            self.refresh_hpad()
            stdscr.refresh()
            self.refresh_pad()


    def collapse_help(self):
        """Show only the basic help commands."""
        self.hpad.clear()
        self.hpad_extent_x = self.hpad_max_collapse_x # + 1
        self.hpad_extent_y = len(self.hpad_default_cmds) # + 1
        self.hpad_pos_x = self.width - self.hpad_extent_x - 1
        self.hpad_collapsed = True
        for i in range(len(self.hpad_default_cmds)): # TODO: Use zip
            helpline = self.make_hpad_string(self.hpad_default_cmds[i],
                self.hpad_default_msgs[i],
                len(self.hpad_default_cmds[0]), len(self.hpad_default_msgs[0]))
            self.hpad.addstr(i, 0, helpline, curses.A_REVERSE)


    def expand_help(self):
        """Show full help menu."""
        self.hpad.clear()
        self.hpad_extent_y = self.hpad_max_y # + 1
        self.hpad_extent_x = self.hpad_max_x # + 1
        self.hpad_pos_x = self.width - self.hpad_extent_x - 1
        self.hpad_collapsed = False
        for i in range(len(self.hpad_cmds)): # TODO: Use zip
            helpline = self.make_hpad_string(self.hpad_cmds[i], self.hpad_msgs[i],
                self.hpad_max_cmd, self.hpad_max_msg)
            self.hpad.addstr(i, 0, helpline, curses.A_REVERSE)


    def make_hpad_string(self, cmd, msg, cmd_length, msg_length):
        """Convert command pieces into string for help menu.

           @param cmd: cmd key(s) string
           @param msg: explanation of command (string)
           @param cmd_length: horizontal space afforded to commands
           @param msg_length: horizontal space afforded to explanations
           @return string centering cmd and msg appropriately given lengths
        """
        string = ' '
        cmd_padding = cmd_length - len(cmd)
        msg_padding = msg_length - len(msg)
        string += ' ' * cmd_padding
        string += cmd
        if len(cmd) == 0:
            string += '   '
        else:
            string += ' - '
        string += msg
        string += ' ' * msg_padding
        string += ' '
        return string


    def refresh_hpad(self):
        """Refresh drawing of help menu."""
        self.hpad.refresh(self.hpad_corner_y, self.hpad_corner_x,
            self.hpad_pos_y, self.hpad_pos_x,
            self.hpad_pos_y + self.hpad_extent_y,
            self.hpad_pos_x + self.hpad_extent_x)


    def refresh_qpad(self):
        """Refresh drawing of question."""
        self.qpad.refresh(self.qpad_corner_y, self.qpad_corner_x,
            self.qpad_pos_y, self.qpad_pos_x,
            self.qpad_pos_y + self.qpad_extent_y,
            self.qpad_pos_x + self.qpad_extent_x)


    def print_interactive(self, stdscr, has_colors = False):
        """Setup curses pads and run the main interactive loop.

           @param stdscr: curses window
           @param has_colors: True if curses has color support
        """
        self.pad = curses.newpad(self.gridsize[0] + 1, self.gridsize[1] + 1)
        self.pad_corner_y = 0 # upper left position inside pad
        self.pad_corner_x = 0 # position shown in the pad

        self.hpad = curses.newpad(self.hpad_max_y + 1, self.hpad_max_x + 1)

        if self.question:
            self.qpad = curses.newpad(self.qpad_max_y, self.qpad_max_x)
            self.qpad.addstr(0, 0, self.question)

        self.resize(stdscr)

        # Save state
        self.grid_colors = []
        for row in range(self.gridsize[0]):
            self.grid_colors.append([self.default_color for x in range(self.gridsize[1])])

        # Draw initial grid and initialize colors to default
        self.redraw_default(stdscr, self.offset)
        self.expand_help()
        stdscr.refresh()
        self.refresh_pad()
        stdscr.move(self.height - 1, 0)

        command = ''
        selected = ''
        while True:
            ch = stdscr.getch()
            if self.logfile:
                self.log_character(ch)

            if ch == curses.KEY_MOUSE:
                pass
            elif ch == curses.KEY_RESIZE:
                self.resize(stdscr)
                stdscr.clear()
                stdscr.refresh()
                self.refresh_pad()
                stdscr.move(self.height - 1, 0)
            elif command == '': # Awaiting new Command

                # Quit
                if ch == ord('q') or ch == ord('Q') or ch == curses.KEY_ENTER \
                    or ch == 10:
                    if self.logfile:
                        self.logfile.write('\n')
                        self.logfile.close()
                    return

                # Start Node Selection
                elif ch == ord('/'):
                    ch = curses.ascii.unctrl(ch)
                    command = ch
                    stdscr.addstr(ch)
                    stdscr.refresh()

                elif ch == ord('h'):
                    self.toggle_help(stdscr)
                    stdscr.move(self.height - 1, 0)

                # Scroll 
                elif ch == ord('s') or ch == curses.KEY_DOWN or ch == 40:
                    self.scroll_up(5)
                    stdscr.refresh()
                    self.refresh_pad()

                elif ch == ord('w') or ch == curses.KEY_UP or ch == 38:
                    self.scroll_down(5)
                    stdscr.refresh()
                    self.refresh_pad()

                elif ch == ord('a') or ch == curses.KEY_LEFT or ch == 37:
                    self.scroll_right(5)
                    stdscr.refresh()
                    self.refresh_pad()

                elif ch == ord('d') or ch == curses.KEY_RIGHT or ch == 39:
                    self.scroll_left(5)
                    stdscr.refresh()
                    self.refresh_pad()

                # Move backwards in node selection
                elif ch == ord('p'):
                    if selected:
                        selected = self.node_order[(-1 + self._nodes[selected].order)
                            % len(self.node_order)].name
                    else:
                        selected = self.node_order[-1].name

                    self.select_node(stdscr, selected, self.offset)
                    self.refresh_pad()
                    stdscr.move(self.height - 1, 0)
                    stdscr.refresh()

                # Advance node selection
                elif ch == ord('n'):
                    if selected:
                        selected = self.node_order[(1 + self._nodes[selected].order)
                            % len(self.node_order)].name
                    else:
                        selected = self.node_order[0].name

                    self.select_node(stdscr, selected, self.offset)
                    self.refresh_pad()
                    stdscr.move(self.height - 1, 0)
                    stdscr.refresh()

                # Start Ctrl Command
                else:
                    ch = curses.ascii.unctrl(ch)
                    if ch[0] == '^' and len(ch) > 1:
                        # Highlight neighbors of a node (unused)
                        if (ch[1] == 'a' or ch[1] == 'A') and selected:
                            self.highlight_neighbors(stdscr, selected, self.offset)
                            self.refresh_pad()
                            stdscr.move(self.height - 1, 0)
                            stdscr.refresh()

                        # Move backwards in the node order
                        elif (ch[1] == 'b' or ch[1] == 'B'):
                            if selected:
                                selected = self.node_order[(-1 + self._nodes[selected].order)
                                    % len(self.node_order)].name
                            else:
                                selected = self.node_order[-1].name

                            self.select_node(stdscr, selected, self.offset)
                            self.refresh_pad()
                            stdscr.move(self.height - 1, 0)
                            stdscr.refresh()

                        # Change connectivity highlighting
                        elif (ch[1] == 'v' or ch[1] == 'V'):
                            self.highlight_full_connectivity = not self.highlight_full_connectivity
                            if selected:
                                self.redraw_default(stdscr, self.offset)
                                self.select_node(stdscr, selected, self.offset)
                                self.highlight_neighbors(stdscr, selected, self.offset)
                                self.refresh_pad()
                                stdscr.move(self.height - 1, 0)
                                stdscr.refresh()

                        # Move forwards in the node order for selection
                        elif (ch[1] == 'w' or ch[1] == 'W'):
                            if selected:
                                selected = self.node_order[(1 + self._nodes[selected].order)
                                    % len(self.node_order)].name
                            else:
                                selected = self.node_order[0].name

                            self.select_node(stdscr, selected, self.offset)
                            self.refresh_pad()
                            stdscr.move(self.height - 1, 0)
                            stdscr.refresh()

            else: # Command in progress

                # Accept Command
                if ch == curses.KEY_ENTER or ch == 10:
                    stdscr.move(self.height - 1, 0)
                    for i in range(len(command)):
                        stdscr.addstr(' ')

                    selected = self.select_node(stdscr, command[1:], self.offset)
                    self.refresh_pad()
                    stdscr.move(self.height - 1, 0)
                    stdscr.refresh()
                    command = ''

                # Handle Backspace
                elif ch == curses.KEY_BACKSPACE:
                    command = command[:-1]
                    stdscr.move(self.height - 1, len(command))
                    stdscr.addstr(' ')
                    stdscr.move(self.height - 1, len(command))
                    stdscr.refresh()

                # New character
                else:
                    ch = curses.ascii.unctrl(ch)
                    command += ch
                    stdscr.addstr(ch)
                    stdscr.refresh()


    def select_node(self, stdscr, name, offset):
        """Highlight the give node.

           @param stdscr: curses screen object. Use None for print-only
           @param name: name of node to be selected
           @param offset: unused
        """
        # Clear existing highlights
        if stdscr:
            self.redraw_default(stdscr, offset)

        if name in self._nodes:
            self.highlight_node(stdscr, name, offset, self.select_color + self.maxcolor) # Cyan
            self.highlight_neighbors(stdscr, name, offset)

            if stdscr:
                node = self._nodes[name]
                self.center_xy(stdscr, self.left_offset + node._col, node._row)
            return name

        return ''


    def highlight_neighbors(self, stdscr, name, offset):
        """Highlights node neighbors. We assume that the node in question is
           already highlighted.

           @param stdscr: curses screen object. Use None for print-only
           @param name: name of node to be selected
           @param offset: unused
        """

        node = self._nodes[name]

        self.highlight_in_neighbors(stdscr, name, offset, self.highlight_full_connectivity)
        self.highlight_out_neighbors(stdscr, name, offset, self.highlight_full_connectivity)


    def highlight_in_neighbors(self, stdscr, name, offset, recurse):
        """Highlights node in-neighbors. We assume that the node in question is
           already highlighted.

           @param stdscr: curses screen object. Use None for print-only
           @param name: name of neighbor node to be highlit
           @param offset: unused
           @param recurse: if True, highlights neighbors of neighbors recursively
        """
        node = self._nodes[name]

        for link in node._in_links:
            neighbor = self._nodes[link.source]
            self.highlight_node(stdscr, neighbor.name, offset, self.neighbor_color)
            self.highlight_segments(stdscr, link.segments, offset)

            if recurse:
                self.highlight_in_neighbors(stdscr, link.source, offset, recurse)


    def highlight_out_neighbors(self, stdscr, name, offset, recurse):
        """Highlights node out-neighbors. We assume that the node in question is
           already highlighted.

           @param stdscr: curses screen object. Use None for print-only
           @param name: name of neighbor node to be highlit
           @param offset: unused
           @param recurse: if True, highlights neighbors of neighbors recursively
        """
        node = self._nodes[name]

        for link in node._out_links:
            neighbor = self._nodes[link.sink]
            self.highlight_node(stdscr, neighbor.name, offset, self.neighbor_color)
            self.highlight_segments(stdscr, link.segments, offset)

            if recurse:
                self.highlight_out_neighbors(stdscr, link.sink, offset, recurse)


    def highlight_segments(self, stdscr, segments, offset):
        """Highlights given segments.

           @param stdscr: curses screen object. Use None for print-only
           @param segments: list of segments to be highlit
           @param offset: unused
        """
        if not stdscr:
            self.highlight_segments_printonly(segments, offset)
            return
        for segment in segments:
            for i, coord in enumerate(segment.gridlist):
                x, y, char, draw = coord
                x += self.left_offset
                if not draw or char == '':
                    continue
                self.grid_colors[y][x] = self.neighbor_color
                if self.grid[y][x] == ' ' or self.grid[y][x] == char:
                    self.pad.addch(y, x, char, curses.color_pair(self.neighbor_color))
                elif char != self.grid[y][x]:
                    if char == '_' and (self.grid[y][x] == '|'
                        or self.grid[y][x] == '/' or self.grid[y][x] == '\\'):
                        segment.gridlist[i] = (x, y, char, False)
                    elif (char == '|' or char == '/' or char == '\\') \
                        and self.grid[y][x] == '_':
                        self.grid[y][x] = char
                        self.pad.addch(y, x,char, curses.color_pair(self.neighbor_color))
                    elif char == '|' and (self.grid[y][x] == '/' or self.grid[y][x] == '\\'):
                        segment.gridlist[i] = (x, y, char, False)
                    elif (char == '/' or char == '\\') \
                        and self.grid[y][x] == '|':
                        self.grid[y][x] = char
                        self.pad.addch(y, x,char, curses.color_pair(self.neighbor_color))
                    else:
                        self.pad.addch(y, x, 'X', curses.color_pair(self.neighbor_color))


    def highlight_segments_printonly(self, segments, offset):
        """Highlights given segments in internal data structure. Does not use curses.

           @param segments: list of segments to be highlit
           @param offset: unused
        """
        for segment in segments:
            for i, coord in enumerate(segment.gridlist):
                x, y, char, draw = coord
                x += self.left_offset
                if not draw or char == '':
                    continue
                self.grid_colors[y][x] = self.neighbor_color
                if char != self.grid[y][x]:
                    if char == '_' and (self.grid[y][x] == '|'
                        or self.grid[y][x] == '/' or self.grid[y][x] == '\\'):
                        segment.gridlist[i] = (x, y, char, False)
                    elif (char == '|' or char == '/' or char == '\\') \
                        and self.grid[y][x] == '_':
                        self.grid[y][x] = char
                    elif char == '|' and (self.grid[y][x] == '/' or self.grid[y][x] == '\\'):
                        segment.gridlist[i] = (x, y, char, False)
                    elif (char == '/' or char == '\\') \
                        and self.grid[y][x] == '|':
                        self.grid[y][x] = char
                    else:
                        self.grid[y][x] = 'X'


    def highlight_node(self, stdscr, name, offset, color):
        """Highlights given node to the given color.

           @param stdscr: curses window
           @param name: name of node to be highlit
           @param offset: unused
           @param color: curses color pair ID for color to be used
        """
        if name not in self._nodes:
            return ''
        if not stdscr:
            self.highlight_node_printonly(name, offset, color)
            return

        node = self._nodes[name]
        self.pad.addch(node._row, self.left_offset + node._col, 'o', curses.color_pair(color))
        self.grid_colors[node._row][self.left_offset + node._col] = color
        label_offset = 0
        if node.use_offset:
            # Offset for shifting the graph, starting at the last mark in the
            # row, and then an extra space after the last mark
            label_offset = self.left_offset + self.row_last_mark[node._row] + 2
        for i, ch in enumerate(node.name):
            self.grid_colors[node._row][label_offset + node.label_pos + i] = color
            self.pad.addch(node._row, label_offset + node.label_pos + i,
                ch, curses.color_pair(color))

        return name


    def highlight_node_printonly(self, name, offset, color):
        """Highlights given node to the given color in the internal data structure.

           @param name: name of node to be highlit
           @param offset: unused
           @param color: curses color pair ID for color to be used
        """
        node = self._nodes[name]
        self.grid_colors[node._row][self.left_offset + node._col] = color
        label_offset = 0
        if node.use_offset:
            label_offset = self.left_offset + self.row_last_mark[node._row] + 2
        for i, ch in enumerate(node.name):
            self.grid_colors[node._row][label_offset + node.label_pos + i] = color

        return name


    def redraw_default(self, stdscr, offset):
        """Redraws the default (unhighlighted) graph to curses.

           @param stdscr: curses window
           @param offset: unused
        """
        for h in range(self.gridsize[0]):
            for w in range(self.gridsize[1]):
                self.grid_colors[h][w] = self.default_color
                if self.grid[h][w] != '':
                    self.pad.addch(h, w, self.grid[h][w], curses.color_pair(self.default_color))
                else:
                    continue


    def find_crossings(self, segments):
        """Bentley-Ottmann line-crossing detection.

           We sweep from bottom to top because the layout y's are
           negative values. The intuition is having the DAG
           upside down and sweeping from top to bottom.

           @param segments: list of TermSegments
        """
        self.bst = TermBST() # BST of segments crossing L
        self.pqueue = [] # Priority Queue of potential future events
        self.crossings = dict() # Will be (segment1, segment2) = (x, y)

        # Put all segments in queue
        # The pushed tuple is of the form (y, x, name1, name2)
        # Different names indicate the (y, x) is a crossing rather than an
        # endpoint
        for segment in segments:
            heapq.heappush(self.pqueue, (segment.y1, segment.x1, segment.name, segment.name))
            heapq.heappush(self.pqueue, (segment.y2, segment.x2, segment.name, segment.name))

        while self.pqueue:
            y1, x1, name1, name2 = heapq.heappop(self.pqueue)
            segment1 = self.segment_ids[name1]
            segment2 = self.segment_ids[name2]

            if segment1.is_top_endpoint(x1, y1):
                self.top_endpoint(segment1)
            elif segment1.is_bottom_endpoint(x1, y1):
                self.bottom_endpoint(segment1)
            else:
                self.crossing(x1, y1, segment1, segment2)


    def top_endpoint(self, segment):
        """Handle top endpoint condition in Bentley-Ottman.

           @param segment: current segment
        """

        # Add end point to BST
        self.bst.insert(segment)

        # Check for crossings of BST neighbors of the segment
        # If it exists, remove it
        before = self.bst.find_previous(segment)
        after = self.bst.find_next(segment)
        if before and after and (before.name, after.name) in self.crossings:
            x, y = self.crossings[(before.name, after.name)]
            if (y, x, before.name, after.name) in self.pqueue:
                self.pqueue.remove((y, x, before.name, after.name))
                heapq.heapify(self.pqueue)

        # Check for and catalog crossing of before neighbor
        bcross, x, y = segment.intersect(before)
        if bcross and (y, x, before.name, segment.name) not in self.pqueue:
            heapq.heappush(self.pqueue, (y, x, before.name, segment.name))
            self.crossings[(before.name, segment.name)] = (x, y)

        # Check for and catalog crossing of after neighbor
        across, x, y = segment.intersect(after)
        if across and (y, x, segment.name, after.name) not in self.pqueue:
            heapq.heappush(self.pqueue, (y, x, segment.name, after.name))
            self.crossings[(segment.name, after.name)] = (x, y)


    def bottom_endpoint(self, segment):
        """Handle bottom endpoint case in Bentley-Ottman.

           @param segment: current segment
        """
        # Find BST neighbors
        before = self.bst.find_previous(segment)
        after = self.bst.find_next(segment)

        # Remove segment from BST
        self.bst.delete(segment)

        # Check for and catalog crossing of neighbors
        if before:
            bacross, x, y = before.intersect(after)
            if bacross and y > segment.y1 and (y, x, before.name, after.name) not in self.pqueue:
                heapq.heappush(self.pqueue, (y, x, before.name, after.name))
                self.crossings[(before.name, after.name)] = (x, y)


    def crossing(self, c1, c2, segment1, segment2):
        """Handle crossing case in Bentley-Ottman.

           @param c1: crossing y coordinate
           @param c2: crossing x coordinate
           @param segment1: first crossing segment
           @param segment2: second crossing segment
        """
        # Find neighbors in the BST of the crossing pair
        first = segment1
        second = segment2
        before = self.bst.find_previous(first)
        if before and before.name == segment2.name:
            first = segment2
            second = segment1
            before = self.bst.find_previous(first)

        after = self.bst.find_next(second)

        # Now do the swap of the crossing segmenets
        self.bst.swap(first, second, c1, c2)

        # Remove crossings between first/before and second/after
        # from the priority queue
        if second and after and (second.name, after.name) in self.crossings:
            x, y = self.crossings[(second.name, after.name)]
            if (y, x, second.name, after.name) in self.pqueue:
                self.pqueue.remove((y, x, second.name, after.name))
                heapq.heapify(self.pqueue)
        if before and first and (before.name, first.name) in self.crossings:
            x, y = self.crossings[(before.name, first.name)]
            if (y, x, before.name, first.name) in self.pqueue:
                self.pqueue.remove((y, x, before.name, first.name))
                heapq.heapify(self.pqueue)

        # Add possible new crossings after the swap
        if before:
            cross1, x, y = before.intersect(second)
            if cross1 and y > c2 and (y, x, before.name, second.name) not in self.pqueue:
                heapq.heappush(self.pqueue, (y, x, before.name, second.name))
                self.crossings[(before.name, second.name)] = (x, y)
        cross2, x, y = first.intersect(after)
        if cross2 and y > c2 and (y, x, first.name, after.name) not in self.pqueue:
            heapq.heappush(self.pqueue, (y, x, first.name, after.name))
            self.crossings[(first.name, after.name)] = (x, y)


class TermBST(object):
    """Binary Search Tree class for overlap detection."""

    def __init__(self):
        self.root = None


    def insert(self, segment):
        """Insert segment into the BST.

           @param segment: segment to be inserted
        """
        self.root = self.insert_helper(self.root, segment)


    def insert_helper(self, root, segment):
        """Helper function for segment insert.

           @param root: subtree root to insert segment into
           @param segment: segment to be inserted
           @return root of the changed subtree
        """
        if root is None:
            root = TermBSTNode(segment)
            segment.BSTNode = root
        elif root.segment > segment:
            root.left = self.insert_helper(root.left, segment)
            root.left.parent = root
        else:
            root.right = self.insert_helper(root.right, segment)
            root.right.parent = root
        return root


    def swap(self, segment1, segment2, b1, b2):
        """Swap two segments in the BST.

           @param segment1: first segment to be swapped
           @param segment2: second segment to be swapped
           @param b1: crossing order value 1
           @param b2: crossing order value 2
        """
        node1 = segment2.BSTNode
        node2 = segment1.BSTNode
        node1.segment = segment2
        node2.segment = segment1
        segment1.b1 = b1
        segment2.b1 = b1
        segment1.b2 = b2
        segment2.b2 = b2


    def find(self, segment):
        """Find segment node in BST.

           @param segment: segment to be found.
        """
        return self.find_helper(self.root, segment)


    def find_helper(self, root, segment):
        """Helper function for recursive segment finding.

           @param root: root of subtree to search
           @param segment: segment to be found.
           @return found node
        """
        if root is None or root.segment == segment:
            return root
        elif root.segment > segment:
            return self.find_helper(root.left, segment)
        else:
            return self.find_helper(root.right, segment)


    def find_previous(self, segment):
        """Find the previous node to the given segment.

           @param segment: segment whose previous node is to be found.
           @return predecessor node
        """
        node = segment.BSTNode
        assert node is not None, \
            "Attempting to find previous of segment without a BST node."
        predecessor = node.left
        last = predecessor
        while predecessor:
            last = predecessor
            predecessor = predecessor.right
        if last:
            return last.segment
        else:
            predecessor = None
            last = node
            search = node.parent
            while search:
                if search.right == last:
                    return search.segment
                else:
                    last = search
                    search = search.parent
            return predecessor


    def find_next(self, segment):
        """Find the next node to the given segment in BST order.

           @param segment: segment whose next node is to be found.
           @return successor node
        """
        node = segment.BSTNode
        assert node is not None, \
            "Attempting to find next of segment without a BST node."
        successor = node.right
        last = successor
        while successor:
            last = successor
            successor = successor.left
        if last:
            return last.segment
        else:
            successor = None
            last = node
            search = node.parent
            while search:
                if search.left == last:
                    return search.segment
                else:
                    last = search
                    search = search.parent
            return successor


    def delete(self, segment):
        """Delete a segment from the BST.

           @param segment: segment to be deleted
        """
        node = segment.BSTNode
        segment.BSTNode = None
        assert node is not None, \
            "Attempting to delete segment from BST without a BST node."

        replacement = None
        if node.left is None and node.right is None:
            replacement = None

        elif node.left is None:
            replacement = node.right

        elif node.right is None:
            replacement = node.left

        else:
            predecessor = node.left
            last = predecessor
            while predecessor:
                last = predecessor
                predecessor = predecessor.right
            node.segment = last.segment
            self.delete(last.segment)
            replacement = node
            replacement.segment.BSTNode = replacement

        if not node.parent:  # We must have been the root
            self.root = replacement
        elif node.parent.left == node:
            node.parent.left = replacement
        elif node.parent.right == node:
            node.parent.right = replacement
        else:
            return

        if replacement:
            replacement.parent = node.parent


class TermBSTNode(object):
    """Class for Binary Search Tree node struct."""

    def __init__(self, segment):
        """Constructor of TermBSTNode

           @param segment: segment contained in BST node.
        """
        self.segment = segment
        self.left = None
        self.right = None
        self.parent = None


class TermSegment(object):
    """A straight-line portion of a drawn poly-line in the graph rendering."""

    def __init__(self, x1, y1, x2, y2, name = ''):
        """Constructor for TermSegment.

           @param x1: x-coordinate of start
           @param y1: y-coordinate of start
           @param x2: x-coordinate of end
           @param y2: y-coordinate of end
           @param name: optional name of segment
        """
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.name = name
        self.BSTNode = None
        self.vertical = (abs(self.x1 - self.x2) < 0.001)

        # Initial sort order for crossing detection
        # Since y is negative, in normal sort order, we start from there
        self.b1 = x2
        self.b2 = y2

        # Alternative representations for crossing detection
        self.p1 = (x1, y1)
        self.p2 = (x2, y2)
        self.pdiff = (x2 - x1, y2 - y1)

        self.start = None
        self.end = None
        self.octant = -1
        self.gridlist = []
        self.links = []

        # From splits
        self.children = []
        self.origin = self
        self.original_end = None
        self.vertical_crossing_count = 0
        self.crossing_count = 0

        self.paths = set()


    def addCrossing(self, other, point):
        """Update crossing information on this link.

           @param other: link which crosses us
           @param point: crossing point of other link
        """
        self.crossing_count += 1
        if other.vertical:
            self.vertical_crossing_count += 1


    def for_segment_sort(self):
        """Metric for sorting segments.

           @return metric value for use in sorting
        """
        xlen = abs(self.x1 - self.x2)
        ylen = abs(self.y1 - self.y2)

        seg = 0
        # Pure vertical should sort smallest
        if xlen > 0:
            seg += 1e9

        # After that, number of characters:
        seg += xlen + ylen
        return seg


    def split(self, node, bundle = False):
        """Split this segment into two at node. Return the next segment.

           Note the new segment is always the second part (closer to the sink).

           @param node: end point of two new segments
           @param bundle: True if this is part of a bundled edge
        """

        # The one we are splitting from may have been updated by a previous split
        # Note that now that we can define horizontal paths, we can't rely on 
        # the y value to totally define. 
        # Therefore, we must find the correct part of this multi-split link to
        # split from, one that contains the node
        splitter = self
        if bundle:
            if self.x1 < self.x2:
                if node._x < self.x1 or node._x > self.x2:
                    for child in self.origin.children:
                        if node._x > child.x1 and node._x < child.x2:
                            splitter = child
            else:
                if node._x < self.x2 or node._x > self.x1:
                    for child in self.origin.children:
                        if node._x > child.x2 and node._x < child.x1:
                            splitter = child
        else:
            if node._y > self.y1 or node._y < self.y2:
                for child in self.origin.children:
                    if node._y < child.y1 and node._y > child.y2:
                        splitter = child

        other = TermSegment(node._x, node._y, splitter.x2, splitter.y2)
        other.start = node
        other.end = splitter.end
        other.name = str(self.origin.name) + '-(' + str(node._x) + ')'
        other.paths = self.paths.copy()
        splitter.end = node
        splitter.x2 = node._x
        splitter.y2 = node._y
        for link in self.origin.links:
            # Why had this never been triggered before since it should have
            # failed
            link.segments.append(other)

        other.origin = self.origin
        self.origin.children.append(other)

        return other


    # The x1, y1 are always the least negative y and therefore
    # in the sorting order they act as the  bottom
    def is_bottom_endpoint(self, x, y):
        """Check if (x,y) is the bottom end point of the segment.

           @param x: x to check
           @param y: y to check
           @return True if the end point matches
        """
        if abs(x - self.x1) < 1e-6 and abs(y - self.y1) < 1e-6:
            return True
        return False


    def is_top_endpoint(self, x, y):
        """Check if (x,y) is the top end point of the segment.

           @param x: x to check
           @param y: y to check
           @return True if the end point matches
        """
        if abs(x - self.x2) < 1e-6 and abs(y - self.y2) < 1e-6:
            return True
        return False


    def intersect(self, other):
        """Check for intersection with another segment.

           @param other: segment we may intersect with
           @return a tuple where the first value indicates whether
                   there was an intersection and the next two values
                   indicate the intersecting point if there was one.
        """
        if other is None:
            return (False, 0, 0)

        # See: stackoverflow.com/questions/563198
        diffcross = self.cross2D(self.pdiff, other.pdiff)
        initcross = self.cross2D((other.x1 - self.x1, other.y1 - self.y1),
            self.pdiff)

        if diffcross == 0 and initcross == 0: # Co-linear
            # Impossible for our purposes -- we do not count intersection at
            # end points
            return (False, 0, 0)

        elif diffcross == 0: # parallel
            return (False, 0, 0)

        else: # intersection!
            offset = initcross / diffcross
            offset2 = self.cross2D((other.x1 - self.x1, other.y1 - self.y1), other.pdiff) / diffcross

            if offset > 0 and offset < 1 and offset2 > 0 and offset2 < 1:
                xi = other.x1 + offset * other.pdiff[0]
                yi = other.y1 + offset * other.pdiff[1]
                return (True, xi, yi)
            return (False, 0, 0)


    def cross2D(self, p1, p2):
        """Return 2D cross product of two points.

           @param p1: point 1 as (x, y)
           @param p2: point 2 as (x, y)
           @return cross product of p1 and p2
        """
        return p1[0] * p2[1] - p1[1] * p2[0]


    def __eq__(self, other):
        """Check if segments are equal. They are equal if they have the
           same end points.

           @param other: other segment to check.
           @return True if equal, False otherwise
        """
        if other is None:
            return False
        return (self.x1 == other.x1
            and self.x2 == other.x2
            and self.y1 == other.y1
            and self.y2 == other.y2)


    # For the line-sweep algorithm, we have some consistent ordering
    # as we will have a lot of collisions on just y alone.
    def __lt__(self, other):
        """Less than comparison operator. This one compares the b values first.

           @param other: segment to be compared for sorting
           @return True if this segment is less than the other
        """
        if self.b1 == other.b1:
            if self.x1 == other.x1:
                if self.b2 == other.b2:
                    if self.y1 < other.y1:
                        return True
                elif self.b2 < other.b2:
                    return True
            elif self.x1 < other.x1:
                return True
        elif self.b1 < other.b1:
            return True

        return False


    def traditional_sort(self, other):
        """Comparison operator for traditional sort. Only compares end point
           values. Compares y value first, then x, starting with the first point
           and continuing onto the second if necessary.

           @param other: segment to be compared for sorting
           @return True if this segment is less than the other
        """
        if self.y1 == other.y1:
            if self.x1 == other.x1:
                if self.y2 == other.y2:
                    if self.x2 < other.x2:
                        return True
                elif self.y2 < other.y2:
                    return True
            elif self.x1 < other.x1:
                return True
        elif self.y1 < other.y1:
            return True

        return False


    def __str__(self):
        """String representation of a segment.

           @return string representation
        """
        return "%s - TermSegment(%s, %s, %s, %s) " % (self.name, self.x1, self.y1,
            self.x2, self.y2) + str(self.paths)


    def __hash__(self):
        """Hash of a segment.

           @return hash of a segment.
        """
        return hash(self.__repr__())


class TermNode(object):
    """Class for internal node representation."""

    def __init__(self, node_id, real = True):
        """Constructor for TermNode.

           @param node_id: name of the node
           @param real: True if part of the given graph, False if used
                        of layout of edges (placer node)
        """
        self.name = node_id
        self._in_links = list()
        self._out_links = list()
        self.rank = -1 # Int
        self._x = -1  # Real
        self._y = -1  # Real
        self._col = 0 # Int
        self._row = 0 # Int
        self.label_pos = -1 # Int
        self.use_offset = True
        self.coord = (-1, -1)

        self.real = real # Real node or segment connector?
        self._in_segments = list()
        self.crossing_counts = dict() # y -> # of crossings from in segments
        self.crossing_heights = dict() # y -> where the crossing should occur


    def reset(self):
        """Reset layout values to prepare for re-doing layout."""
        self.rank = -1 # Int
        self._x = -1  # Real
        self._y = -1  # Real
        self._col = 0 # Int
        self._row = 0 # Int
        self.label_pos = -1 # Int
        self.use_offset = True

        self._in_segments = list()
        self.crossing_counts = dict() # y -> # of crossings from in segments
        self.crossing_heights = dict() # y -> where the crossing should occur


    def add_in_link(self, link):
        """Add in-link for bookkeeping.

           @param link: TermLink with sink at this node.
        """
        self._in_links.append(link)


    def add_out_link(self, link):
        """Add out-link for bookkeeping.

           @param link: TermLink with source at this node.
        """
        self._out_links.append(link)


    def add_in_segment(self, segment):
        """Add in-segment for bookkeeping.

           @param segment: TermSegment with sink at this node.
        """
        if segment.y1 == segment.y2:
            self.vertical_in = segment
        self._in_segments.append(segment)


    def findCrossingHeights(self, min_x, max_x):
        """Determine where crossings between segments should take place for bundling.

           @param min_x: min_x in outer graph
           @param max_x: max_x in outer graph
        """
        for segment in self._in_segments:
            y = segment.y1
            if y not in self.crossing_counts:
                self.crossing_counts[y] = 0
            self.crossing_counts[y] += segment.vertical_crossing_count

        # We set different offsets for different x values based on the
        # min and max x -- we never go higher than half way up the y value
        # We use our own x as a normalization factor to figure out the
        # ordering of heights for bundling -- this is to separate the bundle 
        # heights going into the same row.
        normalized = 1.0
        if max_x - min_x != 0:
            normalized = 0.5 * (self._x - min_x) / (max_x - min_x)
        for y, count in self.crossing_counts.items():
            if count > 0:
                offset = (self._y - y) * normalized
                self.crossing_heights[y] = self._y - offset


    def skeleton_copy(self):
        """Copy for graph layout.

           @return new TermNode with only link information.
        """
        cpy = TermNode(self.name, self.real)
        for link in self._in_links:
            cpy.add_in_link(link.id)
        for link in self._out_links:
            cpy.add_out_link(link.id)
        return cpy


class TermLink(object):
    """Class for internal link representation."""

    def __init__(self, link_id, source_id, sink_id):
        """Constructor for TermLink.

           @param link_id: the name of the link
           @param source_id: the name of the source node
           @param sink_id: the name of the sink node
        """
        self.id = link_id
        self.source = source_id
        self.sink = sink_id
        self._coords = None
        self._edgeLength = 1

        self.segments = []


    def reset(self):
        """Reset internal structures for layout information."""
        self._coords = None

        self.segments = []


    def skeleton_copy(self):
        """Copy with just enough information for layout."""
        return TermLink(self.id, self.source, self.sink)


class TermLayout(object):
    """Class for calculating graph layout. This implements the
       Hierarchical Layout of D. Auber from the Tulip graph drawing
       framework version 4.9.0. It has elements of the HierachicalLayout and
       TreeReingoldAndTilfordExtended layouts. Note this does not perfectly
       copy those layouts, only the portions needed for DAG layouts. It does
       NOT handle edge reversal or self-loops, for example.

       See http://tulip.labri.fr/
    """

    def __init__(self, graph, sweeps = 4):
        """Constructor for TermLayout.

           @param graph: TermDAG object
           @param sweeps: Number of iterations of crossing reduction, defaults
                          to 4
        """
        self.original = graph
        self.valid = False
        self.err = ""
        self.single_source_tree = True

        self._nodes = dict()
        self._nodes_list = list()
        self._added = dict()
        self._running_neighbors = dict()
        self._links = list()
        self._link_dict = dict()

        # ----------------------------------------------------
        # Structures to match C++ layout version:
        #
        # For keeping nodes in added order
        self._nodes_list = list()
        # For keeping track of which nodes were added
        self._added = dict()
        # For keeping track of neighbor add order
        self._running_neighbors = dict()
        # For keeping track of which links were modified
        self._modified_links = set()
        # For keep track of which links were in the original version
        self._original_links = list()
        # ----------------------------------------------------

        # Make a copy so as not to clobber original data
        for name in graph._nodes_list:
            self._nodes_list.append(name)
            self._added[name] = 0
            self._running_neighbors[name] = set()
        for name, node in graph._nodes.items():
            self._nodes[name] = node.skeleton_copy()

        for link in graph._links:
            skeleton = link.skeleton_copy()
            self._links.append(skeleton)
            self._original_links.append(skeleton)
            self._link_dict[link.id] = skeleton
            self._running_neighbors[link.source].add(link.sink)
            self._running_neighbors[link.sink].add(link.source)


        # Layout parameters
        self.grid = []
        self.num_sweeps = sweeps
        self.spacing = 5.0
        self.node_spacing = 5.0


    def is_valid(self):
        """True if layout has been completed."""
        return self.valid


    def get_node_coord(self, name):
        """Returns the node's coordinate.

           @param name: node name
           @return Coordinate according to layout
        """
        return self._nodes[name].coord


    def get_link_segments(self, name):
        """Returns the list of a links segments.

           @param name: the link id
           @return List of segment end point coordinates.
        """
        return self._link_dict[name].segments


    def RTE(self, source, rankSizes):
        """Implements the Reingold-Tilford Extended algorithm to match
           the Tulip version.

           @param source: the added source node.
           @oaram rankSizes: a dictionary tracking the number of elements
                             in each rank.
        """
        relativePosition = dict() # node -> double

        # TreePlace -- figure out LR tree extents, put placements in
        # relativePosition
        self.treePlace(source, relativePosition)

        # Calc Layout -- convert relativePosition into coords
        self.calcLayout(source, relativePosition, 0, 0, 0, rankSizes)

        # Ortho is true -- do edge bends
        # This may be unnecessary
        for link in self._links:
            source = self._nodes[link.source]
            sink = self._nodes[link.sink]
            sourcePos = source.coord
            sinkPos = sink.coord

            tmp = []
            if sourcePos[0] != sinkPos[0]:
                tmp.append((sinkPos[0], sourcePos[1]))
                link.coords = tmp


    def calcLayout(self, node, relativePosition, x, y, rank, rankSizes):
        """Calculates the position of a node.

           @param node: a node object to be placed
           @param relativePosition: dict containing the relative position of the nodes to
                                    the others in the layout.
           @param x: x offset so far
           @param y: y offset so far
           @param rank: the depth of the current node
           @param rankSizes: dict of how many ranks per node... only sused for spacing, REMOVE ME

           Note: as all nodes are the same size, we don't have to worry about spacing.
        """
        node.coord = (x + relativePosition[node], -1 * self.spacing * rank)
        for linkid in node._out_links:
            link = self._link_dict[linkid]
            out = self._nodes[link.sink]

            # New
            lenCounter = link._edgeLength
            decalY = y + self.spacing * lenCounter
            decalLevel = rank + lenCounter

            self.calcLayout(out, relativePosition, x + relativePosition[node],
                decalY, decalLevel, rankSizes)


    def treePlace(self, node, relativePosition):
        """Calculate the positions of the subtrees.

           @param node: root node of subtree to be placed
           @param relativePosition: dict keeping track of the relative positions of the nodes
        """
        if len(node._out_links) == 0:
            relativePosition[node] = 0
            return [(-0.5, 0.5, 1)] # Triple L, R, size

        childPos = []
        leftTree = self.treePlace(self._nodes[self._link_dict[node._out_links[0]].sink],
            relativePosition)
        childPos.append((leftTree[0][0] + leftTree[0][1]) / 2.0)

        # useLength
        if self._link_dict[node._out_links[0]]._edgeLength > 1:
            leftTree.insert(0, (leftTree[0][0], leftTree[0][1],
                self._link_dict[node._out_links[0]]._edgeLength - 1)) # length is probably always 1

        for linkid in node._out_links[1:]:
            link = self._link_dict[linkid]

            rightTree = self.treePlace(self._nodes[link.sink], relativePosition)

            if link._edgeLength > 1:
                rightTree.insert(0, (rightTree[0][0], rightTree[0][1],
                    link._edgeLength - 1))

            decal = self.calcDecal(leftTree, rightTree)
            tempLeft = (rightTree[0][0] + rightTree[0][1]) / 2.0

            merged = self.mergeLR(leftTree, rightTree, decal)
            if merged == leftTree:
                childPos.append(tempLeft + decal)
                rightTree = []
            else:
                for i, pos in enumerate(chlidPos):
                    childPos[i] = pos - decal
                childPos.append(tempLeft)
                leftTree = rightTree


        posFather = (leftTree[0][0] + leftTree[0][1]) / 2.0
        leftTree.insert(0, (posFather - 0.5, posFather + 0.5, 1))
        for i, linkid in enumerate(node._out_links):
            link = self._link_dict[linkid]
            relativePosition[self._nodes[link.sink]] = childPos[i] - posFather
        relativePosition[node] = 0
        return leftTree


    def mergeLR(self, left, right, decal):
        # Left and Right lists are tuples (left, right, size)
        # We use these variables for the indexing
        L = 0
        R = 1
        size = 2

        iL = 0
        iR = 0
        itL = 0
        itR = 0

        while itL < len(left) and itR < len(right):
            minSize = min(left[itL][size] - iL, right[itR][size] - iR)
            tmp = (left[itL][L], right[itR][R] + decal, minSize)


            if left[itL][size] == 1:
                left[itL] = tmp
            else:
                if iL == 0:
                    if iL + minSize >= left[itL][size]:
                        left[itL] = tmp
                    else:
                        left.insert(itL, tmp)
                        itL += 1  #Increment after insert
                        left[itL] = (left[itL][L], left[itL][R], left[itL][size] - minSize)
                        iL = -1 * minSize
                else:
                    if iL + minSize >= left[itL][size]: # end
                        left[itL] = (left[itL][L], left[itL][R], left[itL][size] - minSize)
                        itL += 1
                        left.insert(itL, tmp)
                        itL += 1  #Increment after insert
                        iL = -1 * minSize
                    else: # middle
                        tmp2 = left[itL]
                        left[itL] = (left[itL][L], left[itL][R], iL)
                        itL += 1
                        left.insert(itL, tmp)
                        itL += 1  #Increment after insert
                        tmp2 = (tmp2[L], tmp2[R], tmp2[size] - (iL + minSize))
                        left.insert(itL, tmp2)
                        itL += 1  #Increment after insert
                        itL -= 1
                        iL = -1 * minSize


            iL += minSize
            iR += minSize

            if iL >= left[itL][size]:
                itL += 1
                iL = 0
            if iR >= right[itR][size]:
                itR += 1
                iR = 0

        if itL < len(left) and iL != 0:
            tmp = (left[itL][L], left[itL][R], left[itL][size] - iL)
            itL += 1

        if itR < len(right):
            if iR != 0:
                tmp = (right[itR][L] + decal, right[itR][R] + decal, right[itR][size] - iR)
                left.append(tmp)
                itR += 1

            while itR < len(right):
                tmp = (right[itR][L] + decal, right[itR][R] + decal, right[itR][size])
                left.append(tmp)
                itR += 1

        return left


    def calcDecal(self, leftTree, rightTree):
        iL = 0
        iR = 0
        decal = leftTree[iL][1] - rightTree[iR][0]
        minSize = min(leftTree[iL][2], rightTree[iR][2])
        sL = minSize
        sR = minSize

        if sL == leftTree[iL][2]:
            iL += 1
            sL = 0
        if sR == rightTree[iR][2]:
            iR += 1
            sR = 0

        while iL < len(leftTree) and iR < len(rightTree):
            decal = max(decal, leftTree[iL][1] - rightTree[iR][0])
            minSize = min(leftTree[iL][2] - sL, rightTree[iR][2] - sR)
            sL += minSize
            sR += minSize

            if sL == leftTree[iL][2]:
                iL += 1
                sL = 0

            if sR == rightTree[iR][2]:
                iR += 1
                sR = 0

        return decal + self.node_spacing


    def layout(self):
        """Run layout algorithm. After the algorithm is run, the resulting
           coordinates are in TL's skeleton nodes and links.
        """
        # Check for cycles -- error if not a DAG
        if self.has_cycles():
            self.valid = False
            self.err = "ERROR: Graph is not a DAG."
            return

        # Ensure single source
        if self.single_source_tree:
            for node in self._nodes.values():
                if not node._in_links:
                    source_node = node
                    break
            for link in self._links:
                link.children = []
        else:
            source_node = self.create_single_source()

        # Set Ranks
        maxRank = self.setRanks(source_node)
        for i in range(maxRank + 1):
            self.grid.append([])

        # Divide nodes by rank into grid
        for name in self._nodes_list:
            node = self._nodes[name]
            self.grid[node.rank].append(node)

        # Ensure each link spans exactly one rank
        if not self.single_source_tree:
            self.makeProper(source_node)

        embedding = dict()


        # Reorder in rank
        if not self.single_source_tree:
            self.reduceCrossings(source_node, embedding)

            self.createSpanningTree(embedding)

        # Apply Tree algorithm
        rankSizes = []
        for row in self.grid:
            rankSizes.append(len(row))
        self.RTE(source_node, rankSizes) #self.grid)

        # Do Edge Bends
        self.computeEdgeBends()

        self.valid = True


    def createSpanningTree(self, embedding):
        """Modify the skeleton graph structure such that there's a tree rather
           than a DAG.

           @param embedding: The dictionary keeping embedding values for each node
        """

        # We only keep one in-link: the one that falls in the middle of 
        # our sort of them by the embedding of their sources.
        for name in self._nodes_list:
            node = self._nodes[name]
            if len(node._in_links) > 1:
                # Sort by source node
                node._in_links.sort(key = lambda x : embedding[self._link_dict[x].source])

                # Find the halfway point
                half = int(math.floor(len(node._in_links) / 2))

                # Keep only the halfway point
                node._in_links = [ node._in_links[half] ]


        # Remove all the links that were no kept. 
        for name in self._nodes_list:
            node = self._nodes[name]
            toRemove = list()
            for link in node._out_links:
                if link not in self._nodes[self._link_dict[link].sink]._in_links:
                    toRemove.append(link)
            for link in toRemove:
                node._out_links.remove(link)
            node._out_links = sorted(node._out_links, key = lambda x : embedding[self._link_dict[x].sink])


    def afterCoord(self, coord):
        """Return the coordinate just after the node.

           @param coord: coordinate to offset
           @return coordinate just lower in y
        """
        return (coord[0], coord[1] - self.spacing / 4.0)


    def beforeCoord(self, coord):
        """Return the coordinate just before the node.

           @param coord: coordinate to offset
           @return coordinate just higher in y
        """
        return (coord[0], coord[1] + self.spacing / 4.0)


    def computeEdgeBends(self):
        """Set the link segments as determined by the placer nodes in the layout."""

        # For each of the original links, set its segments
        for link in self._original_links:

            # First bend is right after the source node in y
            link.segments.append(self.afterCoord(self._nodes[link.source].coord))

            # If their are placer nodes, add the place the area around them
            # This is just above the first placer node and just after the
            # last placer node.
            if link.children:
                firstCoord = self._nodes[link.sink].coord
                secondCoord = self._nodes[link.children[-1].source].coord
                if firstCoord != secondCoord:
                    link.segments.append(self.beforeCoord(firstCoord))
                    link.segments.append(self.afterCoord(secondCoord))
                else:
                    link.segments.append(self.beforeCoord(firstCoord))
                    link.segments.append(self.afterCoord(firstCoord))

                # Finally add the node just before the sink
                link.segments.append(self.beforeCoord(self._nodes[link.children[-1].sink].coord))

            # If their are no placer nodes, just add the area right before the
            # sink
            else:
                link.segments.append(self.beforeCoord(self._nodes[link.sink].coord))


    def initCross(self, name, visited, embedding, dfsid):
        """Set the initial embedding order. This implements a DFS.

           @param name: name of node to have its embedding set
           @param visited: dictionary of already visited nodes
           @param embedding: dictionary holding node embedding values
           @param dfsid: depth first search depth
        """
        if (visited[name]):
            return

        visited[name] = True
        embedding[name] = dfsid
        node = self._nodes[name]
        for linkid in node._out_links:
            if linkid not in self._modified_links:
                sink = self._link_dict[linkid].sink
                self.initCross(sink, visited, embedding, dfsid + 1)
        for linkid in node._out_links:
            if linkid in self._modified_links:
                sink = self._link_dict[linkid].sink
                self.initCross(sink, visited, embedding, dfsid + 1)


    def reduceCrossings(self, source, embedding):
        """Permute the row order to reduce edge crossings.

           @param source: source node of the DAG
           @param embedding: dictionary of embeddings of nodes
        """
        visited = dict()

        # Find unique sink name
        self.sink_name = 'layout_sink'
        self.sink_name = self.create_unique_node_name(self.sink_name)

        # Add temporary sink and set visited
        sink = TermNode(self.sink_name, False)
        self._added[self.sink_name] = 0
        self._running_neighbors[self.sink_name] = set()
        self._running_neighbors[self.sink_name].add(self.sink_name)
        tmpSinkLinks = list()
        for name in self._nodes_list:
            node = self._nodes[name]
            visited[node.name] = False
            if not node._out_links:
                linkName = node.name + '-sink'
                sinkLink = TermLink(linkName, node.name, self.sink_name)
                self._links.append(sinkLink)
                node.add_out_link(linkName)
                sink.add_in_link(linkName)
                tmpSinkLinks.append(sinkLink)
                self._link_dict[linkName] = sinkLink
                self._running_neighbors[self.sink_name].add(node.name)
                self._running_neighbors[node.name].add(self.sink_name)

        # Add sink to self._nodes after so we don't create a sink link to
        # itself
        self._nodes[self.sink_name] = sink
        self._nodes_list.append(self.sink_name)

        # Setup grid
        self.grid.append([])
        self.grid[-1].append(sink)

        # Initial heuristic for row order 
        visited = dict()
        for name in self._nodes:
            visited[name] = False
        self.initCross(source.name, visited, embedding, 1)

        # Get node degrees based on original data plus added link
        # to match original Tulip algorithm
        degrees = self.createFakeDegrees()

        # Set the embedding of each row based on the initial crossing order
        for a, row in enumerate(self.grid):
            row = sorted(row, key = lambda x : embedding[x.name])
            for i, node in enumerate(row):
                embedding[node.name] = i
            self.grid[a] = row

        # Iterate through two-layer crossing reduction
        maxRank = len(self.grid) - 1
        for q in range(self.num_sweeps):
            # Up Sweep
            for i in range(maxRank, -1, -1):
                self.reduceTwoLayerCrossings(embedding, i, True, degrees)

            # Down Sweep
            for i in range(maxRank + 1):
                self.reduceTwoLayerCrossings(embedding, i, False, degrees)


        # Set final embedding based on leftover order
        for a, row in enumerate(self.grid):
            sorted_row = sorted(row, key = lambda x : embedding[x.name])
            for i, node in enumerate(sorted_row):
                embedding[node.name] = i

        # Remove the added sink
        for link in tmpSinkLinks:
            self._nodes[link.source]._out_links.remove(link.id)
            self._links.remove(link)
        del self._nodes[sink.name]
        self._nodes_list.remove(self.sink_name)


    def reduceTwoLayerCrossings(self, embedding, layer, isUp, degrees):
        """Modify the embedding of each node in a row based on its neighbor
           embedding values.

           @param embedding: dictionary of node embedding values
           @param layer: the row to re-calculate
           @param isUp: True if layer should be modified based on its below
                        neighbor row. NOTE: This is not used, instead this
                        function calculates based on both neighbor rows.
                        This is the way it is implemented in Tulip 4.9.0
                        so I have left it the same.
           @param degrees: dictionary keeping track of degrees of each node
        """
        row = self.grid[layer]
        for node in row:
            mySum = embedding[node.name]
            degree = degrees[node.name] + self._added[node.name]

            # Add the embeddinmg value of all running neighbors, both
            # original and added
            for name in self._running_neighbors[node.name]:
                mySum += embedding[name]

            # Account for sink between twice its neighbor in tulip
            # It must be added twice
            if node.name == self.sink_name:
                mySum += embedding[self.sink_name]

            embedding[node.name] = mySum / float(degree + 1.0)


    def createFakeDegrees(self):
        """In the Tulip 4.9.0 version of this algorithm, the degrees used
           in the crossing reduction were based on the modified graph.
           This calculates those.
        """
        degrees = dict()
        for name in self._nodes_list:
            node = self._nodes[name]
            degree = len(node._out_links) + len(node._in_links)

            # The sink has two extra degrees as it has a self loop in Tulip
            if name == self.sink_name:
                degree += 2

            degrees[name] = degree
        return degrees


    def setRanks(self, source):
        """Determine rank (level) value of each node.

           @param source: source node of graph
           @return the maximum rank assigned
        """
        import collections
        source.rank = 0
        current = collections.deque([source])
        marks = dict()
        maxRank = 0

        while current:
            node = current.popleft()
            nextrank = node.rank + 1
            for linkid in node._out_links:
                link = self._link_dict[linkid]
                neighbor = self._nodes[link.sink]
                if link.sink not in marks:
                    marks[link.sink] = len(neighbor._in_links)
                marks[link.sink] -= 1
                if marks[link.sink] == 0:
                    neighbor.rank = nextrank
                    if nextrank > maxRank:
                        maxRank = nextrank
                    current.append(neighbor)

        return maxRank


    def makeProper(self, source):
        """Add placer nodes along multi-rank edges.

           To match the Tulip 4.9.0 implementation, this does not actually
           create a placer node at every rank along a link. Instead, it adds a
           maximum of placer nodes when a link spans several ranks. It adds
           one right after the source and right after the sink. Note that the
           before the sink may get shifted as its true rank is not one before
           the sink.

           @param source: source node of graph
        """
        toAppend = list()
        for link in self._links:
            link.children = []
            start = self._nodes[link.source]
            end = self._nodes[link.sink]
            startRank = start.rank
            endRank = end.rank

            nameBase = start.name + '-' + end.name

            delta = endRank - startRank
            if delta > 1:
                self._added[start.name] += 1
                self._added[end.name] += 1
                self._modified_links.add(link.id)
                end._in_links.remove(link.id)
                atRank = startRank + 1
                newName = nameBase + '-1' #+ str(atRank)
                newNode = TermNode(newName, False)
                newNode.rank = atRank
                self._nodes[newName] = newNode
                self._nodes_list.append(newName)
                self._added[newName] = 0
                self._running_neighbors[newName] = set()
                self._running_neighbors[start.name].add(newName)
                self._running_neighbors[newName].add(start.name)

                link.sink = newName
                newNode.add_in_link(link.id)
                newLinkName = str(link.id) + '-1' #+ str(atRank)
                newLink = TermLink(newLinkName, newName, end.name)
                newNode.add_out_link(newLink.id)
                link.children.append(newLink)
                toAppend.append(newLink)
                self._link_dict[newLinkName] = newLink
                self.grid[atRank].append(newNode)

                if delta > 2:
                    atRank = endRank - 1
                    secondName = nameBase + '-2' #+ str(atRank)
                    secondNode = TermNode(secondName, False)
                    secondNode.rank = atRank
                    self._nodes[secondName] = secondNode
                    self._nodes_list.append(secondName)
                    self._added[secondName] = 0
                    self._running_neighbors[secondName] = set()
                    self._running_neighbors[secondName].add(newName)
                    self._running_neighbors[newName].add(secondName)
                    self._running_neighbors[end.name].add(secondName)
                    self._running_neighbors[secondName].add(end.name)

                    newLink.sink = secondName
                    newLink._edgeLength = delta - 2
                    secondNode.add_in_link(newLink.id)
                    secondLinkName = str(link.id) + '-2'# + str(atRank)
                    secondLink = TermLink(secondLinkName, secondName, end.name)
                    secondNode.add_out_link(secondLink.id)
                    link.children.append(secondLink)
                    toAppend.append(secondLink)
                    self._link_dict[secondLinkName] = secondLink
                    end.add_in_link(secondLink.id)
                    self.grid[startRank + 2].append(secondNode)
                else:
                    end.add_in_link(newLink.id)
                    self._running_neighbors[end.name].add(newName)
                    self._running_neighbors[newName].add(end.name)

        # Add all the new links
        for link in toAppend:
            self._links.append(link)


    def printNodeCoords(self):
        print("Current node coordinates:")
        for name, node in self._nodes.items():
            print(name, self.get_node_coord(name))

    def printEdgeCoords(self):
        print("Current edge coordinates:")
        for link in self._original_links:
            print(link.source, link.sink, link.segments)


    def create_unique_node_name(self, stub):
        """Create a unique node name from the given stub.

           @param stub: the initial trial name
           @return a unique name in the graph (string)
        """
        if stub in self._nodes:
            i = 0
            trial_name = stub + str(i)
            while trial_name in self._nodes:
                i += 1
                trial_name = stub + str(i)
            stub = trial_name

        return stub


    def create_single_source(self):
        """Add single source to DAG."""
        sources = list()
        for node in self._nodes.values():
            if not node._in_links:
                sources.append(node)

        # Find unique source name
        source_name = sources[0].name + '_layout_source'
        source_name = self.create_unique_node_name(source_name)

        # Add source node
        source = TermNode(source_name, False)
        self._nodes[source_name] = source
        self._nodes_list.append(source_name)
        self._added[source_name] = 0
        self._running_neighbors[source_name] = set()
        for i, node in enumerate(sources):
            linkName = source_name + '-' + str(i)
            link = TermLink(linkName, source_name, node.name)
            source.add_out_link(linkName)
            node.add_in_link(linkName)
            self._links.append(link)
            self._link_dict[linkName] = link
            self._running_neighbors[source_name].add(node.name)
            self._running_neighbors[node.name].add(source_name)
        return source


    def has_cycles(self):
        """Check if graph has cycles.

           @return True if graph has cycles.
        """
        seen = set()
        stack = set()
        self.single_source_tree = True
        source_count = 0
        for node in self._nodes.values():
            if not node._in_links:
                source_count += 1
                if self.cycles_from(node, seen, stack):
                    self.single_source_tree = False
                    return True
            elif len(node._in_links) > 1:
                self.single_source_tree = False
        if source_count > 1:
            self.single_source_tree = False
        return False


    def cycles_from(self, node, seen, stack):
        """Helper function for cycle check. This also does the tree check.

           @param node: TermNode currently being checked
           @param seen: Set of nodes already seen / visited
           @param stack: stack of nodes currently being checked
           @return True when cycle is detected.
        """
        seen.add(node.name)
        stack.add(node.name)

        if node.name not in seen:
            for linkid in node._out_links:
                link = self._link_dict[linkid]
                sink = self._nodes[link.sink]
                if link.sink not in seen:
                    if self.cycles_from(sink, seen, stack):
                        return True
                elif link.sink in stack:
                    # Each node should have been seen only once if there
                    # is a single source. Otherwise when we add a single
                    # source, it will no longer be a tree.
                    self.single_source_tree = False
                    return True

        stack.remove(node.name)
        return False



def termdag_interactive_helper(stdscr, graph):
    """Function for curses wrapper.

       @param stdscr: curses window
       @param graph: TermDAG to be shown in curses window
    """
    curses.start_color()
    can_color = curses.has_colors()
    curses.use_default_colors()
    graph.maxcolor = curses.COLORS
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
        curses.init_pair(i + 1 + curses.COLORS, 7, i)
    graph.print_interactive(stdscr, can_color)
