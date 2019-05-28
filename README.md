## Article Classifier

Project done for the [MSc Big Data & Business Analytics from ESCP Europe](https://www.escpeurope.eu/programmes/specialised-masters-MScs/MSc-in-Big-Data-and-Business-Analytics).

### Prerequis
Install packages
```markdown

pip3 install terminaltables 
pip3 install unidecode 
pip3 install spacy 
pip3 install bs4 
```

### Launching project

#**Select your own branch on the top of this window, don't code on master !**#

Clone the repo in your computer using command
```markdown
git clone https://github.com/ArthurMARIANI/Articles_Classifier.git
```

Go into the project and run 
```markdown
python3 main.py *number of articles of the txt file you want to scrap*
```
The result will be in the json file (located in files/)

### Configuration 

Check on the config.py file the path of the txt file containing the list of articles and the path you name you want for the result file (in json)

### Implementation 

You can add your own functions of extraction on models/articles.py
It was configured to allow you to easy implement content.
The schema should be this :

    def extractAttribute(self, raw):
          *** your code ***
        return result
        
Naming should respect this schema of extract+Attribute(self, raw).
Change "Attribute" by what you want to extract, it will be automaticaly implemented into the model.

*raw* parameter is the full webpage, you can use BeautifulSoup of whaterver you like to parse it and find the element you want

At the end, return the result of your algorithm to integrate it into the output file

