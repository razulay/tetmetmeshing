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
        nodes: a dictionary {i: [x, y, z]} with i the node number and [x, y, z] the node coordinates
        elements: a dictionary {e: [i, j]} with e the element number and [i, j] the node numbers involved in the element
    """

    if type == 'bcc':
        nodes = {1: [0, 0, 0], 2: [1, 0, 0], 3: [1, 1, 0], 4: [0, 1, 0], 5: [0.5, 0.5, 0.5], 6: [0, 0, 1], 7: [1, 0, 1], 8: [1, 1, 1], 9: [0, 1, 1]}
        elements = {1: [1, 2], 2: [2, 3], 3: [3, 4], 4: [4, 1], 5: [5, 1], 6: [5, 2], 7: [5, 3], 8: [5, 4], 9: [5, 6], 10: [5, 7], 11: [5, 8], 12: [5, 9], 13: [6, 7], 14: [7, 8], 15: [8, 9], 16: [9, 6], 17: [1, 6], 18: [2, 7], 19: [3, 8], 20: [4, 9]}
        logger.info('Unit cell successfully called')
    else:
        logger.error('[unitcell] Unit cell not implemented')

    return nodes, elements



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


def scaling(sc_valx, sc_valy, sc_valz, nodes):
    """
    Scales a volume by a given scaling factor along x, y and z

    Args: 
        sc_valx: scaling parameter along x
        sc_valy: scaling parameter along y
        sc_valz: scaling parameter along z

    Returns:
        sc_nodes: scaled nodes
    """
    sc_nodes = {}
    for nodenb, nodecoord in nodes.items(): 
        sc_coord = [sc_valx*nodecoord[0], sc_valy*nodecoord[1], sc_valz*nodecoord[2]]
        sc_nodes.update({nodenb: sc_coord})
    
    logger.info('[scaling] scaling by x: %s, y: %s, z: %s successful', sc_valx, sc_valy, sc_valz)

    return sc_nodes


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

    node_nb = 0
    for i in range(nx):
        mi = i+1
        for j in range(ny):
            mj = j+1
            for k in range(nz):
                mk = k+1

                aliases = {}
                cand_nodes = {}
                cand_elements = {}


                for unitnodenb, unitnodecoord in unitnodes.items(): 
                    cand_number = 0
                    cand_node = [unitnodecoord[0] + mi*pvectx, unitnodecoord[1] + mj*pvecty, unitnodecoord[2] + mk*pvectz]

                    for nodenb, nodecoord in nodes.items(): 
                        if are_nodes_equal(cand_node, nodecoord):
                            aliases.update({unitnodenb: nodenb})
                        else:
                            cand_number = node + 1
                            cand_nodes.update(len)

                    
                logger.debug('[create_volume] mi = %s, mj = %s and mk = %s aliases = %s', mi, mj, mk, aliases)

    return nodes


#------------------------------------------------------------------------


test_unitcell = unitcell('bcc')

test_nodes = test_unitcell[0]
logger.debug('test_nodes %s', test_nodes)

test_elements = test_unitcell[1]
logger.debug('test_elements %s', test_elements)

plotmesh(test_nodes, test_elements)

sc_test_nodes = scaling(0.2, 0.5, 0.2, test_nodes)

plotmesh(sc_test_nodes, test_elements)

test_volume = create_volume(test_nodes, test_elements, 1, 1, 1, 2, 1, 1)

logger.debug('test_volume %s', test_volume)