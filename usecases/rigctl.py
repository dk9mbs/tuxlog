import socket
import logging

logger=logging.getLogger(__name__)

class RigCtl:
    _sock=None
    _cfg=None

    def __init__(self,cfg, **args):
        self._cfg=cfg
        if not 'mock' in args :
            try:
                self._sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._sock.settimeout(1)
                self._sock.connect((self._cfg['host'], self._cfg['port']))
                self._sock.settimeout(5)
            except Exception as e:
                logger.exception(e)
                raise
        else:
            self._sock=args['mock']
        pass

    def __del__(self):
        self._sock.close()
        pass

    def set_rig(self,command, value_list):
        command=str(command).upper()

        self._sock.send(bytes('%s\n' % command, 'UTF-8' ))

        for para in value_list:
            if para != None:
                self._sock.send(bytes('%s\n' % para, 'UTF-8' ))


        response=self._sock.recv(512).decode('UTF-8')
            
        result=response.split(' ')
        if len(result)>=2:
            return response.split(' ')[1]
        else:
            raise Exception('Wrong response from rigctld daemon => %s' % response)

    def get_rig(self, parameter):
        parameter=str(parameter).lower()
        if not str(parameter).startswith('+'):
            parameter='+%s' % parameter

        self._sock.send(bytes('%s\n' % (parameter) , 'UTF-8'  ))
        response=self._sock.recv(512).decode('UTF-8')
        tmp=response.split('\n')

        result=dict()
        result_item=dict()
        for item in tmp:
            if item.startswith('RPRT'):
                result['result']=str(item.replace('RPRT','')).strip()
            elif str(item.strip()).endswith(':'):
                result['command']=item.replace(':','')
            else:
                keyvalue=item.split(':')
                if len(keyvalue) == 2:
                    key=keyvalue[0].strip()
                    value=keyvalue[1].strip()
                    if key!='':
                        result_item[key]=value   
        
        result['response']=result_item
        return result
