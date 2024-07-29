import xml.etree.ElementTree as ET
from collections import Counter
import json

# Dictionary to map the notes to the direction
arrow_note_map = {
    "D": "N",
    "F": "NE",
    "A": "E",
    "C": "SE",
    "B": "SW",
    "G": "W",
    "E": "NW"
}

def save_notes_to_json(notes, filename):
    """ Writes the notes to a JSON file no return value """

    # Clear the JSON file if it exists
    with open("notes.json", "w") as f:
        pass

    # Write the notes to the JSON file
    with open("notes.json", "w") as f:
        json.dump(notes, f)

def note_to_direction(step, octave, base_octave):
    """ Maps the note to a direction based on the base octave and returns the direction as a string """
    # Check if the note is D and an octave higher than the base octave
    if step == "D" and int(octave) > base_octave:
        return "S"
    return arrow_note_map.get(step, "Unknown")

def extract_notes(xml_file):
    """ Extracts the notes and duration from the xml file and returns a string tuple of duration and arrow direction """

    # Parse the xml file and get an element tree
    tree = ET.parse(xml_file)
    root = tree.getroot()

    notes = []
    octaves = []
    base_octave = None

    # Get all the note nodes from the xml file
    for note in root.findall(".//note"):
        # Check if the note has a pitch element
        pitch = note.find("pitch")
        if pitch:
            # Get the step (note) from the pitch element
            step = pitch.find("step").text 

            # Get the octave of the note
            octave = pitch.find("octave").text

            # Convert the octave to an integer and append it to the list
            octaves.append(int(octave))

    # Determine the base octave (most common octave)
    base_octave = Counter(octaves).most_common(1)[0][0]

    for note in root.iter("note"):
        pitch = note.find("pitch")
        if pitch:
            # Get the step (note) from the pitch element
            step = pitch.find("step").text

            # Get the octave of the note
            octave = pitch.find("octave").text

            # Get the duration of the note
            duration = note.find("type").text

            # Get the direction of the note
            direction = note_to_direction(step, octave, base_octave)

            notes.append((duration, direction))
    
    return notes


if __name__ == "__main__":
    notes = extract_notes("Resources\Pachelbels Canon Parts\Pachelbels's Canon_Cello_CMPSR 4.xml")

    save_notes_to_json(notes, "notes.json")
    
    for note in notes:
        print(note)
    
