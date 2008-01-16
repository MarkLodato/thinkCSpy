infile = open('alice_in_wonderland.txt', 'r')
outfile = open('alice_counts.dat', 'w')
text = infile.read()
counts = 128*[0]

for letter in text:
    counts[ord(letter)] += 1

outfile.write("%-12s%s\n" % ("Character", "Count"))
outfile.write("=================\n")

def display(i):
    if i == 10: return 'LF'
    if i == 13: return 'CR' 
    return chr(i)


for i in range(len(counts)):
    if counts[i]:
        outfile.write("%-12s%d\n" % (display(i), counts[i]))
