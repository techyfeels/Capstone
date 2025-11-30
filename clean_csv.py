import csv

SRC = "Most Streamed Spotify Songs 2024.csv"
DST = "Most Streamed Spotify Songs 2024_clean.csv"

with open(SRC, "r", encoding="utf-8", errors="ignore") as f_in, \
     open(DST, "w", encoding="utf-8", newline="") as f_out:
    
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    
    for row in reader:
        writer.writerow(row)

print("Done. File cleaned ->", DST)

