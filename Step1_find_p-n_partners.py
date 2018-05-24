##########################################################################################################################################
# This script has been written for python3
#
# It uses the dataset from the ElectronLatticeMatch git repo to scan for candidate p-n heterojunction partners for solar cell absorber layers
# This script corresponds to step 1: Electronic band offset matching
#
# Script and workflow by Suzanne K. Wallace
# Original git repo found here: https://github.com/keeeto/ElectronicLatticeMatch
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
print("This script is step 1 for using ElectronLatticeMatch to search for candidate p-n heterojunction partners for a solar cell absorber layer")
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
print("We're now going to search through the ElectronLatticeMatch dataset to find candidate junction partners based on the electronic band offsets with your absorber material\n")
time.sleep(1.0)

# Scanning for CBO for p-type absorbers (spike and cliff if e- m* is below threshold, otherwise cliff only)
if type == "p":
    print("You entered p-type for your absorber material")
    print("Minority carriers are electrons, so we will match candidate junction partners to your absorber based on the CBO")
    print("")
    input("Press Enter to continue...\n")
    print("Some studies have suggested that spike-like offsets give defect-tolerance heterojunctions (doi: 10.1063/1.4953820)") 
    time.sleep(1.0)
    print("But other studies have suggested that spike offsets provide too large of a barrier in minority carrier mobility is too low (doi: 10.1109/JPHOTOV.2017.2766522)")
    time.sleep(1.0)
    print("")
    print("We would advise also looking for a spike CBO if minority carrier effective mass is < 0.5 m_e")
    time.sleep(1.0)
    print("Would you like to also look for a spike CBO?\n")
    spike_check = input("Please type yes or no ")
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
    write_slow("Searching candidates for spike CBO in range "+str(CBO_spike_low)+" to "+str(CBO_spike_up)+" eV...\n")
    ETL = els.CBO_scan(EA, CBO_spike_low, CBO_spike_up, 3.0, output_file="CBO_spike_candidates.dat") 
    print(ETL)

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
    write_slow("Searching for candidates for cliff CBO in range "+str(CBO_lowlim)+" to "+str(CBO_uplim)+" eV...\n")
    ETL = els.CBO_scan(EA, CBO_lowlim, CBO_uplim, 3.0, output_file="CBO_cliff_candidates.dat") 
    print(ETL)

# Scanning just for VBO cliff offsets if absorber is n-type
else:
    print("You entered n-type for your absorber material")
    print("Minority carriers are holes, so we will match candidate junction partners to your absorber based on the VBO")
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
    write_slow("Searching for candidates cliff VBO in range "+str(VBO_lowlim)+" to "+str(VBO_uplim)+" eV...\n")
    HTL = els.VBO_scan(IP, VBO_lowlim, VBO_uplim, 3.0, output_file="VBO_cliff_candidates.dat") 
    print(HTL)


# Old code, scanning for offsets
#ETL, HTL = els.energy_align(5.8, 4.3, window_up=0.4, window_down=-0.1, gap=3.0)
#print(ETL)


print("")
print("Now that you have your junction partner candidates...\n")
time.sleep(0.5)
print("")
print("Please find cif structure files for your candidates and move on to step 2 to find which junction partners should produce the least strain at the interface!\n")

