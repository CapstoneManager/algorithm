from pulp import *
import csv
import time
import json

minScore = 300
studentDict = {}
projectsDict = {}
combinations = []
fhand = open("output.csv","w+")

def writeToFile(elapsed_time, projects):
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0

    for p in projects:
        projectsDict[p] = 0

    # fhand = open("output.csv","w+")
    fhand.write(str(elapsed_time) + "\n")
    fhand.write("Total Cost " + str(minScore) + "\n")
    for key in studentDict.keys():
        line = key + "," + str(studentDict[key][0])+","+str(studentDict[key][1])
        projectsDict[studentDict[key][0]] = projectsDict[studentDict[key][0]]+1
        fhand.write(line)
        fhand.write("\n")


def checkCapacity(possible_projects, projMinCapacity, projMaxCapacity, students):
    for poss in possible_projects: 
        minc = 0
        maxc = 0
        for proj in poss:
            minc += projMinCapacity[proj]
            maxc += projMaxCapacity[proj]
        if (minc <= len(students) and maxc >= len(students)):
            combinations.append(list(poss))

    print("*************Length Checked Combinations*****************")
    print len(combinations)

def optimizeGroups(students, projects, projMinCapacity, projMaxCapacity, ranking):
    global minScore
    global studentDict
    
    flow = [(s, p) for s in students for p in projects]
    vars = LpVariable.dicts("Flow",(students,projects), 0, 1, LpInteger)

    assignment_model = pulp.LpProblem("Student Project Assignment Model", pulp.LpMinimize)
    assignment_model += lpSum([vars[s][p]*ranking[s][p] for (s, p) in flow]), "Sum_of_Assignment_Costs"
  
    for s in students:
        assignment_model += lpSum(vars[s][p] for p in projects) == 1, "One_Student_Per_Project_Only%s"%s

    max_capacity_constraint = {}
    for p in projects:
        constraint = lpSum([vars[s][p] for s in students]) <= projMaxCapacity[p]
        assignment_model += constraint, "Maximum_Project_Capacity_Constraint%s"%p
        max_capacity_constraint[p] = constraint

    min_capacity_constraint = {}
    for p in projects:
        constraint = lpSum([vars[s][p] for s in students]) >= projMinCapacity[p]
        assignment_model += constraint, "Minimum Project Capacity Constraint%s"%p
        min_capacity_constraint[p] = constraint

    assignment_model.solve()
   
    if LpStatus[assignment_model.status] == "Optimal":
        if value(assignment_model.objective) < minScore:
            minScore = value(assignment_model.objective)
           
            print("Total Cost: ", value(assignment_model.objective))
            for v in assignment_model.variables():
                if v.varValue == 1.0:
                    student = v.name.split("_")[1]
                    project = v.name.split("_")[2]
                    studentDict[student] = (project, ranking[student][project])
       
                
def flow(students, projects, projMinCapacity, projMaxCapacity, ranking):
    start_time = time.time()
    capacities = [0] * len(projects)
    for r in ranking:
        for p in range(len(r)):
            if r[p] < 4:
                capacities[p] += 1
    print capacities

    ranking = makeDict([students, projects], ranking, 0)

    pkeys = projMinCapacity.keys()
    chosen = []
    for p in range(len(projects)):
        if capacities[p] >= projMinCapacity[projects[p]]:
            chosen.append(projects[p])
    print len(chosen)
    projects = chosen

    # generate all possible combinations
    for i in range(len(projects),14,-1):
        possible_projects = pulp.combination(projects, i)
        checkCapacity(possible_projects, projMinCapacity, projMaxCapacity, students)
        print len(combinations)
        for c in combinations:
            optimizeGroups(students, c, projMinCapacity, projMaxCapacity, ranking)
        print("***************ENDED OPTIMIZATION*****************")
        elapsed_time = time.time() - start_time

        writeToFile(elapsed_time, projects)
        optmized = []
        for key in projectsDict.keys():
            if projectsDict[key] != 0:
                optmized.append(key)
                # print key

        projects = optmized
        del combinations[:]
        # print len(combinations)

    return studentDict
