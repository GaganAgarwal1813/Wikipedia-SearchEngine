import timeit
import xml.sax
class WikiHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.title=0
    def startElement(self,tag,attr):
        self.current = tag
        
    def characters(self, content):
        if(self.current == "title"):
            fp.write(content)
            fp.write("\n")
    def endElement(self, tag):
        self.current = ""

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
