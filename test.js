var express = require('express')
var app = express()

var port = process.env.PORT || 8080;

app.get('/.well-known/acme-challenge/RAOuLKyi7piLbITEq3p1wzTn8L4-s8VigZe499NJajo', function(req, res) {
    res.send('RAOuLKyi7piLbITEq3p1wzTn8L4-s8VigZe499NJajo.4UzW-_pc32ZB01RhhqCtjeRfzy6vbluKquABtpYww-Q')
})

app.listen(port, function () {
    console.log('Example app listening port ' + port)
})
