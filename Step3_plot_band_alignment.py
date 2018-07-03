#### This script uses python3 ####

from Step1_find_junction_partners import input_float, input_int, file_len
import os.path
import numpy as np

print("")
print("Step3 uses the bapt package to generate band alignment plots from candidate junction partners identified with els")
print("Please ensure output files from step1 and step2 are in the current directory")
print("Before continuing, please follow installation steps for bapt found here: https://github.com/utf/bapt\n")
print("If you make a typo and need to start again or just want to exit the script early, use 'ctrl-c'\n")
input("Press enter to continue...\n")

print("We will now plot band alignments for your absorber using the minimum strain candidates identified in step2")
print("This script will generate a config file for bapt called bapt_input.yaml based on the information you provide")
# Ask user for absorber layer info
ab_name = input("Please enter the name of your absorber: ")
ab_term = input("Please enter the surface termination of your absorber: ")
ab_eg = input_float("Please enter the band gap of your absorber again: ")
ab_ip = input_float("Please enter the IP of your absorber again: ")
ab_ea = ab_ip - ab_eg
ab_ea = '{0:.2f}'.format(ab_ea)
ab_type = input("Sorry I forgot, was your absorber p- or n-type? (please enter p or n): ")
offset = input("Is this plot for a cliff or a spike offset? (enter cliff or spike): ")
# determine output file name from step1
if ab_type == "p" and offset == "spike":
    step1_file = "Step1_CBO_spike_partners.dat"
elif ab_type == "p" and offset == "cliff":
    step1_file = "Step1_CBO_cliff_partners.dat"
elif ab_type == "n" and offset == "spike":
    step1_file = "Step1_VBO_spike_partners.dat"
elif ab_type == "n" and offset == "cliff":
    step1_file = "Step1_VBO_cliff_partners.dat"
else:
    print("Sorry, looks like there's been a typo! please start again :(")
# use python os lib to check step1 file is in this dir
if not os.path.isfile(step1_file):
    print("Uh oh, looks like you're missing the output file from step1!")
    print("Please add it to this directory and start again.")
# ask user for final candidates from step1 and step2
candidates = []
candidates_tot = input_int("How many candidate junction partners were you left with after step2?: ")
for i in range(0, candidates_tot):
     candidates.append(input("Please enter the name of each candidate (one at a time): "))
for candidate in candidates:
    step2_file = "Step2_"+candidate+".dat"
    # use python os lib to check step2 files are in this dir
    if not os.path.isfile(step2_file):
        print("Uh oh, looks like you're missing the output file from step2: "+step2_file)
        print("Please add it to this directory and start again.")
print("")
print("We will now read in information on your junction partner candidates from output files step1 and step2 to generate your config file for bapt...")
print("(just so you know, we take the termination of the candidate from step2 with the minimum strain then average the x-, y- components when we compare the strain for different candidates)")


# Storing final info on candidate junction partners to step3 file and writing to bapt config file
step3_file = open("step3_final_candidates.dat", "w")
step3_file.write("Candidate, Eg, EA,  IP, Min. strain terms.,  Av. strain\n")

# Count lines in Step1 output file to loop over
Step1_loop = file_len(step1_file)
# Reading in data from Step1
# [rows][cols] and col0=Candidate, col1=Eg, col2=EA, col3=IP, reading all in as str
step1_data = np.genfromtxt(step1_file, dtype='U', skip_header=1)
for candidate in candidates:
    # Loop over step1_file rows and set Eg, EA and Ip to write to step3_file
    for i in range(0,Step1_loop-1):
        if step1_data[i][0] == candidate:
           Eg_part = step1_data[i][1] 
           EA_part = step1_data[i][2] 
           IP_part = step1_data[i][3]  
    step2_file = "Step2_"+candidate+".dat"
    strain_data =np.genfromtxt(step2_file, dtype='U', skip_header=1)
    # Setting initial values for av_strain and min strain termination as first line of Step2 output file
    # Alternative read-in if more than two lines (2D array)
    if (file_len(step2_file) > 2 ):
        xstrain = float(strain_data[0][6])
        ystrain = float(strain_data[0][7])
        av_strain = (xstrain+ystrain)/2
        term_part = strain_data[0][1] 
        # Compare all subsequent lines to first to determine termination with min av strain
        # Only compare if there is more than termination option in Step2 output file (i.e more than 2 lines in file)
        for j in range(1,len(strain_data)):
            xstrain = float(strain_data[j][6])
            ystrain = float(strain_data[j][7])
            new_av_strain = (xstrain+ystrain)/2
            if new_av_strain < av_strain:
                av_strain = new_av_strain
                term_part = strain_data[j][1]
            if new_av_strain == av_strain:
                term_part = term_part+","+strain_data[j][1]
    # If only 1 option in Step2 output file
    elif (file_len(step2_file) == 2 ):
        xstrain = float(strain_data[6])
        ystrain = float(strain_data[7])
        av_strain = (xstrain+ystrain)/2
        term_part = strain_data[0][1] 
    else:
        print("Uh oh, error reading in the outputs from the Step2 output file for "+str(candidate))

    # Write info from Step1 and Step2 to new line of Step3 file
    step3_file.write(candidate+" "+Eg_part+" "+EA_part+" "+IP_part+" "+term_part+" "+str(av_strain)+"\n")
