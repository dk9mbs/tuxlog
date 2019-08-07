import socket

class Rig:
    _sock=None
    _cfg=None

    def __init__(self,cfg, **args):
        self._cfg=cfg
        if args['mock']==None:
            self._sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._cfg['host'], self._cfg['port']))
            self._sock.settimeout(1)
        else:
            self._sock=args['mock']
        pass

    def __del__(self):
        self._sock.close()
        print('socket closed')
        pass

    def set_rig(self,command, value):
        command=str(command).upper()

        self._sock.send(bytes('%s %s\n' % (command, value), 'UTF-8' ))
        response=self._sock.recv(512).decode('UTF-8')
            
        result=response.split(' ')
        if len(result)>=2:
            return response.split(' ')[1]
        else:
            raise Exception('Wrong response from rigctld daemon => %s' % response)

    def get_rig(self, parameter):
        parameter=str(parameter).lower()

        self._sock.send(bytes('%s\n' % (parameter) , 'UTF-8'  ))
        response=self._sock.recv(512).decode('UTF-8')
        tmp=response.split('\n')
        result=list()

        for item in tmp:
            if item != "":
                result.append(item)   
        
        return result
