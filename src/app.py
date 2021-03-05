def segmantize(text, identifiers):
  
  i = 0
  list_of_index = []
  for line in text:
    i += 1
    first_word = line.split(' ')[0]
    last_word = ' '
    
    if len(line.split(' ')) > 1:
      last_word = line.split(' ')[-2]
    print(f"{first_word} and {last_word}")
    if (first_word.lower() in [x.lower() for x in identifiers]) or (last_word.lower() in [x.lower() for x in identifiers]):

      list_of_index.append(i-1)

  print(list_of_index)
  articles = []
  for x in range(len(list_of_index)-1):
    new_list = []
    for y in range(list_of_index[x],list_of_index[x+1]):
    
      new_list.append(text[y])
    
    articles.append(new_list)  
  end_list = []
  if len(list_of_index) > 0:
    for z in range(list_of_index[-1], len(text)):
      end_list.append(text[z])
  
    articles.append(end_list)


  
  return articles