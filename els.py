import ase.build.general_surface as surface
import numpy as np
import math

def energy_align(ip_a, ea_a, window=0.6, gap=3.):
    '''
        A function to return band aligned contacts for electrons and holes. It can also check if contacts migh be semiconductors, based on their band gap.
	Args:
	    ip_a: The ionisation potential of the absorber layer.
	    ea_a: The electron affinity of the absorber layer.
   	    window: Double the maximim band offset allowed.
	    gap: The cutoff bandgap, above which the contact is considered insulating.
        Returns:
	    conducting_ETL: Electron withdrawing contact layers.
	    conducting_HTL: Hole withdrawing contact layers.
    '''

    f = open('CollatedData.txt','r')
    lines = f.readlines()
    f.close()

    HTL = []
    ETL = []
    conducting_ETL = []
    conducting_HTL = []

    for line in lines:
        inp = line.split()
        if inp[0] != "Species":
            Eg = float(inp[1])
            EA = float(inp[2])
            IP = float(inp[3])
            if Eg > 2.0:
                if EA >= ea_a - window * 0.5 and EA <= ea_a + window * 0.5:
                    ETL.append(inp[0])
                    if Eg < gap:
                        conducting_ETL.append(inp[0])
            if Eg > 2.0:
                if IP <= ip_a + window * 0.5 and IP >= ip_a - window * 0.5:
                    if Eg < gap:
                        conducting_HTL.append(inp[0])

    return conducting_ETL, conducting_HTL


# We need a class "pair" which contains the information about a matching interface pair
class Pair(object):
    """Class providing standard nformation on interface matching pairs."""

    def __init__(self, material1, material2, surface1, surface2, multiplicity1, multiplicity2, strains, max_vector,
                 area):
        """
        Attributes:
            Pair.material1 : name of first material
            Pair.material2 : name of second material
            Pair.surface1 : miller index of surface 1 Format: [1,1,1]
            Pair.surface2 : miller index of surface 2 Format: [1,1,1]
            Pair.multiplicity1 : multiplicity of u,v in surface1 Format: [1,1]
            Pair.multiplicity2 : multiplicity of u,v in surface2 Format: [1,1]
            Pair.strains : stains in u,v and gamma Format: [0.1,0.1,0.1]
                Pair.max_vector : the largest surface vector of the interface.
            Pair.area : the area of the smallest repeat unit of the interface
        """
        self.material1 = material1
        self.material2 = material2
        self.surface1 = surface1
        self.surface2 = surface2
        self.multiplicity1 = multiplicity1
        self.multiplicity2 = multiplicity2
        self.strains = strains
        self.max_vector = max_vector
        self.area = area

# Define some basic algebra
def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dotproduct(v, v))


def angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


# Define the tests as required by Fig 2 of Zur and McGill
def test1(a, b):
    if np.dot(a, b) < 0:
        return False
    else:
        return True


def test2(a, b):
    if np.linalg.norm(a) > np.linalg.norm(b):
        return False
    else:
        return True


def test3(a, b):
    if np.linalg.norm(b) > np.linalg.norm(b + a):
        return False
    else:
        return True


def test4(a, b):
    if np.linalg.norm(b) > np.linalg.norm(b - a):
        return False
    else:
        return True


# Switching of vectors as prescribed by Fig 2 of Zur and McGill
def cond1(a, b):
    if np.dot(a, b) < 0:
        b = -b
    return a, b


def cond2(a, b):
    if np.linalg.norm(a) > np.linalg.norm(b):
        c = b
        b = a
        a = c
        cond1(a, b)
    return a, b


def cond3(a, b):
    if np.linalg.norm(b) > np.linalg.norm(b + a):
        b = b + a
    return a, b


def cond4(a, b):
    if np.linalg.norm(b) > np.linalg.norm(b - a):
        b = b - a
    return a, b

def reduce_vectors(va, vb):
    '''Reduce the surface vectors to their minimal cell, as outlined in figure 2 of
    J. Appl. Phys. 55, 380 (1984)
    Args:
	va,vb: lists of real numbers/integers. Minimum length 2
    Returns:
	a,b: arrays of dimension (2x1). The reduced vectors

    '''
    a = np.asarray(va[0:2])
    b = np.asarray(vb[0:2])
    test_truth = 0  # A test that all 4 necessary conditions are met
    while test_truth < 4:
        a, b = cond1(a, b)
        a, b = cond2(a, b)
        a, b = cond3(a, b)
        a, b = cond4(a, b)
        truths = [test1(a, b), test2(a, b), test3(a, b), test4(a, b)]
        test_truth = sum(truths)

    return a, b


