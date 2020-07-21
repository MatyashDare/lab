#  NB: data здесь нужна такая - предложения, распарсенные тритаггером

def find_count_errors(data):
    
    many_few_fewer_several_both = r'<(?:(?:M|m)any|(?:F|f)ew|(?:F|f)ewer|(?:S|s)everal|(?:B|b)oth|(?:E|e)ither) DT0>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?<\S*? NN1>'
    bit_amount_deal = r'(?:(<(?:bit|amount) \S*?>)|(<(?:great|good) AJ0><deal NN1>))<of PRF>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?<\S*? NN2>'
    number_couple_of = r'<(?:number(s)?|couple) NN1><of PRF>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?<\S*? NN1>'
    h_thous_mil_s = r'<(?:(?:H|h)undred(s)?|(?:T|t)housand(s)?|(?:M|m)illion(s)?|(?:B|b)illion(s)?) CRD><of PRF>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?<\S*? NN1>'
    little_much_less_least = r'(<the \S*?>)?<(?:little|much|less|least) DT0>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?<\S*? NN2>'
    two_hundreds ='<\S*? CRD><(?:hundreds|thousands|millions|billions) \S*?>'
    one = r'<one CRD><\S*? NN2>'
    numbers = r'<\w*? CRD>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?(<\S*? AJ0>)?<\S*? NN1>'

    speople = r'<((sports)?people) \S*?>'
    species = r'<species \S*?>'

    for q in data:
        
        sfind = re.findall(speople, q)
        # no 'people' or 'sportspeople' in NN0
        if sfind:
            if 'sports' in sfind[0]:
                q = re.sub(r'<sportspeople (\S*?)>', r'<sportspeople NN2>', q)
            else:
                q = re.sub(r'<people (\S*?)>', r'<people NN2>', q)
        # no 'species'
        elif species:
            q = re.sub(species, '', q)

        ## MANY/FEW/FEWER/SEVERAL/BOTH + NN1
        # no 'many sport facilities' type
        if re.findall(many_few_fewer_several_both + '<\S*? NN2>',q):
            pass
        elif re.findall(many_few_fewer_several_both, q):
            if re.findall(r'<(?:B|b)oth DT0>(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?<\S*? NN[0-9]>(<\S*? POS>)?<and CJC>', q):
                pass
            else:
                #errors.append(q)
                #errors_sentences.append(sentence)
                q.append('Check the form of the noun used with many/few/fewer/several or both')
        
        #BIT/AMOUNT/DEAL + OF + NN2
        elif re.findall(bit_amount_deal, q):
            # no 'many sport facilities' type
            if re.findall(bit_amount_deal + '<\S*? NN2>',q):
                pass
            # no 'amount of' + gases' or 'substances'
            elif re.findall(r'<amount \S*?><of PRF><(?:gases|substances) NN[0-9]>', q):
                pass
            else:
                #errors.append(q)
                #errors_sentences.append(sentence)
                q.append('Check the form of the noun used with bit/amount or deal + of')
    
        # NUMBER/COUPLE + OF
        elif re.findall(number_couple_of, q):
            if re.findall(number_couple_of + '<\S*? NN2>', q):
                pass
            elif re.findall(r'<percentage NN[0-9]><number(s)? NN1><of PRF>', q):
                pass
            else:
                #errors.append(q)
                #errors_sentences.append(sentence)
                q.append('Check the form of the noun used with bit/amount or deal + of')

                ## HUNDRED(S)... + OF + NN1
        elif re.findall(h_thous_mil_s, q):
            if re.findall(h_thous_mil_s + '<\S*? NN2>', q):
                pass
            else:
                #errors.append(q)
                #errors_sentences.append(sentence)
                q.append('Check the form of the noun used with number + of')
            
        # LITTLE/MUCH/LESS/THE LEAST + NN2
        elif re.findall(little_much_less_least, q):
            #errors.append(q)
            #errors_sentences.append(sentence)
            q.append('Check the form of the noun used with little/much/less/the least')
            
        # number + 'hundreds' type
        elif re.findall(two_hundreds, q):
            #errors.append(q)
            #errors_sentences.append(sentence)
            q.append('Check the form of the number used with number')
            
        ## one + NN2
        elif re.findall(one, q):
            #errors.append(q)
            #errors_sentences.append(sentence)
            q.append("Check the form of the number used with 'one'")

        ## numbers
            if re.findall(numbers,q):
                if re.findall('<\w*? CRD>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?(<\S*? AJ0>)?(<\S*? AJ0>)?<\S*? NN1><\S*? NN2>',q):
                    pass
                else:
                    num = re.findall('<(\w*?) CRD>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?(<\S*? AJ0>)?<\S*? NN1>', q)
                    n = num[0][0]
                    if n != '':
                        #pass if '%'
                        if re.findall('{0}( )?%'.format(n), sentence):
                            pass
                        elif n == '1':
                            pass
                        elif re.findall(r'<(?:O|o)ne CRD>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?(<\S*? AJ0>)?<\S*? NN1>', q):
                            pass 
                        #pass if a 'procent' or a 'precent' or 'prosent' or 'percentage'
                        #(the same word, but with spelling mistake) is mentioned
                        elif re.findall('<{0} CRD>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?(<\S*? AJ0>)?<pr(?:a|e|o)(?:k|c|s)ent(age)? NN1>', q):
                            pass
                        elif re.findall('<{0} CRD>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?(<\S*? AJ0>)?<p(?:a|e|o)r(?:k|c|s)ent(age)? NN1>', q):
                            pass
                        #pass if a date is mentioned
                        elif re.findall('{0} year'.format(n), sentence):
                            pass
                        #pass if a date is mentioned (like 'in/by 2000 there was..')
                        elif re.findall(r'<(?:((?:I|i)n)|((?:B|b)y)) \S*?>(<the \S*?>)?(<year(s)? \S*?>)?(<of \S*?>)?<\w*? CRD>', q):
                            pass
                        elif re.findall(r'<(?:((?:B|b)etween>)|((?:F|f)rom)) \S*?>(<the \S*?>)?(<year(s)? \S*?>)?(<of \S*?>)?<\w*? CRD>', q):
                            pass
                        elif re.findall(r'<(?:((?:S|s)in(?:s|c)e)|((?:A|a)fter)) \S*?>(<the \S*?>)?(<year(s)? \S*?>)?(<of \S*?>)?<\w*? CRD>', q):
                            pass
                        elif re.findall(r'year(s)?(?:-| )old', sentence):
                            pass
                        elif re.findall('<\w*? CRD>(<\S*? AT0>)?(<\S*? DT0>)?(<\S*? ADV)?(<the \S*?><most \S*?>)?(<\S*? AJ0>)?(<\S*? AJ0>)?<(:?level|age|rate|period|century|decade) NN1>', q):
                            pass
                        else:
                            #errors.append(q)
                            #errors_sentences.append(sentence)
                            q.append("Check the form of the noun or noun group used with numbers")
        
        return data
