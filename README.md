# Clickbait Detector
A chrome extension to check percentage of clickbaits

## Requirements
- Python 2.7.6

## Getting Started
1. Install virtualenv in the project directory  
    `sudo pip install virtualenv`  
    `virtualenv venv`
  
2. Activate the virtualenv  
    On Linux  
    `source venv/bin/activate`
    
3. Install the requirements  
    `pip install -r requirements.txt`
    
4. Run the python server  
    `python server.py`
    
5. Open chrome extensions

6. Enable developer mode

7. Load unpacked extension and add this directory

## About
- Scrapes the website and uses visible text to check if there are clickbaits 
- Uses Naive Bayes Classifier to classify text as clickbaits or genuine
- Dataset about 12000 sentences out of which half are clickbaits taken from another github repo
- Accuracy is not that great, needs improvement

## Examples
1. www.buzzfeed.com - 51.724137931 %
2. www.timesofindia.com - 25.5490483163 %
