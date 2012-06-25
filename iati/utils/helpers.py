# Django specific



def fix_whitespaces(element, leading=True, ending=True, content=True):
    def fix_content(element):
        return element.replace(' ', '-')
    def fix_leading(element):
        while element[0] == ' ':
            element = element[1:]
        return element
    def fix_ending(element):
        length = len(element)
        while element[length-1] == ' ':
            element = element[:length-1]
            length = len(element)
        return element
    if leading and not ending:
        if content:
            return fix_content(fix_leading(leading))
        return fix_leading(element)
    elif ending and not leading:
        if content:
            return fix_content(fix_ending(element))
        return fix_ending(element)
    elif leading and ending:
        if content:
            return fix_content(fix_ending(fix_leading(element)))
        return fix_ending(fix_leading(element))