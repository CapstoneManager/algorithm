import requests

students = ["Student1", "Student2", "Student3", "Student4", "Student5", "Student6", "Student7", "Student8"]

projects = ["Quizzly", "SummerCampReg", "Sigma"]

projMinCapacity = {"Quizzly":1, "SummerCampReg":2, "Sigma":3}

projMaxCapacity = {"Quizzly":8, "SummerCampReg":8, "Sigma":8,}

ranking = [ 
        [2, 3, 1],
        [3, 2, 1],
        [1, 2, 3],
        [2, 1, 3],
        [1, 2, 3],
        [1, 3, 2],
        [1, 2, 3],
        [3, 2, 1]
    ]

json = {
    "students": students,
    "projects": projects,
    "projMinCapacity": projMinCapacity,
    "projMaxCapacity": projMaxCapacity,
    "rankings": ranking,
}

requests.post('http://127.0.0.1:5000/algorithm', json=json)

