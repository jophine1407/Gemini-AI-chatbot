# with open("myfile.txt", "w") as f:
#     f.write("Hello!") creating a file
# file = open("myfile.txt", "w")

# file.write("Hello Python!")

# file.close() write data 
# file = open("myfile.txt", "a")

# file.write("\nWelcome to Python!")

# file.close() adding a data in existing data
# file = open("myfile.txt", "r")

# for line in file:
#     print(line)

# file.close() space vitu type panrathuku

file=open("myfile.txt","w")

file.write(" Hi my name is Jophine!")
file.write("\n I a curretly doing my internship")

file=open("myfile.txt","a")

file.write("\n My Mentor is Gokila mam")

 
file.close()
with open("myfile.txt", "r") as file:

    data = file.read()

    words = data.split()

    for word in words:
        print(word)
 with text (myfile.txt,r) 
 