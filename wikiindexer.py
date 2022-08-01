import timeit
import xml.sax

def titleWrite(title_data, file_count):
    fp1=open("temp/title"+str(file_count),"w")
    fp1.write(title_data)
    fp1.write("\n")

class WikiHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.title=0
        self.title_data = ""
        self.page_count = 0
        self.file_count = 0
    
    def startElement(self,tag,attr):
        if(tag == "page"):
            self.page_count = self.page_count + 1
        if(tag == "title"):
            self.title = 1

    def characters(self, content):
        if(self.title == 1):
            self.title_data += content
        if self.page_count > 20000:
            titleWrite(self.title_data, self.file_count)
            self.page_count = 0
            self.file_count = self.file_count + 1
            title_data = ""

    def endElement(self, tag):
        if(tag == "title"):
            self.title = 0

def main():
    global fp
    fp=open("temp/title_offset","w")
    par=xml.sax.make_parser()
    Handler = WikiHandler()
    par.setFeature(xml.sax.handler.feature_namespaces,0)
    par.setContentHandler( Handler )
    par.parse('data.xml')



if __name__ == "__main__":                                            #main
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print (stop - start)
