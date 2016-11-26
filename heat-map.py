def plot_heat_tree(heatmap_file, tree_file, output_file=None):
    '''
    Plot heatmap next to a tree. The order of the heatmap **MUST** be the same,
    as order of the leafs on the tree. The tree must be in the Newick format. If
    *output_file* is specified, then heat-tree will be rendered as a PNG, 
    otherwise interactive browser will pop-up with your heat-tree.
    
    Parameters
    ----------
    heatmap_file: str
        Path to the heatmap file. The first row must have '#Names' as first 
        element of the header. 
            e.g. #Names, A, B, C, D
                row1, 2, 4, 0, 4
                row2, 4, 6, 2, -1
                
    tree_file: str
        Path to the tree file in Newick format. The leaf node labels should 
        be the same as as row names in the heatmap file. E.g. row1, row2.
        
    output_file: str, optional
        If specified the heat-tree will be rendered in that file as a PNG image,
        otherwise interactive browser will pop-up. **N.B.** program will wait 
        for you to exit the browser before continuing.
    '''
    import numpy
    
    from ete2.treeview.faces import add_face_to_node
    from ete2 import ClusterTree, TreeStyle, AttrFace, ProfileFace
 

    # To operate with numbers efficiently
    
    # Loads tree and array
    t = ClusterTree(tree_file, heatmap_file)
    
    # nodes are linked to the array table
    array =  t.arraytable
    
    # Calculates some stats on the matrix. Needed to establish the color
    # gradients.
    matrix_dist = [i for r in xrange(len(array.matrix))\
                   for i in array.matrix[r] if numpy.isfinite(i)]
    matrix_max = numpy.max(matrix_dist)
    matrix_min = numpy.min(matrix_dist)
    matrix_avg = matrix_min+((matrix_max-matrix_min)/2)
    
    # Creates a profile face that will represent node's profile as a
    # heatmap
    profileFace  = ProfileFace(matrix_max, matrix_min, matrix_avg, 1000, 14, "heatmap",colorscheme=2)

    nameFace = AttrFace("name", fsize=8)
    # Creates my own layout function that uses previous faces
    def mylayout(node):
        # If node is a leaf
        if node.is_leaf():
            # And a line profile
            add_face_to_node(profileFace, node, 0, aligned=True)
            node.img_style["size"]=0
            add_face_to_node(nameFace, node, 1, aligned=True)
        
    # Use my layout to visualize the tree
    ts = TreeStyle()
    ts.layout_fn = mylayout
    t.show(tree_style=ts)


heatmap = 'heatmap.txt'
tree_file = 'eg.tree'
plot_heat_tree(heatmap, tree_file)
