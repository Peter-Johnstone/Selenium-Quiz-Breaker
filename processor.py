# Open the input file and create an output file
with open("words.txt", "r") as infile, open("passwords.txt", "w") as outfile:
    for line in infile:
        # Split the line by tab and get the first word
        first_word = line.split("\t")[0]
        # Write the first word to the output file
        outfile.write(first_word + "\n")

print("First words extracted and saved to passwords.txt")
