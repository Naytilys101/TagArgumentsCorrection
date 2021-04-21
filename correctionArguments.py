""" класс для обработки некоректно написанных тэгов, в которых опущены аргументы
"""

import re

reg_frac = r"(\\[cdt]{0,1}frac([\s\n]*?))[^\s\n]"
reg_underset = r"(\\underset([\s\n]*?))[^\s\n]"
reg_overset = r"(\\overset([\s\n]*?))[^\s\n]"
reg_overline = r"(\\overline([\s\n]*?))[^\s\n]"
reg_underline = r"(\\underline([\s\n]*?))[^\s\n]"
reg_tilde = r"(\\tilde([\s\n]*?))[^\s\n]"
reg_bar = r"(\\bar([\s\n]*?))[^\s\n]"
reg_big = r"(\\big([\s\n]*?))[^\s\n\w\\]"
reg_hat = r"(\\hat([\s\n]*?))[^\s\n]"
reg_binom = r"(\\[t]{0,1}binom([\s\n]*?))[^\s\n]"
reg_textbf = r"(\\textbf([\s\n]*?))[^\s\n]"
reg_texttt = r"(\\texttt([\s\n]*?))[^\s\n]"
reg_textit = r"(\\textit([\s\n]*?))[^\s\n]"
reg_text = r"(\\text([\s\n]*?))[^tbfi\s\n]"
reg_box = r"(\\[a-z]box([\s\n]*?))[^\s\n]"
reg_dot = r"(\\dot([\s\n]*?))[^\s\n]"
reg_tt = r"(\\tt([\s\n]*?))[^s\s\n]"
reg_bf = r"(\\bf([\s\n]*?))[^\s\n]"
reg_sc = r"(\\sc([\s\n]*?))[^r\s\n]"
reg_sf = r"(\\sf([\s\n]*?))[^\s\n]"
reg_sl = r"(\\sl([\s\n]*?))[^\s\n]"
reg_em = r"(\\em([\s\n]*?))[^\s\n]"


reg_out_tt = r"((?<!\{\{)[\s\n]*(\\tt\{.*?\}))"
reg_out_bf = r"((?<!\{\{)[\s\n]*(\\bf\{.*?\}))"
reg_out_sc = r"((?<!\{\{)[\s\n]*(\\sc\{.*?\}))"
reg_out_sf = r"((?<!\{\{)[\s\n]*(\\sf\{.*?\}))"
reg_out_sl = r"((?<!\{\{)[\s\n]*(\\sl\{.*?\}))"
reg_out_em = r"((?<!\{\{)[\s\n]*(\\em\{.*?\}))"
reg_out_pm = r"((?<!\{\{)[\s\n]*(\\pm))"
#reg_out_bfV2 = r"([^\{](\\bf\{.*?\}))"
def correctionArguments(raw_file):
    raw_file = correctForREG(raw_file,reg_frac, 2)
    raw_file = correctForREG(raw_file,reg_underset, 2)
    raw_file = correctForREG(raw_file,reg_overset, 2)
    raw_file = correctForREG(raw_file,reg_binom, 2)
    raw_file = correctForREG(raw_file,reg_overline, 1)
    raw_file = correctForREG(raw_file,reg_underline, 1)
    raw_file = correctForREG(raw_file,reg_tilde, 1)
    raw_file = correctForREG(raw_file,reg_bar, 1)
    raw_file = correctForREG(raw_file,reg_big, 1)
    raw_file = correctForREG(raw_file,reg_hat, 1)
    raw_file = correctForREG(raw_file,reg_textbf, 1)
    raw_file = correctForREG(raw_file,reg_texttt, 1)
    raw_file = correctForREG(raw_file,reg_textit, 1)
    raw_file = correctForREG(raw_file,reg_text, 1)
    raw_file = correctForREG(raw_file,reg_box, 1)
    raw_file = correctForREG(raw_file,reg_dot, 1)
    raw_file = correctForREG(raw_file,reg_tt, 1)
    raw_file = correctForREG(raw_file,reg_bf, 1)
    raw_file = correctForREG(raw_file,reg_sc, 1)
    raw_file = correctForREG(raw_file,reg_sf, 1)
    raw_file = correctForREG(raw_file,reg_sl, 1)
    #raw_file = correctForREG(raw_file,reg_em, 1)
    
    raw_file = correctOutsideArgs(raw_file, reg_out_tt)
    raw_file = correctOutsideArgs(raw_file, reg_out_bf)
    raw_file = correctOutsideArgs(raw_file, reg_out_sc)
    raw_file = correctOutsideArgs(raw_file, reg_out_sf)
    raw_file = correctOutsideArgs(raw_file, reg_out_sl)
    raw_file = correctOutsideArgs(raw_file, reg_out_em)
    raw_file = correctOutsideArgs(raw_file, reg_out_pm)
    return raw_file
    
def correctOutsideArgs(raw_file, reg_exp):
    matches = re.findall(reg_exp,raw_file)
    #print(matches)
    while (len(matches)>0):
        match = matches[0]
        #print(match)
        #две скобки, т.к. может быть аргументом внутри другого тэга
        #а конвертер на 1 скобках в таком случае падает
        byReplace = "{{"+match[1]+"}}"
        raw_file = raw_file.replace(match[1],byReplace)
        #print(raw_file)        
        matches = re.findall(reg_exp,raw_file)
    return raw_file

def correctForREG(raw_file, reg_exp, num_args):
    toReplace = re.compile(reg_exp)
    res = toReplace.search(raw_file)     
    begin = 0
    #print(toReplace, res)
    #обработка правильного скобочного выражения
    while (res is not None):
    
        curr = begin + res.end()-2
        forReplace = res.group(1)      
        byReplace = res.group(1).strip();
        for i in range(num_args):
            curr += 1
            ch = raw_file[curr]
            while(ch.isspace()):
                forReplace = forReplace + ch
                curr+=1
                ch = raw_file[curr]
            #print(0,forReplace, ch, i)
            if ch != "{":
                if ch != "\\" and ch !="$":
                    forReplace = forReplace + ch
                    byReplace = byReplace +"{"+ch+"}"
                elif ch == "$":
                    forReplace = forReplace + ch
                    byReplace = byReplace +"{"+ch
                    curr += 1
                    ch = raw_file[curr]
                    while(ch != "$"):
                        forReplace = forReplace+ch
                        byReplace = byReplace+ch
                        curr += 1
                        ch = raw_file[curr]
                    
                    forReplace = forReplace+ch
                    byReplace = byReplace+ch+"}"
                else:
                    forReplace = forReplace + ch
                    byReplace = byReplace +"{"+ch
                    curr += 1
                    ch = raw_file[curr]
                    while(not(ch.isdigit() or ch.isspace() or (ch in "\n\\}{][)(><+=-*!.,:;/\'\"|$"))):
                        forReplace = forReplace+ch
                        byReplace = byReplace+ch
                        curr += 1
                        ch = raw_file[curr]
                    
                    byReplace = byReplace+"}"
                    curr -= 1
            else:
                count = 0;
                # число аргументов    
                num = 1
                tmp = ""
                while(num > 0):
                    if curr >= len(raw_file):
                        raise Exception("Error in brackets equation in tag \"{}\", position={}".format(forReplace, curr))
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
        begin = begin + res.start()+1
        res = toReplace.search(raw_file[begin:])
   
    return raw_file

                    
