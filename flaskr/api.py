
def create_var_list(call, api_config, request):    
    if call in api_config:
        varnames=[]

        if len(request.args) > 0:
            for k, v in request.args.items(): 
                if k in api_config[call]:                    
                    varnames.append(api_config[call][k]['var'])   
        else:
            for val in api_config[call].values():        
                varnames.append(val['var'])                        
        return varnames
    return None

def create_response(result, call, api_config):
    response={}
    for key, val in api_config[call].items():   
        if resp := result.get(val['var']) != None:
            response[key] = resp
    return response

def omit_apiinfo_var_name(api_info):
    for api in api_info.values():
        for entry in api.values():
            entry.pop("var")
    return api_info 