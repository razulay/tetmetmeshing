import logging
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

#---------------------------------LOGGER---------------------------------
# Create a logger
logger = logging.getLogger('my_logger')

# Set the logging level
logger.setLevel(logging.DEBUG)

# Create a file handler to write log messages to a file
#file_handler = logging.FileHandler('my_log.log')

# Create a console handler to display log messages in the console
console_handler = logging.StreamHandler()

# Define a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Set the formatter for the handlers
#file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
#logger.addHandler(file_handler)
logger.addHandler(console_handler)

#------------------------------------------------------------------------


#-------------------------------FUNCTIONS--------------------------------

def unitcell(type):
    """
    Defines an elementary unit cell

    Args: 
        type: a string which indicates the name of the unit cell

    Returns:
        nodes: a dictionary {i: [x, y, z]} with i the node number and [x, y, z] the node coordinates inside the unit cell
        elements: a dictionary {e: [i, j]} with e the element number and [i, j] the node numbers involved in the element inside the unit cell
        pvect: a list of lists which is the 3D periodicity vectors of the unit cell
    """

    if type == 'bcc':
        nodes = {1: [0, 0, 0], 2: [1, 0, 0], 3: [1, 1, 0], 4: [0, 1, 0], 5: [0.5, 0.5, 0.5], 6: [0, 0, 1], 7: [1, 0, 1], 8: [1, 1, 1], 9: [0, 1, 1]}
        elements = {1: [1, 2], 2: [2, 3], 3: [3, 4], 4: [4, 1], 5: [5, 1], 6: [5, 2], 7: [5, 3], 8: [5, 4], 9: [5, 6], 10: [5, 7], 11: [5, 8], 12: [5, 9], 13: [6, 7], 14: [7, 8], 15: [8, 9], 16: [9, 6], 17: [1, 6], 18: [2, 7], 19: [3, 8], 20: [4, 9]}
        pvects = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        logger.info('Unit cell successfully called')

    elif type == 'cubic':
        nodes = {1: [0, 0, 0], 2: [1, 0, 0], 3: [1, 1, 0], 4: [0, 1, 0], 5: [0, 0, 1], 6: [1, 0, 1], 7: [1, 1, 1], 8: [0, 1, 1]}
        elements = {1: [1, 2], 2: [2, 3], 3: [3, 4], 4: [4, 1], 5: [5, 6], 6: [6, 7], 7: [7, 8], 8: [8, 5], 9: [1, 5], 10: [2, 6],  11: [3, 7], 12: [4, 8]}
        pvects = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        logger.info('Unit cell successfully called')

    elif type == 'fcc': #Also called octet truss
        nodes = {1: [0, 0, 0], 2: [1, 0, 0], 3: [1, 1, 0], 4: [0, 1, 0], 5: [0, 0, 1], 6: [1, 0, 1], 7: [1, 1, 1], 8: [0, 1, 1], 9: [0.5, 0.5, 0], 10: [0.5, 0.5, 1], 11: [0.5, 0, 0.5], 12: [0.5, 1, 0.5], 13: [0, 0.5, 0.5], 14: [1, 0.5, 0.5]}
        elements = {1: [9,1], 2: [9, 2], 3: [9, 3], 4: [9, 4], 5: [9, 14], 6: [9, 11], 7: [9, 12], 8: [9, 13], 9: [10, 5], 10: [10, 6], 11: [10, 7], 12: [10, 8], 13: [10, 11], 14: [10, 12], 15: [10, 13], 16: [10, 14], 17: [11, 1], 18: [11, 2], 19: [11, 5], 20: [11, 6], 21: [11, 14], 22: [11, 13], 23: [12, 8], 24: [12, 3], 25: [12, 4], 26: [12, 7], 27: [12, 14], 28: [12, 13], 29: [13, 5], 30: [13, 1], 31: [13, 4], 32: [13, 8], 33: [14, 2], 34: [14, 3], 35: [14, 6], 36: [14, 7]}
        pvects = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        logger.info('Unit cell successfully called')

    else:
        logger.error('[unitcell] Unit cell not implemented')

    return nodes, elements, pvects



