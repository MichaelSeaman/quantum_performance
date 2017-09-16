
import sys
from csv_to_tracklist import csv_to_tracklist

if len(sys.argv) <= 1:
    print("Input file needed.")
    sys.exit(0)
else:
    infile = sys.argv[1]

# run midi to csv


# csv rows to qsys
rows = open(CSV_FILE, encoding="latin-1").read().splitlines()

tracklist = csv_to_tracklist(rows)

# re-write csv
newCSV = rewrite_csv(CSV_FILE, tracklist)
write to NEW_CSV_FILENAME

#call Timidity
