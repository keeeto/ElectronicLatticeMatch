

f = open('CollatedData.txt','r')
lines = f.readlines()
f.close()

HTL = []
ETL = []
conducting_ETL = []
conducting_HTL = []
scaffolding = []

for line in lines:
    inp = line.split()
    if inp[0] != "Species":
	Eg = float(inp[1])
	EA = float(inp[2])
	IP = float(inp[3])
	if Eg > 2.8:
	    if EA >= 3.9:
		ETL.append(inp[0])
		if Eg < 4.0:
		    conducting_ETL.append(inp[0])
	    if IP > 5.8 and EA < 3.9:
		scaffolding.append(inp[0])
        if IP <= 5.8:
	    if EA < 3.9:
       	        HTL.append(inp[0])
	        if Eg < 4.0:
		    conducting_HTL.append(inp[0])

print "Number of potential electron contacting layers: ", len(ETL)
print "Number of potential hole contacting layers: ", len(HTL)

print "Conductive electron contacting layers: "
print len(conducting_ETL)
print conducting_ETL
print "Conductive hole contacting layers: "
print len(conducting_HTL)
print conducting_HTL
print "Scaffolding layers"
print len(scaffolding)
print scaffolding

		
