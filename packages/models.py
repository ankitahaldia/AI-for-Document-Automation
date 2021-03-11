# TODO : continuation of paragraphs on another page??
# TODO : what if the first word of a page is chapter or article ??
# TODO : erratum layout
# TODO : what if the chapter name takes multiple lines?
import statistics as stat




class Dto():
    text = ' '
    page = 0        
    left_coord = 0.0
    top_coord = 0.0
    width = 0.0
    height = 0.0
    confidence = 100.0
    is_text = False

    def __str__(self):
        return (f'{self.text}') 

class Paragraph():
    type = ''
    name = ''
    number = 0
    text = []
    page = 0
    left_coord = 0.0
    top_coord = 0.0
    width = 0.0
    height = 0.0
    confidence = 100.0
    sub_paragraphs = []
    sub_dtos = []

def build_paragraphs(list_dto, identifiers):
    '''
    always put the full name of the identifiers as first element of the list identifiers.
    '''
    # TODO : manage continuation of a paragraph on different pages
   
    output_list = []
    is_first_line = True
    has_reached_identifier = False
    paragraph = Paragraph()
    i = 1

    for dto in list_dto:
        if is_first_line and dto.text[0].lower() in identifiers:
            
            if i > 1:                
                paragraph.confidence = stat.mean([sub.confidence for sub in paragraph.sub_dtos].append(paragraph.confidence))
                paragraph.width = max([sub.width for sub in paragraph.sub_dtos].append(paragraph.width)) 
                paragraph.height += sum([sub.height for sub in paragraph.sub_dtos])
                output_list.append(paragraph)
            
            paragraph = Paragraph()
            paragraph.name = dto.text[1:] # TODO: improve this so we can remove digits and roman numbers
            paragraph.type = identifiers[0]
            paragraph.number = i
            paragraph.page = dto.page
            paragraph.left_coord = dto.left_coord
            paragraph.top_coord = dto.top_coord
            paragraph.height = dto.height
            paragraph.width = dto.width
            paragraph.confidence = dto.confidence 
            i += 1            
            has_reached_identifier = True
                                                            # elif is_first_line and dto.text[0].lower() in ['bijlage', 'annexe' ]:
                                                            #     #TODO : create annexe and takes all the rest of the document
                                                            #     pass
                                                            # elif is_first_line and 'neerlegging-d' in dto.text[0].lower():
                                                            #     #TODO : create paragraph STAMP
                                                            #     pass
        
        elif has_reached_identifier:
            is_first_line = False
            paragraph.text.append(dto.text)
            paragraph.sub_dtos.append(dto)

        else:
            is_first_line = False
        if dto.text[0] == ' ':            
            is_first_line = True

    paragraph.confidence = stat.mean([sub.confidence for sub in paragraph.sub_dtos].append(paragraph.confidence))
    widths = [sub.width for sub in paragraph.sub_dtos]
    widths.append(paragraph.width)
    paragraph.width = max(widths)
    paragraph.height += sum([sub.height for sub in paragraph.sub_dtos])
    output_list.append(paragraph)



def procession(df, page_number):
    
    df['text'] = df['text'].apply(lambda x : str(x))
    df = df[df['text'] != 'nan']

    list_output = []
        
    blocks = df.groupby('block_num')
    for _, block in blocks:
        paragraphs = block.groupby('par_num')
        for _, paragraph in paragraphs:
            lines = paragraph.groupby('line_num')
            for _, line in lines:
                dto = Dto()
                dto.text = ' '.join([str(te) for te in line['text']])
                dto.page = page_number
                dto.left_coord = line.iloc[0]['left']
                dto.top_coord = line.iloc[0]['top']
                dto.width = sum(line.iloc['width'])
                dto.height = line.iloc[0]['height']
                dto.confidence = stat.mean(line['conf'])
                dto.is_text = True
                list_output.append(dto)
                pass
            dto = Dto()
            list_output.append(dto)
        dto = Dto()
        list_output.append(dto)

    return list_output




