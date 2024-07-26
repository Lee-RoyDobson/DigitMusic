import xml.etree.ElementTree as ET

def extract_notes(xml_file):
    """ Extracts the notes from the xml file and returns a list of notes """

    # Parse the xml file and get an element tree
    tree = ET.parse(xml_file)
    root = tree.getroot()

    notes = []


    # Get all the note nodes from the xml file
    for note in root.findall('.//note'):
        # Check if the note has a pitch element
        pitch = note.find('pitch')
        if pitch:
            # Add the step (note) to the list
            notes.append( pitch.find("step").text )
    
    return notes


if __name__ == '__main__':
    notes = extract_notes("Resources\Pachelbels Canon Parts\Pachelbels's Canon_Cello_CMPSR 4.xml")
    print("Running Test...")
    for note in notes:
        print(note)
