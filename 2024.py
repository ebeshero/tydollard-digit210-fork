import spacy
import os
import shutil
import json
import warnings

# Suppress FutureWarnings, including the one about 'pyarrow'
warnings.filterwarnings("ignore", category=FutureWarning)

# Check and install pandas module
try:
    import pandas as pd
except ModuleNotFoundError:
    print("pandas module not found. Installing...")
    os.system('pip install pandas')
    import pandas as pd

# Check and install dicttoxml module
try:
    from dicttoxml import dicttoxml
except ModuleNotFoundError:
    print("dicttoxml module not found. Installing...")
    os.system('pip install dicttoxml')
    from dicttoxml import dicttoxml

# Check and install spaCy model 'en_core_web_md'
try:
    nlp = spacy.load('en_core_web_md')
except OSError:
    print("en_core_web_md spaCy model not found. Downloading...")
    os.system('python -m spacy download en_core_web_md')
    nlp = spacy.load('en_core_web_md')

# Check and install pyarrow
try:
    import pyarrow
except ModuleNotFoundError:
    print("pyarrow module not found. Installing...")
    os.system('pip install pyarrow')

from xml.dom.minidom import parseString

# Define a new word of interest
new_word_of_interest = 'exciting'

# Identify the directory with text files to explore
workingDir = os.getcwd()
CollPath = os.path.join(workingDir, 'textCollection')

# Clear existing output folders
for folder in ['JSON-output', 'csv-output', 'xml-output']:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)

# Create a function for reading and processing text files
def readTextFiles(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        readFile = f.read()
        tokens = nlp(readFile)

        wordOfInterest = nlp(new_word_of_interest)

        highSimilarityDict = {}
        for token in tokens:
            if token.vector_norm and wordOfInterest.vector_norm:
                if wordOfInterest.similarity(token) > 0.3:
                    highSimilarityDict[token.text] = wordOfInterest.similarity(token)

        return highSimilarityDict

# Iterate over text files in the 'textCollection' directory
for file in sorted(os.listdir(CollPath)):
    if file.endswith(".txt"):
        filepath = f"{CollPath}/{file}"
        filename = os.path.splitext(os.path.basename(filepath))[0]
        similarityData = readTextFiles(filepath)

        # Output to JSON
        with open(f'JSON-output/{filename}.json', 'w') as fp:
            json.dump(similarityData, fp)

        # Output to CSV
        df = pd.DataFrame(list(similarityData.items()), columns=['token', 'similarity'])
        df.to_csv(f'csv-output/{filename}.csv', index=False, encoding='utf-8')

        # Output to XML
        xml = dicttoxml(similarityData)
        dom = parseString(xml)
        with open(f'xml-output/{filename}.xml', 'w') as xmlFile:
            xmlFile.write(dom.toprettyxml())
