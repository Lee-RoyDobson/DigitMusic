import xml.etree.ElementTree as ET
from collections import Counter
from bs4 import BeautifulSoup
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

def save_to_html(notes, filename):
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
    for note in notes:
        # Create a div element for the note
        note_div = soup.new_tag("div", **{"class": "note"})

        # Create an image element for the note
        img = soup.new_tag("img", src=f"arrow_notes/{note[0]}/{note[1]}.png", alt=f"{note[0]} {note[1]}")

        # Append the image to the note div
        note_div.append(img)
        container.append(note_div)

    # Write the modified HTML back to index.html
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(str(soup))


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

    save_to_html(notes, "index.html")
    
    for note in notes:
        print(note)
    
