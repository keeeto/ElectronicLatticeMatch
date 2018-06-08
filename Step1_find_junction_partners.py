##########################################################################################################################################
# This script has been written for python3
#
# It uses the dataset from the ElectronLatticeMatch git repo to scan for candidate heterojunction partners for solar cell absorber layers
# This script corresponds to step 1: Electronic band offset matching
# Necessary inputs (i.e. data for absorber material): 
### Ionisation potential (IP)
### Band gap (Eg)
### Ideally knowledge of p-type or n-type conductivity (otherwise, run script for both cases) 
#
# Script and workflow by Suzanne K. Wallace
# Original git repo by Keith T. Butler found here: https://github.com/keeeto/ElectronicLatticeMatch
#
##########################################################################################################################################

import els as els
import sys
import time

# Function to write line of text letter by letter
def write_slow(text_line):
    for char in text_line:
        time.sleep(0.08)
        sys.stdout.flush()
        sys.stdout.write(char)
# Function to read user input as float (instead of default string)
def input_float(user_input):
    return float(input(user_input))


# Reading in user inputs required for matching of electronic bands of absorber to dataset of candidates junction partners
print("")
print("This script is Step1 for using ElectronLatticeMatch to search for candidate heterojunction partners for a solar cell absorber layer")
print("In this step, the ElectronLatticeMatch dataset is screened to find candidate materials based on the electronic band offsets with your absorber material")
print("If you use this setup in any publications, please cite DOI: 10.1039/C5TC04091D")
print("For original ElectronLatticeMatch git repo by Keith T. Butler, see here: https://github.com/keeeto/ElectronicLatticeMatch\n")
print("Let's look for some junction partners!")
input("Press Enter to continue...\n")

print("Please enter the ionisation potential (IP) of your absorber material")
IP = input_float("IP = ")
print("Please enter the band gap (Eg) of your absorber material")
Eg = input_float("Eg = ")
EA = IP - Eg
print("Is your absorber material p- or n-type? Enter either n or p.")
print("(If you're not sure, run this script for each case in turn)")
type = input("type = ")
print("")

# Scanning for cliff VBO (to establish junction) for p-type absorbers and then CBO (spike and cliff if e- m* is below threshold, otherwise cliff only)
if type == "p":
    print("You entered p-type for your absorber material\n")
    time.sleep(1.0)
    # Setup for VBO screening (to establish junction for p-type)
    print("We will first screen by the valence band offset (VBO)")
    print("This is to find a partner to your absorber where we would expect a built-in voltage to develop to separate photoexcited electron-hole pairs")
    print("To establish the built-in voltage we're looking for a cliff VBO to allow for majority carrier injection from the absorber into the partner (doi: 10.1016/S0040-6090(03)00583-2)")
    print("We're going to use 0.0 to 0.3 as our range, if you're happy to use the default values just press enter, otherwise set custom limits")
    VBO_lowlim = input("VBO lower limit = ")
    VBO_uplim = input("VBO upper limit = ")
    if VBO_lowlim == "":
        VBO_lowlim = 0.0
    if VBO_uplim == "":
        VBO_uplim = 0.3
    VBO_lowlim = float(VBO_lowlim)
    VBO_uplim = float(VBO_uplim)    
    # Setup for CBO screening (for transport of minority carriers across junction)
    print("")
    print("We will now screen by the conduction band offset (CBO)")
    print("This offset is important for the transport of photoexcited minority carrier electrons across the junction")  
    print("")
    input("Press Enter to continue...\n")
    print("Some studies have suggested that spike-like offsets give defect-tolerance heterojunctions (doi: 10.1063/1.4953820)") 
    time.sleep(1.0)
    print("But other studies have suggested that spike offsets provide too large of a barrier if minority carrier mobility is too low (doi: 10.1109/JPHOTOV.2017.2766522)")
    time.sleep(1.0)
    print("")
    print("We would advise also looking for a spike CBO if minority carrier effective mass is < 0.5 m_e\n")
    time.sleep(1.0)
    print("Would you like to also look for a spike CBO?\n")
    spike_check = input("Please type yes or no \n")
    if spike_check == "yes":
        print("Let's first look for a spike CBO for your absorber!")
        print("Please enter a lower and upper limit for your spike CBO, otherwise defaults of 0.1 and 0.4 eV will be used")
        print("0.1 to 0.3 eV has been suggested to be optimal for CdTe (doi: 10.1063/1.4953820)")
        CBO_spike_low = input("CBO spike lower limit = ")
        CBO_spike_up = input("CBO spike upper limit = ")
        if CBO_spike_low == "":
            CBO_spike_low = 0.1
        if CBO_spike_up == "":
            CBO_spike_up = 0.4
        CBO_spike_up = float(CBO_spike_up)
        CBO_spike_low = float(CBO_spike_low)
    print("")
    write_slow("Searching candidates for spike CBO in range "+str(CBO_spike_low)+" to "+str(CBO_spike_up)+" eV...\n")
 #   ETL = els.CBO_scan(EA, CBO_spike_low, CBO_spike_up, 3.0, output_file="CBO_spike_candidates.dat") 
 #   print(ETL)
    partners = els.CBOandVBO_scan(EA, IP, 3.0, CBO_spike_low, CBO_spike_up, VBO_lowlim, VBO_uplim, output_file="CBO_spike_partners.dat")
    print(partners)
    print("Your candidate junction partners are also listed in CBO_spike_partners.dat")
    print("")
    print("Let's look for a cliff CBO for your absorber!")
    print("Please enter a lower and upper limit for the CBO, otherwise default values of -0.3 and 0.0 eV will be used")
    print("(for a cliff CBO the lower limit should be negative and the upper limit should be zero or less)")
    CBO_lowlim = input("CBO lower limit = ")
    CBO_uplim = input("CBO upper limit = ")
    if CBO_lowlim == "":
        CBO_lowlim = -0.3
    if CBO_uplim == "":
        CBO_uplim = 0.0
    CBO_lowlim = float(CBO_lowlim)
    CBO_uplim = float(CBO_uplim)
    print("")
    write_slow("Searching for candidates for cliff CBO in range "+str(CBO_lowlim)+" to "+str(CBO_uplim)+" eV...\n")
 #   ETL = els.CBO_scan(EA, CBO_lowlim, CBO_uplim, 3.0, output_file="CBO_cliff_candidates.dat") 
 #   print(ETL)
    partners = els.CBOandVBO_scan(EA, IP, 3.0, CBO_lowlim, CBO_uplim, VBO_lowlim, VBO_uplim, output_file="CBO_cliff_partners.dat")
    print(partners)
    print("Your candidate junction partners are also listed in CBO_cliff_partners.dat")

