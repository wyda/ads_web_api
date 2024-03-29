# ads_web_api

Simple web API interface build with [flask](https://flask.palletsprojects.com/en/2.2.x/) to give access to data on a Beckhoff PLC.  
The whole API interface can be descriped in a single text file.  
Option to read directly by PLC variable name.  
  
For reading the PLC data [pyads](https://github.com/stlehmann/pyads) is used.  

## API definition structure  
The API is defined by one or more calls of which each contains a number of data request points.  

```
{
  "request_1": {
    "data_access_point1": {
      "var": "Main.MyTestVar1",
      "lable": "Var1",
      "description": "Explain what informaiton you provide here"
    },
    "data_access_point2": {
      "var": "Main.MyTestVar2",
      "lable": "Var2",
      "description": "Explain what informaiton you provide here"
    }
  },
  "request_2": {
    ...
  }
}
```

## Example requests  
### Request request_1  
localhost:5000/api/request_1  
### Response  
```
{
  "data_access_point1": 132.32,
  "data_access_point2": true,
}
```

### It's possible to request a single data point or a list of data points
 localhost:5000/api/request_1?data_access_point1  
### Response 
```
{
  "data_access_point1": 132.32,
}
```

### Request the API description  
localhost:5000/api/apiinfo  
### Response 
The variable names are ommited in the response if "omit_var_names" is set to true in config.json  
```
{
  "request_1": {
    "data_access_point1": {
      "var": "Main.MyTestVar1",
      "lable": "Var1",
      "description": "Explain what informaiton you provide here"
    },
    "data_access_point2": {
      "var": "Main.MyTestVar2",
      "lable": "Var2",
      "description": "Explain what informaiton you provide here"
    }
  },
  "request_2": {
    ...
  }
}
```

### Request values directly by PLC variable names
This needs to be allowed in config.json by setting "allow_var_req" to true

localhost:5000/api/readvar?Main.MyTestVar1&Main.MyTestVar2  

### Response 
```
{
  "Main.MyTestVar1": 132.32,
  "Main.MyTestVar2": true,
}
```

## Deploing  
Before deployng checkout [flask home page](https://flask.palletsprojects.com/en/2.2.x/deploying/)  
### Test setup  
To run the app for the first time in local development mode run the following commands (PowerShell):  
* git clone https://github.com/wyda/ads_web_api.git  
* pip install ads_web_api -r requirements.txt  
* $env:FLASK_APP='ads_web_api'  
* $env:FLASK_ENV='development'  
* flask create_config -> enter ams address to the created config file (instance folder)   
* flask create_api -> write your API definition to the created file (instance folder)  
* flask init-db  
* flask run  
  
You should now be able to query information according your api devinition from your local machine.   
The PLC must run on the same PC.  
If you change values in the config.json file run "flask reload-config" to load the changes to the db.  
  
To access the server from an external device (testing only!):  
* flask --host "your ip" run  

See also development server on the [flask homepage](https://flask.palletsprojects.com/en/2.2.x/server/) for more information.  
### Production setup  
...  