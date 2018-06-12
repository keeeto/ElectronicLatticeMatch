# Ask Keith for e.g. matplotlib script for band alignment diagrams
# Or use: https://github.com/utf/bapt

# Modify this e.g. to have more ids for red and blue colours? - https://github.com/utf/bapt/blob/master/examples/gradients.yaml
print("Step3 uses Bapt to generate band alignment plots from candidate junction partners identified with ELS")
print("Before continuing, please follow installation steps found here: https://github.com/utf/bapt")
input("Press Enter to continue...\n")

print("We will now plot band alignments for your absorber using the minimum strain candidates identified in Step2.")
# Ask user if absorber was p- or n-type 
# (for colour coding plot red for p-type absorber with blue contacts, blue for n-type absorber with red contacts)
# Ask user for name of absorber, IP and Eg
# Ask user for total number of junction partner candidates
# Ask user for name of each junction partner and IP and EA from Step1 output file and min strain of candidate from Step2
# Use strain to assign colour gradient to plot, darker for lower strain?