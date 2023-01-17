from xml.sax.handler import ContentHandler
import xml.sax
import xml.parsers.expat
import configparser


class xmlParser(xml.sax.handler.ContentHandler):
    """
    This class is to parse the xml file



    """

    def __init__(self):
        """

        """
        self.dictionary = dict()
        self._charBuffer = []
        self.docid = ""
        self.paragraph = ""
        self.headline = ""

    def _flushCharBuffer(self):
        """

        """
        s = ''.join(self._charBuffer)
        self._charBuffer = []
        return s
    
    def startElement(self, name, attrs):
        """

        """
        self.CurrentData = name
        if name == "DOC":
            self.clearFields() #indicate start of new doc amd clear previous documents info
            self.docid = attrs.getValue("id") #get document id



    def endElement(self, name):
        """
        Updates the dictionary
        Parameter:
        name (string): name of the tag
        """
        if name == "TEXT": #indicates end of a document
            self.dictionary[self.docid] = [self.headline, self.paragraph] #update the dictionary


    def characters(self, data):
        """
        read the characters as data for each tag
        Parameter:
        data (str)
        """
        if self.CurrentData == "P":
            self.paragraph += " " +data.replace("\n", "")
        elif self.CurrentData == "HEADLINE":
            self.headline += data.replace("\n","")
        elif self.CurrentData == "TEXT":
            self.paragraph += " " +data.replace("\n", "")
        


    def clearFields(self):
        """
        clears the current docid, paragraph and headline to make buffer for next one


        """
        self.docid = ""
        self.paragraph = ""
        self.headline = ""

def get_data(xmlfile):    
    """
    extract xml file and returns the dictionary of document and the content.

    Parameters:
    xmlfile (str) : name of xml file to be parsed

    Returns:
    Dictionary
    """

    parser = xml.sax.make_parser() 
    handler = xmlParser()
    parser.setContentHandler(handler)
    parser.parse(open(xmlfile+".xml"))
    return handler.dictionary
