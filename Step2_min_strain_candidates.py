#### OLD SCRIPT ####

# Adapt below to loop nicely over user-inputted list of non-polar surface terminated for the absorber layer
# Then loop over all low index surfaces of candidate junction partners, allowing up to 10 unit cells to construct interface (limit) and strain tolerance of 4% 


import els as els
import ase.io as io

candidate = io.read('candidate_cifs/Ce2O3/MyBaseFileName_621711.cif')
CZTS = io.read('CZTS.cif')

epitaxy_1, scA_1, scB_1, strains_1 = els.epitaxy_search(CZTS, [1,0,0], candidate, [1,0,0], tolerance=0.04, limit=10)
print(epitaxy_1)

epitaxy_2, scA_2, scB_2, strains_2 = els.epitaxy_search(CZTS, [1,0,0], candidate, [1,1,0], tolerance=0.04, limit=10)
print(epitaxy_2)

epitaxy_3, scA_3, scB_3, strains_3 = els.epitaxy_search(CZTS, [1,0,0], candidate, [1,0,1], tolerance=0.04, limit=10)
print(epitaxy_3)

epitaxy_4, scA_4, scB_4, strains_4 = els.epitaxy_search(CZTS, [1,0,0], candidate, [0,0,1], tolerance=0.04, limit=10)
print(epitaxy_4)

epitaxy_5, scA_5, scB_5, strains_5 = els.epitaxy_search(CZTS, [1,0,0], candidate, [0,1,1], tolerance=0.04, limit=10)
print(epitaxy_5)

epitaxy_6, scA_6, scB_6, strains_6 = els.epitaxy_search(CZTS, [1,0,0], candidate, [1,1,1], tolerance=0.04, limit=10)
print(epitaxy_6)


# outputs for true
print(scA_1, scB_1, strains_1)
print(scA_2, scB_2, strains_2)
print(scA_3, scB_3, strains_3)
print(scA_4, scB_4, strains_4)
print(scA_5, scB_5, strains_5)
#print(scA_6, scB_6, strains_6)
