import string
class Utils(object):
    @staticmethod
    def cleaner(elements: list):
        """
        Extract the title of the article with this hierarquy : 
        1. In metadata
        2. Reading H1 tags
        """

        cleaned = []
        if elements:
            for element in elements:
                [s.extract() for s in element('i')]
                [s.extract() for s in element('a')]

                content = element.text
                content = content.replace("\n", '')
                content = content.replace("\r", '')
                    
                cleaning_content = content
                for c in string.punctuation:
                    cleaning_content = cleaning_content.replace(c, "")
                if(cleaning_content.split()):
                    cleaned.append(content)

            if cleaned:
                return cleaned
        return None
    
    @staticmethod
    def checkLength(content):
        words = 0
        for paragraph in content:
            words += len(paragraph.split())
        return words