def plotmesh(nodes, elements):
    """
    Plots the nodes and elements in an interactive 3D matplotlib graph

    Args: 
        nodes: a dictionary {i: [x, y, z]} with i the node number and [x, y, z] the node coordinates
        elements: a dictionary {e: [i, j]} with e the element number and [i, j] the node numbers involved in the element

    Returns:
        Interactive 3D matplotlib mesh of the nodes and elements
    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    
    for eltnb, eltnd in elements.items(): 
        x_values = [nodes[eltnd[0]][0], nodes[eltnd[1]][0]]
        y_values = [nodes[eltnd[0]][1], nodes[eltnd[1]][1]]
        z_values = [nodes[eltnd[0]][2], nodes[eltnd[1]][2]]
        ax.plot(x_values, y_values, z_values, 'b')

    #problem to solve with equal axis 
    plt.axis('equal')

    logger.info('[plotmesh] plot created')
    plt.show()


def unit_cell_scaling(sc_valx, sc_valy, sc_valz, unitnodes, unitelements, pvects):
    """
    Scales a volume by a given scaling factor along x, y and z

    Args: 
        sc_valx: scaling parameter along x
        sc_valy: scaling parameter along y
        sc_valz: scaling parameter along z
        unitnodes: a dict containing the nodes inside the unit cell
        unitelements: a dict containing the elements of the unit cell
        pvects: a list of lists 

    Returns:
        sc_nodes: scaled nodes
    """
    sc_unitnodes = {}
    sc_pvects = []
    for unitnodenb, unitnodecoord in unitnodes.items(): 
        sc_coord = [sc_valx*unitnodecoord[0], sc_valy*unitnodecoord[1], sc_valz*unitnodecoord[2]]
        sc_unitnodes.update({unitnodenb: sc_coord})

    for vect in pvects:
        sc_vect = [sc_valx*vect[0], sc_valy*vect[1], sc_valz*vect[2]]
        sc_pvects.append(sc_vect)
    
    logger.info('[scaling] scaling by x: %s, y: %s, z: %s successful', sc_valx, sc_valy, sc_valz)

    return sc_unitnodes, unitelements, sc_pvects


def are_nodes_equal(node1, node2, threshold=1e-6):
    """
    Check if two 3D points are equal within a specified threshold.

    Args:
        node1: list representing the first node coordinates (x, y, z).
        node2: list representing the second node coordinates (x, y, z).
        threshold: The maximum allowed difference for equality (default is 1e-6).

    Returns:
        True if the points are equal within the threshold, False otherwise.
    """

    if len(node1) != 3 or len(node2) != 3:
        raise ValueError("Points must be in the format [x, y, z]")

    distance = math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2 + (node1[2] - node2[2])**2)
    
    return distance < threshold


def are_elements_equal(element1, element2):
    """
    Check if two elements are equal.

    Args:
        element1: list representing the first element
        element2: list representing the second element

    Returns:
        True if the elements are equal. False otherwise.
    """
    if set(element1) == set(element2):
     return True
    
    else:
        return False


def create_volume(unitnodes, unitelements, pvectx, pvecty, pvectz, nx, ny, nz):
    """
    Creates a volume using a unit cell. No doubles in nodes or elements.

    Args:
        unitnodes: a dictionary {i: [x, y, z]} with i the node number and [x, y, z] the node coordinates or the unit cell
        unitelements: a dictionary {e: [i, j]} with e the element number and [i, j] the node numbers involved in the element of the unit cell
        pvectx: periodicity vector value in x direction
        pvecty: periodicity vector value in y direction
        pvectz: periodicity vector value in z direction
        nx: number of repeated cells in x direction
        ny: number of repeated cells in y direction
        nz: number of repeated cells in z direction

    Returns:
        nodes: a dictionary {i: [x, y, z]} with i the node number and [x, y, z] the node coordinates of the volume 
        elements: a dictionary {e: [i, j]} with e the element number and [i, j] the node numbers involved in the element of the volume
    """

    nodes = {}
    elements = {}
    logger.debug('[create-volume] len(nodes): %s', len(nodes))

    node_nb = 0
    for i in range(nx):
        mi = i
        logger.debug('[create-volume] mi: %s', mi)
        for j in range(ny):
            mj = j
            logger.debug('[create-volume] mj: %s', mj)
            for k in range(nz):
                mk = k
                logger.debug('[create-volume] mk: %s', mk)

                #Translate nodes from unit cell and identify which have aliases on the already existing nodes
                aliases = {}
                add_nodes = {}


                for unitnodenb, unitnodecoord in unitnodes.items(): 
                    #Translate node
                    add_node = [unitnodecoord[0] + mi*pvectx[0] + mj*pvecty[0] + mk*pvectz[0], unitnodecoord[1] + mi*pvectx[1] + mj*pvecty[1] + mk*pvectz[1], unitnodecoord[2] + mi*pvectx[2] + mj*pvecty[2] + mk*pvectz[2]]
                    logger.debug('[create-volume] {unitnodenb: add_node}: {%s: %s}', unitnodenb, add_node)
                    add_nodes.update({unitnodenb: add_node})

                    #Create aliases dictionary to change the node numbers and element numbers when concatenating the node list 
                    for nodenb, nodecoord in nodes.items(): 
                        #Check if it has an alias in the already constructed nodes, if yes, give the add_nodenb this alias
                        if are_nodes_equal(add_node, nodecoord):
                            aliases.update({unitnodenb: nodenb})




                #Initialise the next node number in the node dict
                next_nodenb = len(nodes)+1

                for add_nodenb, add_nodecoord in add_nodes.items(): 
                    #If the node number does not have an alias in the aliases dict, give it a new number not in nodenb
                    if add_nodenb not in aliases.keys(): 
                        aliases.update({add_nodenb: next_nodenb})
                        logger.debug('[create-volume] next_nodenb: %s', next_nodenb)
                    

                        next_nodenb = next_nodenb + 1

                logger.debug('[create-volume] aliases: %s', aliases)

                #Add the nodes to the node dict
                for add_nodenb, add_nodecoord in add_nodes.items(): 
                    nodes.update({aliases[add_nodenb]: add_nodecoord})
                logger.debug('[create-volume] nodes: %s', nodes)

                #Now the element list needs to use the aliases dict to create a list of elemets with the aliases as node numbers
                add_elements = {}
                for uniteltnb, unitelt in unitelements.items():
                    add_elements.update({uniteltnb: [aliases[unitelt[0]],aliases[unitelt[1]]]})
                
                logger.debug('[create-volume] add_elements: %s', add_elements)

                #Need to check element and add_element to see if there are any doubles

                add_elementstoremove = []

                for add_elementnb, add_element in add_elements.items():
                    for elementnb, element in elements.items():
                        if are_elements_equal(element, add_element) == True and add_element not in add_elementstoremove :
                            add_elementstoremove .append(set(add_element))
                
                logger.debug('[create_volume] add_elementstoremove : %s', add_elementstoremove )
                logger.debug('[create_volume] len(add_elementslist): %s', len(add_elementstoremove ))


                #Add elements without doubles to the list of elements
                #Initialise the next element number in the element dict 
                next_elementnb = len(elements)+1

                for add_elementnb, add_element in add_elements.items():
                    #If the element is not a double, give it a new number not in element number
                    if set(add_element) not in add_elementstoremove: 
                        elements.update({next_elementnb: add_element})
                        next_elementnb = next_elementnb + 1

                logger.debug('[create_volume] elements: %s', elements)


    return nodes, elements


def export_build(nodes, elements, path):
    """
    Exports the nodes and elements in the appropriate format for building at specified path

    Args:
        nodes: a dictionary {i: [x, y, z]} with i the node number and [x, y, z] the node coordinates or the unit cell
        elements: a dictionary {e: [i, j]} with e the element number and [i, j] the node numbers involved in the element of the unit cell
        path: path of file

    Returns:
        file in specified path
    """

    with open(path, "w") as file:
    for nodenb, nodecoord in nodes.items():
        file.write(f"{nodecoord},")

    file.write(f"\n")
    for elementnb, element in elements.items():
        file.write(f"{[element[0]-1, element[1]-1]},")


def export_mesh(nodes, elements, path):
    """
    Exports the nodes and elements at specified path

    Args:
        nodes: a dictionary {i: [x, y, z]} with i the node number and [x, y, z] the node coordinates or the unit cell
        elements: a dictionary {e: [i, j]} with e the element number and [i, j] the node numbers involved in the element of the unit cell
        path: path of file

    Returns:
        file in specified path
    """

    with open(path, "w") as file:
    file.write(f"Nodes: \n")
    for nodenb, nodecoord in nodes.items():
        file.write(f"{nodenb} {nodecoord} \n")

    file.write(f"`Elements`: \n")
    for elementnb, element in elements.items():
        file.write(f"{elementnb} {element} \n")


#------------------------------------------------------------------------


test_unitcell = unitcell('bcc')

test_nodes = test_unitcell[0]
logger.debug('test_nodes %s', test_nodes)

test_elements = test_unitcell[1]
logger.debug('test_elements %s', test_elements)

test_pvects = test_unitcell[2]
logger.debug('test_pvects %s', test_pvects)

plotmesh(test_nodes, test_elements)

sc_test_unitcell = unit_cell_scaling(16.66, 16.66, 16.66, test_nodes, test_elements, test_pvects)
sc_test_nodes = sc_test_unitcell[0]
logger.debug('sc_test_nodes %s', sc_test_nodes)

sc_test_elements = sc_test_unitcell[1]
logger.debug('sc_test_elements %s', sc_test_elements)

sc_test_pvects = sc_test_unitcell[2]
logger.debug('sc_test_pvects %s', sc_test_pvects)

plotmesh(sc_test_nodes, sc_test_elements)


test_volume = create_volume(test_nodes, test_elements, test_pvects[0], test_pvects[1], test_pvects[2], 3, 3, 3)

test_volume_nodes = test_volume[0]
test_volume_elements = test_volume[1]

plotmesh(test_volume_nodes, test_volume_elements)


sc_test_volume = create_volume(sc_test_nodes, sc_test_elements, sc_test_pvects[0], sc_test_pvects[1], sc_test_pvects[2], 3, 3, 3)

sc_test_volume_nodes = sc_test_volume[0]
sc_test_volume_elements = sc_test_volume[1]

plotmesh(sc_test_volume_nodes, sc_test_volume_elements)



