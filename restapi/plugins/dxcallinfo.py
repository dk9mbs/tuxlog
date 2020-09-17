#from model.model import LogDxccPrefixes
import logging

from core.fetchxmlparser import FetchXmlParser
from services.database import DatabaseServices


logger = logging.getLogger(__name__)

class DxCallInfo:

    def __init__(self):
        pass

    @classmethod
    def get_dxinfo_by_call(cls,context, callsign):
        callsign=callsign.replace('-', '/').strip().upper()

        prefix=""
        postfix=""
        call_info=dict()

        call_info['complete']=callsign

        parts=callsign.split('/')
        if len(parts)==3:
            prefix=parts[0]
            callsign=parts[1]
            postfix=parts[2]

        if len(parts)==2:
            if len(parts[0]) < len(parts[1]):
                prefix=parts[0]
                callsign=parts[1]
            else:
                callsign=parts[0]
                postfix=parts[1] 

        call_info['prefix']=prefix
        call_info['call']=callsign
        call_info['postfix']=postfix

        # look for the complete call 
        dxinfo=DxCallInfo.get_prefix_by_call(context, call_info['complete'])
        if dxinfo!=None:
            return dxinfo
            #return DxCallInfo.model_to_dict(dxinfo, call_info)

        for x in range(len(call_info['complete'])):
            part=call_info['complete'][:x*-1]
            dxinfo=DxCallInfo.get_prefix_by_call(context,part)
            if dxinfo!=None:
                return dxinfo
                #return DxCallInfo.model_to_dict(dxinfo, call_info)

        return None

    @classmethod
    def get_prefix_by_call(cls, context, call):
        fetch=f"""
        <restapi type="select">
            <table name="log_dxcc_prefixes"/>
            <filter>
                <condition field="id" value="{call}" operator="="/>
            </filter>
        </restapi>
        """

        fetchparser=FetchXmlParser(fetch, context)
        rs=DatabaseServices.exec(fetchparser, context, fetch_mode=1)
        result=rs.get_result()
        rs.close()
        #print(result)
        return result

    @classmethod
    def model_to_dict(cls, dxcc_model, info_dict):
        info_dict['country']=dxcc_model.dxcc.country
        info_dict['itu_zone']=dxcc_model.itu_zone
        info_dict['cq_zone']=dxcc_model.cq_zone
        info_dict['main_prefix']=dxcc_model.dxcc_id
        info_dict['continent']=dxcc_model.dxcc.continent
        info_dict['entity']=dxcc_model.entity
        info_dict['time_offset']=dxcc_model.time_offset
        info_dict['latitude']=dxcc_model.dxcc.latitude
        info_dict['longitude']=dxcc_model.dxcc.longitude
        return dxcc_model
        #return info_dict