step3_file.close()

# starting to write config file for bapt based on user inputs
line_break = '\\n' #needed to do funky stuff for writing \n to config file
config_file = open("bapt_input.yaml", "w")
config_file.write("compounds:\n")
# adding absorber info to top of compounds list in bapt config file
config_file.write("    - name: \""+str(ab_name)+str(line_break)+str(ab_term)+ "\" \n")
config_file.write("      ea: "+str(ab_ea)+"\n")
config_file.write("      ip: "+str(ab_ip)+"\n")
config_file.write("      gradient: 0, 0"+"\n")

candidates_data = np.genfromtxt("Step3_final_candidates.dat", dtype='U', skip_header=1)
# First loop over step3 file to determine min strain candidate
min_strain = candidates_data[0][5] #Setting first strain as initial min val 
min_strain_candidate = candidates_data[0][0] 
for k in range(1, len(candidates_data)):
    if candidates_data[k][5] < min_strain:
        min_strain = candidates_data[k][5]
        min_strain_candidate = candidates_data[k][0] 
# Then loop over to write candidates to config file with all but min strain candidate set to fade mode
for k in range(0, len(candidates_data)):
    # Write info on junction partner candidates to bapt config compounds section
    config_file.write("    - name: "+candidates_data[k][0]+"\n")
    config_file.write("      ea: "+candidates_data[k][2]+"\n")
    config_file.write("      ip: "+candidates_data[k][3]+"\n")
    config_file.write("      gradient: 1, 1\n")
    if candidates_data[k][0] != min_strain_candidate:
        config_file.write("      fade: true\n")    


config_file.write("\n")
# writing hex colors for gradients for each compound in bapt config file
config_file.write("gradients:\n")
# gradient for absorber
config_file.write("    - id: 0\n")
config_file.write("      start: '#ffffff'\n")
# set id 0 to be red for p-type absorber or blue for n-type absorber and id 1 to be opposite for candidate junction partners
if ab_type == "p":
    config_file.write("      end: '#ad2020'\n")
    config_file.write("    - id: 1\n")
    config_file.write("      start: '#ffffff'\n")
    config_file.write("      end: '#2555a8'\n")
elif ab_type == "n":
    config_file.write("      end: '#2555a8'\n")
    config_file.write("    - id: 1\n")
    config_file.write("      start: '#ffffff'\n")
    config_file.write("      end: '#ad2020'\n")
else:
    print("Looks like you didn't enter n or p for your absorber conductivity type :( please start again.")
config_file.write("\n")
# settings at the end of bapt config file
config_file.write("settings:\n")
config_file.write("    name_colour: 'k'\n")
config_file.write("    fade_cb: true\n")
config_file.write("    show_ea: true\n")
config_file.write("    show_axis: true\n")

config_file.close()

print("")
print("Now just use bapt on the command line to generate your plot with the command: bapt --filename bapt_input.yaml")
print("")
print("This will generate a plot called alignment.pdf")
print("p-type absorbers are coloured red, n-type absorbers are coloured blue and the minimum strain candidate junction partner is the boldest colour.")
print("We've also summarised the info on the candidates from step1 and 2 into the file 'step3_final_candidates.dat")
print("Enjoy!")
print("")
