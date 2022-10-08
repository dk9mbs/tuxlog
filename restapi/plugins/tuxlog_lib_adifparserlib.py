import sys
import re

class AdifParserLib:
    def __init__(self,fn):
        self.fn=fn
        pass

    def __call__(self, *args, **kwargs):
        adif_str=args[0]
        rec_count=args[1]
        #do not assign adif_str to another value!!!

        records=re.split("<eoh>", adif_str, flags=re.IGNORECASE)
        records=re.split("<eor>", records[1], flags=re.IGNORECASE)

        adif_recs=list()

        for rec in records:
            rec=rec.replace("\r", "").replace("\n", "").replace("\t", "").strip()

            adif_rec=self._extract_fields(rec+' <')
            if len(adif_rec) >0:

                edit_adif_rec=self.fn(adif_rec,rec,rec_count, **kwargs)

                if edit_adif_rec != None:
                    adif_recs.append(edit_adif_rec)
                else:
                    adif_recs.append(adif_rec)

        return adif_recs

    def _extract_fields(self, adif_record):
        attr = re.findall(r"(.*?):(\d{1,})>(.*?)\s(<.*?)", adif_record)
        json={}
        for m in attr:
            name=str(m[0]).replace("<","")
            value=m[2]
            json[name]=value

        return json





if __name__ == "__main__":

    f = open("/tmp/wsjtx_log.adi", "r")
    content=f.read()

    @AdifParserLib
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
