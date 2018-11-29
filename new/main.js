 
var express = require('express'); 
var app = express(); 
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));

app.set('view engine', 'ejs');

app.get('/', function (req, res, next) {
res.render('main.ejs',{
});
});

app.listen(3000, function() { 
    console.log('server running on port 3000'); 
} ) 

app.post('/', callName); 
  
function callName(req, res) { 
    
    var spawn = require("child_process").spawn; 
      
    var process = spawn('python',["auto_enc.py", req.body.studid,req.body.sem] ); 
     
    
    process.stdout.on('data', function(data) { 
      var s=JSON.parse(data.toString());
    	res.render('submit.ejs',{
 			'requests':s
          });
    } ) 
} 