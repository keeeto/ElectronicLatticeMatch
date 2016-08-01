ELS
====
** Tool for lattice matching of crystalline materials. **

Contents
---------

* LatticeMatch.py : script for matching lattice parameters of two .cif files.
* ElectronEnergies.dat : Data on IPs and EAs of > 100 semiconductors collated from various sources.
* scan_IP_EA.py : script for scanning band-offsets, based on Anderson's rule.
* SiteMatch.py : script for performing the site matching routines of lattice matched surfaces.
* surface_points.py : the information on the surface atomic coordinates for a selcted number of materials.

Requirements
-----------

The main language is Python 2.7 with Numpy, Scipy and Matplotlib.
The [Atomic Simulation Environment](https://wiki.fysik.dtu.dk/ase) 
(ASE) is required for some components, as is [spglib](http://atztogo.github.io/spglib). 

Usage
---------
The functions are all run through python scripts. Running `pyhton script.py -h` will produce information on running each script.

A full tutorial on the method and online interactive notebooks can be found [on the WMD github](https://github.com/WMD-group/SMACT_practical).

License and attribution
-----------
ELS Python code and original data tables are licensed under the GNU General Public License (GPL) v3.
 
References
------------
[Keith T Butler, Yu Kumagai, Fumiyasu Oba, Aron Walsh,
Screening procedure for structurally and electronically matched contact layers for high-performance solar cells: hybrid perovskites, * J. Mater. Chem. C* 2016](http://pubs.rsc.org/en/content/articlehtml/2016/tc/c5tc04091d)

[A. Zur, T.C. McGill "Lattice match: An application to heteroepitaxy" *J. Appl. Phys.* 1984](http://scitation.aip.org/content/aip/journal/jap/55/2/10.1063/1.333084)
