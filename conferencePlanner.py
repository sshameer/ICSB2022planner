class talk:
        
    
    def __init__(self,TalkTitle,SessionName,SpeakerList,day,start,end):
        import numpy as np
        self.title = TalkTitle
        self.session = SessionName
        self.speakers = SpeakerList
        self.day = day
        self.start = start 
        self.end = end
        if int(60*(self.start%1))<10:
            temp1 = "0"+str(int(60*(self.start%1)))
        else:
            temp1 = str(int(60*(self.start%1)))
        if int(60*(self.end%1))<10:
            temp2 = "0"+str(int(60*(self.end%1)))
        else:
            temp2 = str(int(60*(self.end%1)))
        self.timeslot = str(self.day)+"th "+str(int(np.floor(self.start)))+":"+temp1+" - "+str(int(np.floor(self.end)))+":"+temp2
    
    def __str__(self):
        return(str(self.timeslot)+": "+self.title+" - "+str(self.speakers).replace("[","").replace("]","").replace("'",""))

def createFromICSBFile(filename):
    talkList= list()
    fin = open(filename,encoding='utf8')
    Daylines=dict()
    Daylines[8] = list()
    Daylines[9] = list()
    Daylines[10] = list()
    Daylines[11] = list()
    Daylines[12] = list()
    Day8flag = False
    Day9flag = False
    Day10flag = False
    Day11flag = False
    Day12flag = False
    missed = list()
    for line in fin:
        if "Day 8" in line:
            Day8flag = True
            Day9flag = False
            Day10flag = False
            Day11flag = False
            Day12flag = False
            continue
        elif "Day 9" in line:
            Day8flag = False
            Day9flag = True
            Day10flag = False
            Day11flag = False
            Day12flag = False
            continue
        elif "Day 10" in line:
            Day8flag = False
            Day9flag = False
            Day10flag = True
            Day11flag = False
            Day12flag = False
            continue
        elif "Day 11" in line:
            Day8flag = False
            Day9flag = False
            Day10flag = False
            Day11flag = True
            Day12flag = False
            continue
        elif "Day 12" in line:
            Day8flag = False
            Day9flag = False
            Day10flag = False
            Day11flag = False
            Day12flag = True
            continue
        line = line.replace("\n","")
        if Day8flag:
            Daylines[8].append(line)
        elif Day9flag:
            Daylines[9].append(line)
        elif Day10flag:
            Daylines[10].append(line)
        elif Day11flag:
            Daylines[11].append(line)
        elif Day12flag:
            Daylines[12].append(line)
        else:
            missed.append(lines)
#     print(Day9lines)

    for Day in range(8,13):
        i = 0
        time=""
        for line in Daylines[Day]:
    #         print(line)
            if len(line) < 15 and "Session" in line:
                Session = Daylines[Day][i]+Daylines[Day][i+1]
#                 print(Day)
#                 print(Session)
            if len(line) == 11 and line[2]==":" and line[5]=="-" and line[8]==":":
                if time!="":
                    temp = "".join(Daylines[Day][noted+2:i])
                    if temp[len(temp)-1]==".":
                        temp = temp[:len(temp)-1]
                    Talktitle = temp.split(".")[len(temp.split("."))-1]
                    Speakers = "".join(Daylines[Day][noted+2:i]).replace("".join(Daylines[Day][noted+2:i]).split(".")[len("".join(Daylines[Day][noted+2:i]).split("."))-1],"")
                    if Talktitle == "":
                        print("".join(Daylines[Day][noted+2:i]))
                        print(Talktitle)
    #                 print(Speakers)
                    t = talk(Talktitle,Session,Speakers.replace("and",",").split(","),Day,int(time.split("-")[0].split(":")[0])+(int(time.split("-")[0].split(":")[1])/60),int(time.split("-")[1].split(":")[0])+(int(time.split("-")[1].split(":")[1])/60))
#                     print(t)
                    talkList.append(t)
                time = line
                noted = i
    #             print(time)
            i=i+1
    return talkList

def generateGraph(talkList):
    graph = list()
    processed = set()
    for talk1 in talkList:
        processed.add(talk1)
        for talk2 in talkList:
            if talk2 in processed:
#                 print(talk2.title+" skipped")
                continue
            if (round(talk1.end - talk2.start,1) == 0) and (talk1.day == talk2.day):
#                 print(talk1)
                if talk2.title == " " or talk2.title == "":
                    print(talk2)
                    print(talk2.title)
                graph.append(talk1.title+" -> "+talk2.title)
    return graph

def retrieveTalkByTitle(talkList,title):
    results = list()
    for talk in talkList:
        if title in talk.title:
            results.append(talk)
    if len(results)>1:
        print("Multiple results, please be more specific")
        print(title)
#         for result in results:
#             print(result)
        return
    else:
        return results[0]

def addgraphWeightings(graph,talkList,preferences,moving_penalty=-10,session_preference_bonus=20):
    weightings = dict()
    for interaction in graph:
#         print(interaction)
        source = interaction.split(" -> ")[0]
        target = interaction.split(" -> ")[1]
        sourceTalk = retrieveTalkByTitle(talkList,source)
        targetTalk = retrieveTalkByTitle(talkList,target)
#         if "Regulation of Mammalian Iron Physiology Across Scales" in target:
#             print(source)
#             print(target)
#             print(targetTalk.title)
        if sourceTalk.session == targetTalk.session:
            weightings[interaction] = 1
        else:
            weightings[interaction] = moving_penalty
        for preference in preferences.keys():
            if target in preference:
#                 print(weightings[interaction])
                weightings[interaction] = weightings[interaction] + preferences[preference]
#                 print(weightings[interaction])
            if targetTalk.session in preferences:
#                 print(weightings[interaction])
                weightings[interaction] = weightings[interaction] + preferences[preference]
#                 print(weightings[interaction])
    return weightings

def findNextStep(weighted_graph,talkList,start,verbose=False):
    best_path=""
    best_score=0
    for interaction in weighted_graph.keys():
        if start+" ->" in interaction:
            if verbose:
                print("==========")
                print(interaction)
                print(weighted_graph[interaction])
                print(retrieveTalkByTitle(talkList,interaction.split(" -> ")[1]))
                print(best_score)
                print("=========")
            if weighted_graph[interaction]>best_score:
                best_path = interaction
    return best_path

def calculatePath(weighted_graph,talkList,start):
    path = list()
    total_path_score = 0
    source = start
    nextStep = None
    while nextStep!="":
        nextStep = findNextStep(weighted_graph,talkList,source)
        path.append(nextStep)
#         print(nextStep)
        if nextStep == "":
            break
        source = nextStep.split(" -> ")[1]
    return path

def generateInstructions(path,talkList):
    start = path[0].split(" -> ")[0]
    startTalk = retrieveTalkByTitle(talkList,start)
    print("You start in "+str(startTalk.session))
    i = 0
    for pathstep in path[:len(path)-2]:
        source = pathstep.split(" -> ")[0]
        sourceTalk = retrieveTalkByTitle(talkList,source)
        target = pathstep.split(" -> ")[1]
        targetTalk = retrieveTalkByTitle(talkList,target)
        if sourceTalk.session != targetTalk.session:
            print("Move to "+targetTalk.session+" by "+str(targetTalk.timeslot.split("th ")[1].split(" - ")[0])+" for talk titled \""+targetTalk.title+"\"")
    print("You end in "+str(targetTalk.session))