def surface_vectors(lattice, miller):
    ''' Given the xtal as defined with a (3x3) cell uses the ase surface module to cut the required surface.
	Args:
	    lattice : ase Atoms object
	    miller  : miller indices of the surface, a tuple of integers, length 3.
	Returns:
	    vectors[0/1] : the surface vectors (u,v), list of real numbers.
    '''
    surf = surface.surface(lattice, miller, layers=1)
    vectors = surf.cell[0:2]
    return vectors[0], vectors[1]


def surface_ratios(surface_a, surface_b, threshold=0.05, limit=5):
    ''' Given two surfaces a and b defined by vectors (u,v) tests to see if there is a ratio of r1/r2 which gives a lattice vector with mismatch less than the threshold.
	Args:
	    surfaces_ : the surface vectors and angle. A (3) tuple of real numbers.
	    threshold : the limit for lattice mismatch.
	    limit : the maximum number to multiply lattices by to obtain match.
	Returns:
	    exists : a bool of wheter the match was found
	    multiplicity : a list (1x2) with the integer values to multiply by.
    '''

    epitaxy = False
    u_satisfied = False
    v_satisfied = False
    angles_match = False

    super_a = (0, 0)
    super_b = (0, 0)
    strains = [0, 0, 0]
    max_strain = 0.
    all_strains = []  # A list of all strains within threshold, we can identify the lowest strain at the end
    # Ensure that the vector angles match (up to an arbitrary 180 degree rotation)
    if surface_a[2] - surface_b[2] <= 0.01:
        angles_match = True
        strains[2] = surface_a[2] - surface_b[2]

    # Run the test for the first lattice vector set
    if angles_match:
        for i in range(1, limit + 1):
            for j in range(1, limit + 1):
                r1 = float(i * surface_a[0])
                r2 = float(j * surface_b[0])
                strain = 2 * abs(r1 - r2) / (r1 + r2)
                if strain < threshold:
                    a = (i, j)
                    strains[0] = strain
                    for k in range(1, limit + 1):
                         for l in range(1, limit + 1):
                             r3 = float(k * surface_a[1])
                             r4 = float(l * surface_b[1])
                             strain = 2 * abs(r3 - r4) / (r3 + r4)
                             if strain < threshold:
                                b = (k, l)
                                v_satisfied = True
                                strains[1] = strain
                                super_a = (a[0], b[0])
                                super_b = (a[1], b[1])
                                epitaxy = True
                                mean_strain = np.average(strains)
                                if max_strain == 0:
                                    champion_strain = [max(strains), super_a, super_b, [strains[0], strains[1], strains[2]]]
                                    max_strain = mean_strain
                                elif mean_strain < max_strain - 0.001:
                                    champion_strain = [max(strains), super_a, super_b, [strains[0], strains[1], strains[2]]]
                                    max_strain = mean_strain



    if epitaxy:
        return epitaxy, champion_strain[1], champion_strain[2], champion_strain[3]
    else:
        return epitaxy, super_a, super_b, strains

def epitaxy_search(xtalA, index_a, xtalB, index_b, tolerance = 0.05, limit = 5):
    '''

        :param xtalA: The first crystal, ase Atoms object
        :param indexA: The miller index of the first crystal, [a,b,c]
        :param xtalB: The second crystal, ase Atoms object
        :param indexB: The miller index of the second crystal, [a,b,c]
        :param tolrance: The strain tolerance allowed, real number
        :param limit: maximum number of supercell expansions, interger
        :return:
    '''

    vec1, vec2 = surface_vectors(xtalA, index_a)
    r_vec1, r_vec2 = reduce_vectors(vec1, vec2)
    surface_vector_1 = (length(r_vec1), length(r_vec2), angle(r_vec1, r_vec2))

    vec1, vec2 = surface_vectors(xtalB, index_b)
    r_vec1, r_vec2 = reduce_vectors(vec1, vec2)
    surface_vector_2 = (length(r_vec1), length(r_vec2), angle(r_vec1, r_vec2))

    epitaxy, a, b, strains = surface_ratios(surface_vector_1, surface_vector_2, threshold=tolerance,
                                            limit=limit)

    return epitaxy, a, b, strains



