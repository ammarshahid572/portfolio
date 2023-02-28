var express = require('express')
var path = require('path')
var app= express();


app.set("view engine", "html");
app.use("/assets", express.static('./assets'));
app.get('/', function(req, res){
    res.sendFile(path.join(__dirname + "/index.html"));
});

app.get('/components', function(req, res){
    res.sendFile(path.join(__dirname + "/components.html"));
});


app.use(function (req, res, next) {
    console.log(req.url) // populated!
    next()
  })

  app.use(function (err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    console.log(err.message);
    res.locals.error = req.app.get("env") === "development" ? err : {};
    // render the error page
    res.status(err.status || 500);
    res.send("Error " + err.status);
  });

console.log('http://localhost:5000');
app.listen(5000);