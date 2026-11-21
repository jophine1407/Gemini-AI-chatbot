import json

student = {
    "name": "Jophine",
    "age": 20,
    "course": "IT"
}

data = json.dumps(student)

print(data)