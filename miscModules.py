
def sectionDump(sectionList):

    sectionHTML = "<ul>"

    for section in sectionList:
        sectionHTML += f"<li>{section}</li>"

    sectionHTML += "</ul>"

    return sectionHTML