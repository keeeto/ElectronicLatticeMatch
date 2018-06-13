#### This script uses python3 ####

from Step1_find_junction_partners import input_float, input_int

print("")
print("Step3 uses the bapt package to generate band alignment plots from candidate junction partners identified with ELS")
print("Please ensure output files from Step1 and Step2 are in the current directory")
print("Before continuing, please follow installation steps for bapt found here: https://github.com/utf/bapt")
input("Press Enter to continue...\n")

print("We will now plot band alignments for your absorber using the minimum strain candidates identified in Step2")
print("This script will generate a config file for bapt called bapt_input.yaml based on the information you provide")
# Ask user for absorber layer info
ab_name = input("Please enter the name of your absorber: ")
ab_IP = input_float("Please enter the IP of your absorber again: ")
ab_Eg = input_float("Please enter the band gap of your absorber again: ")
ab_EA = ab_IP - ab_Eg
ab_type = input("Sorry I forgot, was your absorber p- or n-type? (Please enter p or n): ")
if ab_type == "p":
    CBO = input("Is this plot for a cliff or a spike offset? (enter cliff or spike): ")
# Determine output file name from Step1
if ab_type == "p" and CBO == "spike":
    Step1_file = "Step1_CBO_spike_partners.dat"
elif ab_type == "p" and CBO == "cliff":
    Step1_file = "Step1_CBO_cliff_partners.dat"
elif ab_type == "n":
    Step1_file = "Step1_VBO_cliff_partners.dat"
else:
    print("Sorry, looks like there's been a typo! Please start again :(")
# Determine output file names for all candidates from Step2
candidates = []
Step2_files = []
candidates_tot = input_int("How many candidate junction partners were you left with after Step2?: ")
for i in range(0, candidates_tot):
    candidates.append(input("Please enter the name of each candidate (one at a time): "))
for candidate in candidates:
    Step2_files.append("Step2_"+candidate+".dat")
print("We will now read in information on your junction partner candidates from output files Step1 and Step2 to generate your config file for bapt...")
print("(Just so you know, we take the termination of the candidate from Step2 with the minimum strain then average the x-, y- components when we compare the strain for different candidates)")
# Use a bash function (with os python lib? to check step1 and step2 files are in this dir?)


# For candidate junction partners read info directly from output files
# First take EA and IP for candidates list from Step1 output file (store in dictionary??)
# Then find min strain termination from step2 output files, average, add this to dictionary and use to generate hex code
# check strains output (3 components) with Keith + tidy format of step2 output?

# Store info as dictionary??? (called candidates)
# Find min strain, then calculate strain_weight=strain-min_strain, assign strain_colour (and add to dictionary) based on weight
# Use strain to assign colour gradients to plot (darkest for lowest strain, i.e. best candidate) for config file gradients
# Use list len to set id nums

# Set colour ids for junction partners based on strain list and total number of candidates to plot
# (set min of list as darkest colour and set this based on if absorber was n- or p-type)
# Hex colors: #FFFFFF = white, #000000 = black
# p-type red: red_start = #AD2020, red_end = #D18383
# n-type blue: blue_start = #2555A8, blue_end = #7896C9
# dictionary, candidates: 0=name, 1=EA, 2=IP, 3=strain, 4=id, 5=grad??
### LOOK FOR PYTHON LIBRARY THAT GENERATES HEX CODES???



# Starting to write config file for bapt based on user inputs
config_file = open("bapt_input.yaml", "w")
config_file.write("compounds:\n")
# Adding absorber info to top of compounds list in bapt config file
config_file.write("    - name: '"+str(ab_name)+"'\n")
config_file.write("      ea: "+str(ab_EA)+"\n")
config_file.write("      ip: "+str(ab_IP)+"\n")
config_file.write("      gradient: 0, 0"+"\n")
# Adding junction partners to bapt config file compounds (use len of candidates list to set id num)
#for item in candidates:
    #confile_file.write("    - name:  '"+str(candidates[0])+"'")
    #etc... gradient startting from 1,1


config_file.write("\n")
# Writing hex colors for gradients for each compound in bapt config file
config_file.write("gradients:\n")
# gradient for absorber
config_file.write("    - id: 0\n")
config_file.write("      start: '#FFFFFF'\n")

# Set id 0 to be red for p-type absorber or blue for n-type absorber, all subsequent ids for candidate junction partners
if ab_type == "p":
    config_file.write("      end: '#AD2020'\n")
elif ab_type == "n":
    config_file.write("      end: '#2555A8'\n")
else:
    print("Looks like you didn't enter n or p for your absorber conductivity type :( Please start again.")
# Adding hex colors for candidate junction partners (ids starting from 1)
#config_file.write("    - id: "+str(candidates[4])+"\n")
#config_file.write("      start: '#FFFFFF'\n")
#config_file.write("      end: '"+str(candidates[5])+"'\n")

config_file.write("\n")
# Settings at the end of bapt config file
config_file.write("settings:\n")
config_file.write("    name_colour: 'k'\n")
config_file.write("    fade_cb: True\n")
config_file.write("    show_ea: True\n")
config_file.write("    show_axis: True\n")

config_file.close()

print("")
print("Now just use bapt on the command line to generate your plot with the command: bapt --filename bapt_input.yaml")
print("This will generate a plot called alignment.pdf")
print("p-type absorbers are coloured red, n-type are coloured blue and the darker the colour of the candidate junction partner, the lower the strain.")
print("Enjoy!")
print("")
