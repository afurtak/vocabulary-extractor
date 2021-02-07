## Setup project
### Get Stanford CoreNLP
Download stanford CoreNLP from https://stanfordnlp.github.io/CoreNLP/download.html, unzip it and run 
```
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
```
to start stanford nlp server. It will be used to parse sentences' dependencies

### Get Rapidapi key
Get Rapidapi key and save it in `x-rapidapi-key` file

### Install requirements
run this command with activated python virtual environment 
```
pip install -r requirements.txt
```

## Run project
To run vocabulary extractor use command:
```
python -m src.vocabulary_extractor --input <input_file_path> --output <output_file_path> [--min-level <1-10>]
```