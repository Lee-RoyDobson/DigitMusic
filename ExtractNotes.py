import xml.etree.ElementTree as ET

def extract_notes(xml_file):
    """ Extracts the notes and duration from the xml file and returns a string tuple of notes, octave and duration """

    # Parse the xml file and get an element tree
    tree = ET.parse(xml_file)
    root = tree.getroot()

    notes = []


    # Get all the note nodes from the xml file
    for note in root.findall(".//note"):
        # Check if the note has a pitch element
        pitch = note.find("pitch")
        if pitch:
            # Get the step (note) from the pitch element
            step = pitch.find("step").text 

            # Get the octave of the note
            octave = pitch.find("octave").text

            # Get the duration of the note
            duration = note.find("type").text
            
            notes.append( (step, octave, duration) )
    
    return notes


if __name__ == "__main__":
    notes = extract_notes("Resources\Pachelbels Canon Parts\Pachelbels's Canon_Cello_CMPSR 4.xml")
    for note in notes:
        print(note[0], note[1], note[2])
