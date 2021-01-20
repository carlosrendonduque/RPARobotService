
var express = require('express'); // Web Framework
var app = express();
var sql = require('mssql'); // MS Sql Server client
//https://www.youtube.com/watch?v=T2cdL-KvVaY&list=PLqhnP4YYLcb4X3AgmW699wyAhoP2SYf5j
// Connection string parameters.
var sqlConfig = {
    server : '172.17.7.26', 
    database : 'Adv_Condor_soporte', 
    user : 'usuariodms', 
    password : 'Usu2017*dms' 
}

// Start server and listen on http://localhost:8081/
var server = app.listen(8081, function () {
    var host = server.address().address
    var port = server.address().port

    console.log("app listening at http://%s:%s", host, port)
});

app.get('/jobs', function (req, res) {
    sql.connect(sqlConfig, function() {
        var request = new sql.Request();
        request.query('select * from RPA_GetCnsValidacionJornadasTope', function(err, recordset) {
            if(err) console.log(err);
            res.end(JSON.stringify(recordset)); // Result in JSON format
        });
    });
})


app.get('/customers/:customerId/', function (req, res) {
    sql.connect(sqlConfig, function() {
        var request = new sql.Request();
        var stringRequest = 'select * from RPA_GetCnsValidacionJornadasTope customerId = ' + req.params.customerId;
        request.query(stringRequest, function(err, recordset) {
            if(err) console.log(err);
            res.end(JSON.stringify(recordset)); // Result in JSON format
        });
    });
})


app.get('/customers/:customerId/orders', function (req, res) {
    sql.connect(sqlConfig, function() {
        var request = new sql.Request();
        request.input('CustomerId', req.params.customerId);
        request.execute('Sales.uspShowOrderDetails', function(err, recordsets, returnValue, affected) {
            if(err) console.log(err);
            res.end(JSON.stringify(recordsets)); // Result in JSON format
        });
    });
})