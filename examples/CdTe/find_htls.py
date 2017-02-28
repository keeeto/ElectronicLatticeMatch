import els as els
import ase.io as io


ETL, HTL = els.energy_align(5.93, 4.23)
print "Hole contact layers: ", HTL

surfaces_A = [[1,0,0],[1,1,0]]
surfaces_B = [[1,0,0],[1,1,0]]

cdte = io.read("structures/CdTe.cif")
for material in HTL:
    xtalB = io.read("structures/%s.cif" % material)
    for a in surfaces_A:
        for b in surfaces_B:
            epitaxy, scA, scB, strains = els.epitaxy_search(cdte, a, xtalB, b, tolerance=0.03, limit=10)
            if epitaxy:
                print 'CdTe', material, scA, scB, strains
