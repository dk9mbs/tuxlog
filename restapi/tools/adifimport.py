import sys
import re
import json
import datetime

from clientlib import RestApiClient

class AdifParserLib:
    def __init__(self,fn):
        self.fn=fn
        pass

    def __call__(self, *args, **kwargs):
        adif_str=args[0]
        mapping=args[1]
        #do not assign adif_str to another value!!!

        records=re.split("<eoh>", adif_str, flags=re.IGNORECASE)
        records=re.split("<eor>", records[1], flags=re.IGNORECASE)

        adif_recs=list()

        for rec in records:
            rec=rec.replace("\r", "").replace("\n", "").replace("\t", "").strip()

            adif_rec=self._extract_fields(rec+' <')
            if len(adif_rec) >0:

                edit_adif_rec=self.fn(adif_rec,rec,mapping, **kwargs)

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


class AdifDataTypeTools:
    @staticmethod
    def adif2date(adif_date):
        return datetime.date(year=int(str(adif_date)[0:4]), month=int(str(adif_date)[4:6]), day=int(str(adif_date)[6:8]))

    @staticmethod
    def adif2time(adif_time):
        return datetime.time(hour=int(str(adif_time)[0:2]), minute=int(str(adif_time)[2:4]), second=int(str(adif_time)[4:6]))

if __name__ == "__main__":
    rest_uid=sys.argv[1]
    rest_pwd=sys.argv[2]
    api=sys.argv[3]
    adif=sys.argv[4]
    rest=RestApiClient(api)
    rest.login (rest_uid,rest_pwd)

    fetch="""
    <restapi type="select">
        <table name="log_data_exchange_fields"/>
        <filter>
            <condition field="converter_id" operator="=" value="adif_v2"/>
            <condition field="internal_fieldname" operator="notnull"/>
            <condition field="internal_fieldname" operator="neq" value=""/>
        </filter>
    </restapi>
    """
    mapping=json.loads(rest.read_multible("log_data_exchange_fields",fetch))

    f = open(adif, "r")
    content=f.read()

    @AdifParserLib
    def test(*args, **kwargs):
        #mapping=args[2]
        #json record=args[0]
        data={}
        for k,v in args[0].items():
            fieldname=""
            for mapping in args[2]:
                if str(mapping['external_fieldname']).upper()==str(k).upper():
                    value=""
                    if mapping['internal_datatype']=="Date":
                        value=str(AdifDataTypeTools.adif2date(v))
                    elif mapping['internal_datatype']=="Time":
                        value=str(AdifDataTypeTools.adif2time(v))
                    else:
                        value=v

                    data[mapping['internal_fieldname']]=value
                    break

        data['logbook_id']=str(data['logbook_id']).lower()

        fetch=f"""
        <restapi type="select">
            <table name="log_logs"/>
            <select>
                <field name="id"/>
            </select>
            <filter type="and">
                <condition field="logbook_id" value="{data['logbook_id']}" operator="="/>
                <condition field="yourcall" value="{data['yourcall']}" operator="="/>
                <condition field="logdate_utc" value="{str(data['logdate_utc'])}" operator="="/>
                <condition field="start_utc" value="{str(data['start_utc'])}" operator="="/>
            </filter>
        </restapi>
        """
        rs=json.loads(rest.read_multible("log_logs",fetch))
        #print(data)

        if len(rs)==0:
            print(f"Importing:{data['logbook_id']} {data['yourcall']} {data['logdate_utc']} {data['start_utc']}")
            rest.create("log_logs", data)
        else:
            print(f"Dupe detected:{data['logbook_id']} {data['yourcall']} {data['logdate_utc']} {data['start_utc']}")
    test(content,mapping)


    rest.logoff()