# Scanning for cliff CBO to establish junction for n-type absorber and then VBO cliff offset only
elif type =="n":
    print("You entered n-type for your absorber material\n")
    time.sleep(1.0)

    # Setup for CBO screening (to establish junction for n-type)
    print("We will first screen by the conduction band offset (CBO)")
    print("This is to find a partner to your absorber where we would expect a built-in voltage to develop to separate photoexcited electron-hole pairs")
    print("To establish the built-in voltage we're looking for a cliff CBO to allow for majority carrier injection from the absorber into the partner (doi: 10.1016/S0040-6090(03)00583-2)")
    print("We're going to use -0.3 to 0.0 as our range, if you're happy to use the default values just press enter, otherwise set custom limits")
    CBO_lowlim = input("CBO lower limit = ")
    CBO_uplim = input("CBO upper limit = ")
    if CBO_lowlim == "":
        CBO_lowlim = -0.3
    if CBO_uplim == "":
        CBO_uplim = 0.0
    CBO_lowlim = float(CBO_lowlim)
    CBO_uplim = float(CBO_uplim)    
    # Setup for VBO screening (for transport of minority carriers across junction)
    print("We will now screen by the valence band offset (VBO)")
    print("This offset is important for the transport of photoexcited minority carrier holes across the junction")
    print("Please enter a lower and upper limit for the VBO, otherwise default values of 0 and 0.3 eV will be used")
    print("(for a cliff VBO the lower limit should be 0 or larger and the upper limit should be positive)")
    VBO_lowlim = input("VBO lower limit = ")
    VBO_uplim = input("VBO upper limit = ")
    if VBO_lowlim == "":
        VBO_lowlim = 0
    if VBO_uplim == "":
        VBO_uplim = 0.3
    VBO_lowlim = float(VBO_lowlim)
    VBO_uplim = float(VBO_uplim)
    print("")
    write_slow("Searching for candidates cliff VBO in range "+str(VBO_lowlim)+" to "+str(VBO_uplim)+" eV...\n")
 #   HTL = els.VBO_scan(IP, VBO_lowlim, VBO_uplim, 3.0, output_file="VBO_cliff_candidates.dat") 
 #   print(HTL)
    partners = els.CBOandVBO_scan(EA, IP, 3.0, CBO_lowlim, CBO_uplim, VBO_lowlim, VBO_uplim, output_file="VBO_cliff_partners.dat")
    print(partners)
    print("Your candidate junction partners are also listed in VBO_cliff_partners.dat")

else:
    print("Sorry. I think that was a typo. Please start again :(")


print("")
print("Now that you have your junction partner candidates...\n")
time.sleep(1.0)
print("")
print("Please find cif structure files for your candidates and move on to Step2 to find which junction partners should produce the least strain at the interface!\n")

