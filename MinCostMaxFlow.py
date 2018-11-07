from pulp import *
import csv
import time

minScore = 300
studentDict = {}

def optimizeGroups(students, projects, projMinCapacity, projMaxCapacity, ranking):
    global minScore
    
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
                    studentDict[student] = (project,ranking[student][project])
                
def flow(students, projects, projMinCapacity, projMaxCapacity, ranking):
    combinations = []

    start_time = time.time()
    ranking = makeDict([students, projects], ranking, 0)
   
    chosen = []
    for p in projects:
        if p != "P2P4Health" and p != "CosmicSystem" and p != "Perfit" and p != "EFormsProject" and p != "Quizzly":
            chosen.append(p)

    projects = chosen

    # generate all possible combinations\
    possible_projects = pulp.combination(projects, 22)
   
    for poss in possible_projects: 
        minc = 0
        maxc = 0
        combination = []
        for proj in poss:
            minc += projMinCapacity[proj]
            maxc += projMaxCapacity[proj]
        if (minc <= len(students) and maxc >= len(students)):
            combinations.append(list(poss))

    print("*************Length Checked Combinations*****************")

    for c in combinations:
        optimizeGroups(students, c, projMinCapacity, projMaxCapacity, ranking)
    print("***************ENDED OPTIMIZATION*****************")

    elapsed_time = time.time() - start_time

    fhand = open("output.csv","w+")
    fhand.write(str(elapsed_time) + "\n")
    fhand.write("Total Cost " + str(minScore) + "\n")
    for key in studentDict.keys():
        line = key + "," + str(studentDict[key][0])+","+str(studentDict[key][1])
        fhand.write(line)
        fhand.write("\n")
