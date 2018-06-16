#### This script uses python3 ####

import els as els
import ase.io as io
from Step1_find_junction_partners import write_slow, input_int, input_float

def main():
    print("")
    print("Hello, this is Step2 for using ELS to find candidate heterojunction partners for your absorber material with minimal interface strain.")
    print("This step is based on methodology in doi: 10.1063/1.333084")
    print("Please ensure you have a cif file for the bulk structure of your absorber material in this directory.")
    print("Please also add cif files for the bulk structures of all of your candidate junction partners from Step1 into a directory called candidates.")
    absorber_file = input("Please enter the name of the cif file for your absorber: ")
    miller1 = input_int("Please enter the Miller indices of your absorber one at a time: ")
    miller2 = input_int("Next index: ")
    miller3 = input_int("And the last index: ")
    candidate = input("Please enter the name of the candidate junction partner you want to screen by strain: ")
    output_file = "Step2_"+str(candidate)+".dat"
    candidate_cif_file = input("Now please enter the path to the cif file for this candidate from the current directory: ")
    tol = input("Please enter a tolerance for max. interface strain (or default of 0.04 for 4% will be used): ")
    if tol == "":
        tol = 0.04
    tol = float(tol)
    lim = input("Please enter an upper limit for the number of unit cells used to create the interface (otherwise a default of 10 will be used): ")
    if lim == "":
        lim = 10
    lim = int(lim)
    print("")
    write_slow("Checking low index terminations of candidate junction partner (strain <= "+str(tol*100)+"%)...")
    print("")
    absorber = io.read(absorber_file)
    outputs = open(output_file, "w")
    outputs.write("junction partner, miller indices of partner, unit cells of absorber, unit cells of candidate partner, strains\n")

    # Need to figure out how to loop over candidate dirs or just ask user to input path??
    #candidate_cif = io.read('candidates/Ce2O3/MyBaseFileName_621711.cif')
    candidate_cif = io.read(candidate_cif_file)
    # Loop over all low index terminations for junction partner candidate
    for m in range(0,2):
        for k in range(0,2):
            for l in range(0,2):
                if not (m == 0 and k == 0 and l == 0):
                    epitaxy, sc_ab, sc_part, strains = els.epitaxy_search(absorber, [miller1, miller2, miller3], candidate_cif, [m, k, l], tolerance=tol, limit=lim)
                    if epitaxy:
                        outputs.write(candidate+" ")
                        outputs.write("(")
                        outputs.write(str(m))
                        outputs.write(str(k))
                        outputs.write(str(l))
                        outputs.write(") ")
                        outputs.writelines(str(sc_ab)+" ")
                        outputs.writelines(str(sc_part)+" ")
                        outputs.write(str(strains[0])+" ")
                        outputs.write(str(strains[1])+" ")
                        outputs.write(str(strains[2])+" ")
                        outputs.write("\n")

    outputs.close()

    print("")
    print("Terminations of the candidate junction partner with strain <="+str(tol*100)+"% when matched to your absorber have been written to "+str(output_file)+" (if any exist). Good luck!")

if __name__ == '__main__':
    main()