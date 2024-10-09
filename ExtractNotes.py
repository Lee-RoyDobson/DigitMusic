import xml.etree.ElementTree as ET
from collections import Counter
from bs4 import BeautifulSoup
import json

note_scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
note_pattern = [2, 2, 1, 2, 2, 2, 1]


def save_to_html(notes, filename, group_size=4):
    """ Writes the notes to an HTML file no return value """
    html_content = None
    # Read the index.html file
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Get the notes container
    container = soup.find(id="notes-container")

    # Clear the container to get rid of any existing notes
    container.clear()

    # Create div and img elements for each note and append them to the container
    for i in range(0, len(notes), group_size):
        # Create a sub div element for the group of notes
        note_group_div = soup.new_tag("div", **{"class": "note-group"}) # ** is for unpacking the dict

        cur_note = 1 # Counter for the current note
        
        for note in notes[i:i+group_size]:
            # Create a div element for the note
            note_div = soup.new_tag("div", **{"class": "note"})

            # Create a span element for the note number
            note_number = soup.new_tag("span", **{"class": "note-number"})

            # Set the note number text
            note_number.string = str(cur_note)

            cur_note += 1

            # Create an image element for the note
            img = soup.new_tag("img", src=f"arrow_notes/{note[0]}/{note[1]}.png", alt=f"{note[0]} {note[1]}")

            # Append the note number to the note div
            note_div.append(note_number)

            # Append the image to the note div
            note_div.append(img)

            # Append the note div to the sub div
            note_group_div.append(note_div)

            # Append the note group div to the container
            container.append(note_group_div)
        
      
    # Write the modified HTML back to the file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(soup))

def note_to_direction(step, octave, base_octave, note_map):
    """ Maps the note to a direction based on the base octave and returns the direction as an integer """

    # Get the note from the step
    note = note_map.get(step, None)
   
    # Check if the note is 1 and the octave is greater than the base octave
    if note == 1 and int(octave) > base_octave:
        return 8
    
    return note

def extract_notes(xml_file, note_scale, note_pattern):
    """ Extracts the notes and duration from the xml file and returns a string tuple of duration and arrow direction """

    # Parse the xml file and get an element tree
    tree = ET.parse(xml_file)
    root = tree.getroot()

    notes = []
    base_octave = None

    # Get the key of the music
    key = find_key(int(root.find(".//key").find("fifths").text), root.find(".//key").find("mode").text)
    key = convert_to_standard(key)
    print(key)
    # Generate the note map
    note_map = generate_note_scale(key, note_scale, note_pattern)
    #print(note_map)

    # Get all the note nodes from the xml file
    for note in root.findall(".//note"):
        # Check if the note has a pitch element
        pitch = note.find("pitch")
        if pitch:
            # Get the step (note) from the pitch element
            step = pitch.find("step").text 

            # Get the octave of the note
            octave = pitch.find("octave").text

            # Get the alter (check if sharp for now)
            alter = pitch.find("alter")
            if alter is not None:
                alter = alter.text
                step = apply_alter(step, alter)
            
            step = convert_to_standard(step)

            if step == key:
                if not base_octave:
                    base_octave = int(octave)
                elif int(octave) < base_octave:
                    base_octave = int(octave)


    for note in root.iter("note"):
        pitch = note.find("pitch")
        if pitch:
            # Get the step (note) from the pitch element
            step = pitch.find("step").text
            

            # Get the octave of the note
            octave = pitch.find("octave").text

            # Get the duration of the note
            duration = note.find("type").text

            # Get the alter (check if sharp for now)
            alter = pitch.find("alter")
            if alter is not None:
                alter = alter.text
                step = apply_alter(step, alter)

            step = convert_to_standard(step)
            #print(step)

            # Get the direction of the note
            direction = note_to_direction(step, octave, base_octave, note_map)
            #print(direction, step, octave)

            
            
            notes.append((duration, direction))
    
    return notes

def generate_note_scale(key, note_scale, note_pattern):
    """ Generates a note scale based on the key and note pattern and returns a dictionary of the note and direction """
    # The key works out to be the starting index of the note scale
    start_index = note_scale.index(key)
    # Start at direciton 1 (North)
    direction_count = 1
    # Create the scale dictionary with the starting note
    scale = {note_scale[start_index] : direction_count}
    current_index = start_index

    # Iterate over each step in the note pattern
    for step in note_pattern:
        # Increment the direction count for the next direction
        direction_count += 1
        # Get the next index accounting for the length of the note scale
        current_index = (current_index + step) % len(note_scale)
        # If the note at the current index is not already in the scale, add it
        if note_scale[current_index] not in scale:
            scale[note_scale[current_index]] = direction_count


    return scale

def find_key(fiths, mode):
    """ finds the key of the music based on the fiths and mode """
    if mode == "major":
        match fiths:
            case 0: return "C"
            case 1: return "G"
            case 2: return "D"
            case 3: return "A"
            case 4: return "E"
            case 5: return "B"
            case 6: return "F#"
            case 7: return "C#"
            case -1: return "F"
            case -2: return "Bb"
            case -3: return "Eb"
            case -4: return "Ab"
            case -5: return "Db"
            case -6: return "Gb"
            case -7: return "Cb"

def convert_to_standard(step):
    """ Converts the step to a standard note """
    match step:
        case "Cb": return "B"
        case "Db": return "C#"
        case "Eb": return "D#"
        case "Fb": return "E"
        case "Gb": return "F#"
        case "Ab": return "G#"
        case "Bb": return "A#"
        case "E#": return "F"
        case "B#": return "C"
        case _: return step
        
def apply_alter(step, alter):
    """ Applies the alter to the step and returns the new step """
    if (alter is not None) and (alter == "1"):
        step += "#"
    elif (alter is not None) and (alter == "-1"):
        step += "b"
    return step


  
if __name__ == "__main__":
    note_scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_pattern = [2, 2, 1, 2, 2, 2, 1]

    notes = extract_notes("Arrownotes AI Assets\XML Files\B Major.xml", note_scale, note_pattern)
    
    save_to_html(notes, "index.html", 4) 
    
