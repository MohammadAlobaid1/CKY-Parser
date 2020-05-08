
def cky_recognize(string, grammar, lexicon):
    '''CKY recognizer to determine well-formedness of string.
    The string is assumed to be tokenized and lowercased already, e.g.
    ["the", "man", "water", "s", "the", "flower", "s"].

    Arguments
    ---------
    string (str): a string to be parsed
    grammar (dict) : a grammar to be parsed 
    lexicon (dict) : a lexicon to be parsed 

    Return
    ------
    bool: boolean value that detrimine the well-formedness of a string.
    '''
    #calling a function that return a matrix and storing it in a variable
    matrix = cky_matrix(string, grammar, lexicon)
    #if you reach final state (right top corner) and is S return True 
    if "S" in (x[1] for x in matrix[0][len(string)-1]) :
      return True 
    else:
      return False


def cky_matrix(string, grammar, lexicon):
    '''A function that return a matrix of combinations and backpointer in a form of dict.

    Arguments
    ---------
    string (str): a string to be parsed
    grammar (dict) : a grammar to be parsed 
    lexicon (dict) : a lexicon to be parsed 

    Return
    ------
    list : a list that contain element of matrix parsed diagnoally. 
    matrix : a matrix shape of parsed items where parsing works diagnoally.
    dict : a dict of backpointer in the form of ("POS", (key, index), (key, index)). 
    '''
    
    backpointer = {}
    cky_list = []
    string_len = len(string)
    #create a matrix for x and y relative to the string length
    matrix = [[[] for x in range(string_len)] for y in range(string_len)]

    for index in range(string_len):
      #print("index: ",index, " string_len: ",string_len)
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

    #define the values for j and i and x and y that will operate over diagnoal  
    i = 1
    j = 0
    start_x = 0 
    start_y = 1
    done = False
    #iterate until you reach the final state (the top right corner)
    #in other words if done = True
    while not done:
      #take the length of the string -1 
      string_len += -1
      x = start_x
      y = start_y
      # create the diagnol loop
      for index in range(string_len):
        keep_iter = True
        #while True keep iterating for the list inside the postion 
        #position = x,y 
        #row formula = x,x+j such that  j starts from 0
        #colum formula = x+i,y such that i starts from 1 
        while keep_iter:
          print("i: ", i , " j: ", j, " x: ", x, " y: ", y)
          #iterate over the list inside the cell of the matrix
          #find a valid grammar by checking the values inside the list in matrix[x][x+j] with the values inside the matrix[x+i][y]
          for transition1 in matrix[x][x+j]:
            for transition2 in matrix[x+i][y]:
              #check if the dict (grammar) has the (lefthand) symbol
              state1 = grammar.get(transition1[1],None)
              print("state1: ", state1)
              if state1:
                #check if the (lefthand) symbol has the (righthand symbol) 
                state2 = grammar.get(transition1[1],None).get(transition2[1],None)
                if state2:
                  matrix[x][y].append((transition1[0],state2,transition2[2]))
                  #backpointer relative to x,y
                  #backpointer[(x,x+j)]] refers to left symbol on row (backpointer1)
                  #backpointer[(x+i,y)]] refers to bottom symbol on col(backpointer2)
                  index1 = [t[0]for t in backpointer[(x,x+j)]].index(transition1[1] )
                  index2 = [t[0]for t in backpointer[(x+i,y)]].index(transition2[1] )
                  #if (x,y) the key is None 
                  if backpointer.get((x,y)) == None:
                    #add it along with the value in a form of tuple
                    backpointer[(x,y)]= [(state2,((x,x+j),index1),((x+i,y),index2))]
                  else:
                    #if it exist add the new value
                    backpointer[(x,y)].append((state2,((x,x+j),index1),((x+i,y),index2)))
          #increase col and row                  
          i+=1
          j+=1
          #if x+j == y, then we are at position x,y(the position we are trying to fill out the value for)
          #if so stop iteration
          if x+j == y:
            keep_iter = False 
        #increase diagnol iteration and reset i and j 
        x += 1
        y += 1
        i = 1
        j = 0
      #move to the next diagnal 
      start_y += 1
      #if finished from all string done = True break 
      if string_len < 1:
        done = True

    #below creates the shape of matrix 
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
    '''A function to change tuples to dict. 

    Arguments
    ---------
    grammar (set) : set of tuples of the form ('lefthand side',(symbol 1'), ('symbol 2'))

    Return
    ------
    dict : A dictionary of the form {'symbol 1': {'symbol 2': 'lefthand side'}}
    '''
    new_grammar = {} 
    #loop over tuples
    for (q1, (symbol1, symbol2)) in grammar:
      if symbol1 in new_grammar:
        #if there is symbol add it along with the previous symbol
        new_grammar[symbol1].update({symbol2: q1})
      else:
        # if there is none add it
        new_grammar[symbol1] = {symbol2: q1}
        
    return new_grammar

def convert_lexicon(lexicon):
    '''A function to reverse lexicon dict keys to values and visa versa.

    Arguments
    ---------
    lexicon (dict) : A dictionary with part of speech as keys and  words as values

    Return
    ------
    dict : A dictionary with words as keys and part of speech as values
    '''
    new_lexicon = {}
    #iterate over the keys and values in dict
    for key,value in lexicon.items():
      for word in value:
        if word in new_lexicon:
          #if there is symbol add it along with the previous symbol
          new_lexicon[word].append(key)
          #if there is none add it
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
