""" класс для удаления из mbox, text и прочих тэгов, внутри формул долларов, которые
прерывают формулы при их вытаскивании регуляркой для конвертера
"""

import re

reg_box = r"(\\[a-z]{0,1}box([\s\n]*?))[^\s\n]"
reg_framebox = r"(\\framebox([\s\n]*?))[^\s\n]"
reg_raisebox = r"(\\raisebox(?:\{.*?\}){0,1}(?:\[.*?\]){0,1}([\s\n]*?))[^\s\n]"
reg_text = r"(\\text[bfti]{0,2}([\s\n]*?))[^\s\na-zA-Z]"
reg_scriptsize = r"(\\scriptsize([\s\n]*?))[^\s\na-zA-Z]"

def correctionDollars(raw_file):
    raw_file = correctForREG(raw_file,reg_box)
    raw_file = correctForREG(raw_file,reg_framebox)
    raw_file = correctForREG(raw_file,reg_raisebox)
    raw_file = correctForREG(raw_file,reg_text)
    raw_file = correctForREG(raw_file,reg_scriptsize)
    return raw_file
 

def correctForREG(raw_file, reg_exp):
    toReplace = re.compile(reg_exp)
    res = toReplace.search(raw_file)     
    begin = 0
    #print(res)
    #обработка правильного скобочного выражения
    while (res is not None):
        #print(2, res.group(0))
        curr = begin + res.end()-2
        forReplace = res.group(1)      
        byReplace = res.group(1).strip();
        curr += 1
        ch = raw_file[curr]
        while(ch.isspace()):
            forReplace = forReplace + ch
            curr+=1
            ch = raw_file[curr]
        count = 0
        if ch != "{":
            raise Exception("Error: not found arguments for {}".format(forReplace+ch))
        else:
            count = 0;
            # число аргументов    
            num = 1
            tmp = ""
            while(num > 0):
                if curr >= len(raw_file):
                    raise Exception("Error in brackets equation in position \"{}\"".format(res.start))
                ch = raw_file[curr]
                forReplace = forReplace + ch
                if ch == "{":
                    if count == 0:
                        tmp = tmp+"{"
                    else:
                        tmp = tmp+"{"
                    count += 1
                elif ch == "}":
                    count -= 1
                    if count == 0:
                        tmp = tmp+"}"
                    else:
                        tmp = tmp+"}"
                elif ch == "$":
                    curr += 1
                    continue
                else:
                    tmp = tmp + ch
                #print(1, num, ch, count)       
                if count == 0 and ch == "}":
                        num -= 1
                elif count < 0:
                    raise Exception("Error in brackets equation in tag \"{}\"".format(match[1]))
                curr += 1
            curr -= 1
            #print(22, tmp)
            byReplace = byReplace+tmp
        for i in range(5):
            curr += 1
            if curr >= len(raw_file):
                break
            ch = raw_file[curr]
            forReplace += ch
            byReplace += ch
        #print(1, forReplace, byReplace);
        raw_file = raw_file.replace(forReplace,byReplace)
        toReplace = re.compile(reg_exp) 
        #???????????????????????????????????
        begin = begin + res.start()+1
        res = toReplace.search(raw_file[begin:])#??????????????????????????????????? 
   
    return raw_file

                    