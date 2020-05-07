def cky_recognize(string, grammar, lexicon):
    """CKY recognizer to determine well-formedness of string.
    The string is assumed to be tokenized and lowercased already, e.g.
    ["the", "man", "water", "s", "the", "flower", "s"]
    """
    matrix = cky_matrix(string, grammar, lexicon)
    #if you reach final and is S return True 
    if "S" in (x[1] for x in matrix[0][len(string)-1]) :
      return True 
    else:
      return False


def cky_matrix(string, grammar, lexicon):
    """CKY recognizer to determine well-formedness of string.
    The string is assumed to be tokenized and lowercased already, e.g.
    ["the", "man", "water", "s", "the", "flower", "s"]
    """
    backpointer = {}
    cky_list = []
    string_len = len(string)
    matrix = [[[] for x in range(string_len)] for y in range(string_len)]

    for index in range(string_len):
      if not lexicon.get(string[index],None):
        return []
      #save the leafs
      for x in lexicon[string[index]]:
        matrix[index][index].append((index,x,index+1))
        #save the leaf nodes as None
        if backpointer.get((index,index)) == None:
          backpointer[(index,index)] = [(x,None,None)]
        else:
          backpointer[(index,index)].append((x,None,None))
    i = 1
    j = 0
    start_x = 0 
    start_y = 1
    done = False   
    while not done: 
      string_len += -1
      x = start_x
      y = start_y

      for index in range(string_len):
        #print("string_len: ", string_len)
        keep_iter = True

        while keep_iter:
          #print("i: ", i , " j: ", j, " x: ", x, " y: ", y)
          #matrix[x][x+j] transition1 (row)
          #matrix[x+i][y] transition 2 (col)
          for transition1 in matrix[x][x+j]:
            for transition2 in matrix[x+i][y]:
              
              #print("state1: ", state1, "state2: ",state2)
              state1 = grammar.get(transition1[1],None)
        
              if state1:
                state2 = grammar.get(transition1[1],None).get(transition2[1],None)
                if state2:
                  matrix[x][y].append((transition1[0],state2,transition2[2]))
                
                  index1 = [t[0]for t in backpointer[(x,x+j)]].index(transition1[1] )
                  index2 = [t[0]for t in backpointer[(x+i,y)]].index(transition2[1] )
                  
                  if backpointer.get((x,y)) == None:
                    backpointer[(x,y)]= [(state2,((x,x+j),index1),((x+i,y),index2))]
                  else:
                    backpointer[(x,y)].append((state2,((x,x+j),index1),((x+i,y),index2)))
                            
          i+=1
          j+=1

          if x+j == y:
            keep_iter = False

        x += 1
        y += 1
        i = 1
        j = 0

      start_y += 1
      if string_len < 1:
        done = True

    log = ""
    y = 0

    for x in range(len(string)):
       log +=  "|\t" + str(x) + "\t"

    for i in range(len(matrix)):
      log += "\n"
      log += "--------------------------------------------------------------------------------------\n"
      log +=  str(i) + "|"
      y  += 1 

      for i2 in range(len(matrix[i])):
        log += ", ".join([str(x[1])  for x in matrix[i][i2]]) + "\t\t|" 
    
    print(log)
    print(backpointer)
    return matrix

def convert_grammar(grammar):
    '''A method to convert grammar to dict'''
    new_grammar = {} 
    for (q1, (symbol1, symbol2)) in grammar:
      if symbol1 in new_grammar:
        #if there is symbol add it along with the previous symbol
        new_grammar[symbol1].update({symbol2: q1})
      else:
        new_grammar[symbol1] = {symbol2: q1}
        
    return new_grammar

def convert_lexicon(lexicon):
    '''A method to convert lexicon to dict'''
    new_lexicon = {}
    for key,value in lexicon.items():
      for word in value:
        if word in new_lexicon:
          #if there is symbol add it along with the previous symbol
          new_lexicon[word].append(key)
        else:
          new_lexicon[word] = [key]
           
    return new_lexicon

def test_cky(sentence=None):
    """Test cky_recognize.
    You can either specify your own sentence as a string,
    or use the default test sentences.
    """

    lexicon = {
        "A": ["old", "former", "alleged", "handsome", "big", "ugly"],
        "Adv": ["very", "quickly", "allegedly", "today"],
        "Agr": ["s"],
        "Det": ["a", "the", "this", "these", "those", "some", "every"],
        "P": ["at", "on", "in", "near", "above", "below", "under"],
        "N": ["balcony", "boat", "man", "old", "woman", "singer", "opera", "water", "slide", "flower"],
        "Poss": ["'s"],
        "Vi": ["sleep", "slide", "rust", "flower"],
        "Vt": ["water", "see", "man", "like"],
        }
    grammar = (
        ("AdvP", ("Adv", "Adv")),
        ("AdvP", ("Adv", "AdvP")),
        ("AP", ("Adv", "A")),
        ("AP", ("AdvP", "A")),
        ("AP", ("Adv", "AP")),
        ("AP", ("AdvP", "AP")),
        ("D'", ("Poss", "NP")),
        ("D'", ("Poss", "N")),
        ("DP", ("Det", "N")),
        ("DP", ("Det", "NP")),
        ("DP", ("DP", "D'")),
        ("N", ("N", "N")),
        ("N", ("N", "Agr")),
        ("NP", ("A", "N")),
        ("NP", ("A", "NP")),
        ("NP", ("AP", "N")),
        ("NP", ("AP", "NP")),
        ("NP", ("N", "PP")),
        ("PP", ("P", "DP")),
        ("S", ("DP", "VP")),
        ("S", ("DP", "Vi")),
        ("VP", ("Adv", "Vi")),
        ("VP", ("Adv", "VP")),
        ("VP", ("AdvP", "Vi")),
        ("VP", ("AdvP", "VP")),
        ("VP", ("Vi", "Adv")),
        ("VP", ("Vi", "AdvP")),
        ("VP", ("VP", "Adv")),
        ("VP", ("VP", "AdvP")),
        ("VP", ("Vt", "DP")),
        ("Vi", ("Vi", "Agr")),
        ("Vt", ("Vt", "Agr")),
        )
    # make any required changes to the grammar format
    lexicon = convert_lexicon(lexicon)
    grammar = convert_grammar(grammar)

    # default test sentences
    sentences = {
        "the ugly water slide s rust": True,
        "the old man the boat": True,
        "slide": False,
        "every opera singer 's water on some very very old woman 's balcony very quickly man s the boat today": True,
        "": False,
        "John sleep s": False,
        }
    if sentence:
      	  
        return cky_recognize(sentence, grammar, lexicon)
    else:
        for s, val in sentences.items():
            if cky_recognize(s.split(), grammar, lexicon) != val:
                print("Wrong output!")
                print(f"The following sentence should be {val}")
                print(s)

#convert_grammar(grammar)
#convert_lexicon(lexicon)
#cky_recognize("the old man the boat".split(), convert_grammar(grammar),convert_lexicon(lexicon))
#cky_matrix("the ugly water slide s rust".split(), convert_grammar(grammar),convert_lexicon(lexicon))
