import axios from 'axios';


export class Tuxlog {
    static deviceType='desktop';

    static setdeviceType(type) {
        Tuxlog.deviceType=type;
    }

    static  isPhone() {
        return screen.width<=760 || Tuxlog.deviceType == 'phone' ? true : false;
    }

    static webRequestAsync (method, url, data, callBackOk, callBackErr) {
        console.log('HTTP method => '+method);

        var responseProxy = (response) => {
            var res={};
            res['data']=response.data;
            res['orgres']=response;
            callBackOk(res);
        }

        var responseProxyErr = (error) => {
            var res={};
            res['orgres']=error;
            res['statusCode']=error.response.status;
            
            callBackErr(res);
        }

        //var res=await axios.get('');

        if (method=='POST') {
            axios.post(url, data).then(responseProxy).catch(responseProxyErr);
        } else if (method=='PUT') {
            axios.put(url, data).then(responseProxy).catch(responseProxyErr);
        } else if (method=='GET') {
            axios.get(url).then(responseProxy).catch(responseProxyErr);         
        }
    }

    /*
    static async webRequestSync (method, url, data) {
        console.log('HTTP method => '+method);
        //debugger;
        if (method=='POST') {
            var res = await axios.post(url, data);
            return {'data': res.data,'orgres': res };
        } else if (method=='PUT') {
            var res = await axios.put(url, data);
            return {'data': res.data,'orgres': res };
        } else if (method=='GET') {
            var res = await axios.get(url);         
            return {'data': res.data,'orgres': res };
        }
    }
    */

}


export function ifnull(value, thenVal, elseVal ) {
    if(value==undefined) {
        return thenVal;
    } else {
        return elseVal;
    }
}

export function encodeIdToURI(value) {
    return value.replace('/','%2F')
}
