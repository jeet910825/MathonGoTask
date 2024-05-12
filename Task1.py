import re
import json
def convertToJson(text):
    #questionPattern to find questions
    results = []
    
    questionPattern = r"Question\s+ID:\s+[0-9]{6}.*\n*.*\n*[\\.\\(\\)\\A-D]*.*\n*[\\.\\(\\)\\A-D]*.*\n*[\\.\\(\\)\\A-D]*.*\n*[\\.\\(\\)\\A-D]*.*\n*.*\n*"
    solutionPattern = r"Sol.(.*?)"+re.escape("Question")
    answerPattern = r"Answer\s+..."
    
    answers = re.findall(answerPattern,text,re.DOTALL)
    
    for i in range(0,len(answers)):
        answers[i]=answers[i][-2]
    
    solutions = re.findall(solutionPattern,text,re.DOTALL)
    questions = re.findall(questionPattern,text)
    
    solutionIndex = 0
    answerIndex = 0
    
    count = 0
    answerMap = {"A":0,"B":1,"C":2,"D":3}
    
    for j in range(0,len(questions)):
        
        options = []
         
        question_id = re.findall("[0-9]{6}",questions[j])[0]
        
        question_text = re.findall("Question\s+ID:\s+[0-9]{6}.*\n*.*\n",questions[j])
        question_text = question_text[0].split("\n\n")[1]
        
        question_options  = re.findall("[//(]?[A-D][//)//.].+",questions[j])
        
        for i in range(0,len(question_options)):
            isCorrect = i == answerMap[answers[answerIndex]]
            options.append({"optionNumber":i,"optionText":question_options[i],"isCorrect": isCorrect})
            
        answerIndex += 1
        solutionText = ""
        if(count < len(solutions)):
            solutionText = solutions[count]
            count += 1
            
        results.append({"questionNumber":answerIndex,
                        
                        "questionId": question_id,
                        "questionText":question_text,
                        "options":[options],
                        "solutionText":solutionText
                        })
    return results
        


file = open('Task.txt','r')
text = file.read()

results = convertToJson(text)

with open('results.json', 'w') as json_file:
    json.dump(results, json_file, indent=2)