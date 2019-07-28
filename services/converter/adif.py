import re

class AdifParserService:
    def __init__(self,fn):
        self.fn=fn
        pass

    def __call__(self, *args, **kwargs):
        adif_str=args[0]
        #do not assign adif_str to another value!!!  
        adif=adif_str.replace("\r", "")
        adif=adif_str.replace("\n", "")
        adif=adif_str.replace("\t", "")

        records=str(adif).split("<eoh>")
        records=str(records[1]).split("<eor>")

        for rec in records:
            adif_rec=self._extract_fields(rec)
            if len(adif_rec) >0:
                self.fn(adif_rec, **kwargs)

    def _extract_fields(self, adif_record):
        attr = re.findall(r"(.*?):(\d)>(.*?)\s(<.*?)", adif_record) 
        json={}         
        for m in attr:
            name=str(m[0]).replace("<","")
            value=m[2]
            json[name]=value  

        return json


if __name__ == "__main__":
    
    f = open("/tmp/wsjtx_log.adi", "r")
    content=f.read()

    @AdifParserService
    def test(*args, **kwargs):
        print("Test => " + str(args[0]))

    test(content)

    #f = open("c:\\temp\\wsjtx_log.adi", "r")
    #content=f.read()
    #parser=AdifParser2()
    #@parser.parse("")
    #def test(*args, **kwargs):
    #    print(type(*args))
    #    print (*args, **kwargs)
        
    #test(content)
