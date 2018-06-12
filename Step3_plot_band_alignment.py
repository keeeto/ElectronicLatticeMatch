# Ask Keith for e.g. matplotlib script for band alignment diagrams
# Or use: https://github.com/utf/bapt

# Modify this e.g. to have more ids for red and blue colours? - https://github.com/utf/bapt/blob/master/examples/gradients.yaml
print("Step3 uses Bapt to generate band alignment plots from candidate junction partners identified with ELS")
print("Before continuing, please follow installation steps found here: https://github.com/utf/bapt")
input("Press Enter to continue...\n")

print("We will now plot band alignments for your absorber using the minimum strain candidates identified in Step2.")
print("This script will generate a config file for bapt called bapt_input.yaml based on the information you provide.")
# Ask user if absorber was p- or n-type 
# (for colour coding plot red for p-type absorber with blue contacts, blue for n-type absorber with red contacts)
# Ask user for name of absorber, IP and Eg
# Ask user for total number of junction partner candidates
# Ask user for name of each junction partner and IP and EA from Step1 output file and min strain of candidate from Step2
# Use strain to assign colour gradient to plot, darker for lower strain?
# Use above to generate config file for bapt like e.g. gradients.yaml, but set extra ids based on strain?

config_file = open("bapt_input.yaml", "w")
# Set id 0 to be red for p-type absorber or blue for n-type absorber

# Set colour ids for junction partners based on strain list (set min of list as darkest colour and set this based on if absorber was n- or p-type)

print("Now just use bapt on the command line to generate your plot with the command: bapt --filename bapt_input.yaml")
print("This will generate a plot called alignment.pdf")


config_file.close()