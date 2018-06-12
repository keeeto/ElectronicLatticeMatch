#### This script uses python3 ####

# Adapt below to loop nicely over user-inputted list of non-polar surface terminated for the absorber layer
# Then loop over all low index surfaces of candidate junction partners, allowing up to 10 unit cells to construct interface (limit) and strain tolerance of 4%

import els as els
import ase.io as io
from Step1_find_junction_partners import write_slow

def main():
    print("")
    print("Hello, this is Step2 for using ELS to find candidate heterojunction partners for your absorber material!")
    print("Please ensure you have a cif file for the bulk structure of your absorber material in this directory.")
    print("Please also add cif files for the bulk structures of all of your candidate junction partners from Step1 into a directory called candidates.")
    absorber_file = input("Please enter the name of the cif file for your absorber: ")
    miller1 = input("Please enter the Miller indices of your absorber one at a time: ")
    miller1 = int(miller1)
    miller2 = input("Next index: ")
    miller2 = int(miller2)
    miller3 = input("And the last index: ")
    miller3= int(miller3)
    candidate = input("Please enter the name of the candidate junction partner you want to screen by strain: ")
    candidate_cif_file = input("Now please enter the path to the cif file for this candidate from the current directory: ")
    tol = input("Please enter a tolerance for max. interface strain (or default of 0.04 for 4% will be used): ")
    if tol == "":
        tol = 0.04
    lim = input("Please enter an upper limit for the number of unit cells used to create the interface (otherwise a default of 10 will be used): ")
    if lim == "":
        lim = 10
    output_file = input("And lastly, please choose a name for the file containing your low-strain candidates: ")
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
                if not (m==0 and k ==0 and l == 0):
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
                        outputs.writelines(str(strains)+" ")
                        outputs.write("\n")

    outputs.close()

    print("Please check your output file.")

if __name__ == '__main__':
    main()