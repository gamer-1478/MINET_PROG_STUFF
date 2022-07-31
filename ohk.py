import sys
sys.setrecursionlimit(600000000)
negative = []
lock = []
boost = False
boosted = ['A3', 'CR2']
key = False

paths = ['']

required = ['Fuel', 'Manual', 'Medication', 'Circuit', 'Food', 'Automatic Guns', 'Tools',
            'Antenna', 'Solar Panel', 'Space Sattelite']

graph = {
    "Start" : [("u", "S1"), ("r", "SR1")],
    "S1" : [("u", "S2"), ("d", "Start")],
    "S2" : [("u", "Food"), ("d", "S1")],
    "Food" : [("u", "F1"), ("b", "TD3"), ("d", "S2")],
    "F1" : [("u", "F2"), ("d", "Food")],
    "F2" : [("u", "F3"), ("d", "F1"), ("r", "FD1")],
    "F3" : [("u", "Antenna"), ("d", "F2")],
    "Antenna" : [("r", "A1"), ("d", "F3")],
    "A1" : [("r", "A2"), ("l", "Antenna")],
    "A2" : [("r", "A3"), ("l", "A1")],
    "A3" : [("r", "A4"), ("l", "A2")],
    "A4" : [("r", "A5"), ("l", "A3")],
    "A5" : [("r", "Automatic Guns"), ("l", "A4")],
    "Automatic Guns" : [("r", "AG1"), ("l", "A5"), ("d", "FU3"), ("b", "Tools")],
    "AG1" : [("r", "AG2"), ("l", "Automatic Guns")],
    "AG2" : [("r", "AG3"), ("l", "AG1")],
    "AG3" : [("r", "Solar Panel"), ("l", "AG2")],
    "Solar Panel" : [ ("r", "SPR1"),("d", "SPD"), ("l", "AG3")],
    "SPR1" : [ ("r", "SPR2"), ("l", "Solar Panel"),],
    "SPR2" : [ ("d", "KU"), ("l", "SPR1")],
    "KU" : [("u", "SPR2"), ("d", "Key")],
    "Key" : [("u", "KU"), ("d", "KD1"), ("l", "KL1")],
    "KD1" : [("u", "Key"), ("d", "KD2")],
    "KD2" : [("u", "KD1"), ("d", "KD3")],
    "KD3" : [("u", "KD2"), ("d", "KD4")],
    "KD4" : [("u", "KD3"), ("d", "Manual")],
    "Manual" : [("u", "KD4"), ("l", "M1")],
    "M1" : [("l", "M2"), ("r", "Manual")],
    "M2" : [("l", "M3"), ("r", "M1"), ("b", "Space satellite")],
    "M3" : [("l", "M4"), ("r", "M2")],
    "M4" : [("l", "M5"), ("r", "M3")],
    "M5" : [("l", "M6"), ("r", "M4")],
    "M6" : [("l", "Circuit"), ("r", "M5")],
    "Circuit" : [("l", "CL2"), ("r", "M6"), ("b", "Fuel")],
    "CL2" : [("l", "CL1"), ("r", "Circuit")],
    "CL1" : [("u", "X1"), ("r", "CL2"), ("d", "SR2")],
    "SR3" : [("u", "CL1"), ("l", "SR2")],
    "SR2" : [("l", "SR"), ("r", "SR3")],
    "SR1" : [("l", "Start"), ("r", "SR2")],
    "FD1" : [("l", "F2"), ("r", "FD2")],
    "FD2" : [("l", "FD1"), ("r", "Tools")],
    "Tools" : [("l", "FD2"), ("r", "TR1"), ("u", "TU1"), ("d", "TD1"), ("b", "Automatic Guns")],
    "TU1" : [("u", "A3"), ("D", "Tools")],
    "TR1" : [("r", "TR2"), ("l", "Tools")],
    "TR2" : [("r", "TR3"), ("l", "TR1")],
    "TR3" : [("r", "FU2"), ("l", "TR2")],
    "FU2" : [("r", "TR5"), ("l", "TR3")],
    "TR5" : [("r", "Medicine"), ("l", "FU2")],
    "FU3" : [("u", "Automatic"), ("d", "FU2")],
    "FU1" : [("u", "FU2"), ("d", "Fuel")],
    "Medicine" : [ ("r", "KL4"), ("d", "ME1"), ("l", "TR5")],
    "KL1" : [("l", "KL2"), ("r", "Key")],
    "KL2" : [("l", "KL3"), ("r", "KL1"), ("u", "SPD")],
    "KL3" : [("b", 'Space satelite'), ("r", "KL2"), ("l", "KL4") ],
    "KL4" : [ ("r", "KL3"), ("l", "Medicine")],
    "SPD" : [ ("d", "KL2"),("u", "Solar Panel")],
    "TD1" : [("u", "Tools"), ("d", "TD2")],
    "TD2" : [("u", "TD1"), ("d", "TD3"), ("r", "FL3")],
    "TD3" : [("u", "TD2"), ("d", "TD4"), ("b", "Food")],
    "TD4" : [("u", "TD3"), ("r", "X1")],
    "FL3" : [("l", "TD4"), ("r", "FL2")],
    "FL2" : [("l", "FL3"), ("r", "FL1")],
    "FL1" : [("l", "FL2"), ("r", "Fuel")],
    "Fuel" : [("l", "FL1"), ("r", "FR1"), ("u", "FU1"), ("b", "Circuit")],
    "FR1" : [("l", "Fuel"), ("r", "ME2")],
    "ME1" : [("u", "Medicine"), ("d", "ME2")],
    "ME2" : [("u", "ME1"), ("d", "ME3"), ("l", "FR1")],
    "ME3" : [("u", "ME2"), ("d", "ME4")],
    "ME4" : [("u", "ME3"), ("d", "ME5")],
    "ME5" : [("u", "ME4"), ("d", "M5")],
    "KD1" : [("u", "Key"), ("d", "KD2")],
    "KD2" : [("u", "KD1"), ("d", "KD3")],
    "KD3" : [("u", "KD2"), ("d", "KD4")],
    "KD4" : [("u", "KD3"), ("d", "Manual")],
    "X1" : [("r", "X2"), ("l", "TD4")],
    "X2" : [("d", "CL1"), ("l", "X1")],
    "Space satelite" : [("b", "M2"), ("b", "KL3")]
}
last = [];
def traverseGraph(inv, path, cur):
    global boost;
    if(len(inv) == 10):
        print("Found a path: " + path)
        paths.append(path)
        return path
    if cur in negative:
        path = path+'-----'
    for i in graph[cur]:
        if i[1] in last:
            continue
        if i[1] in lock and not key:
            continue
        if i[0] == 'b' and not boost:
            continue
        if len(last) > 20:
            last.pop(0)
        if i[1] in boosted:
            boost = True
        if i[1] in required and i[1] not in inv:
            if (i[1] == 'Key'):
                key = True
            inv.append(i[1])
        print(last, i[1], inv)
        last.append(i[1])
        traverseGraph(inv, path+' '+i[1], i[1])


traverseGraph([], '', 'Start')

best = paths[0]

for i in paths:
    if len(best) > len(i):
        best = i

print((best))
