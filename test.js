var express = require('express')
var app = express()

var port = process.env.PORT || 8080;

app.get('/.well-known/acme-challenge/Evvr5kg3GH0LoP5KNQAjowLJM2yY9ikYy2qNJazpeHo', function(req, res) {
    res.send('Evvr5kg3GH0LoP5KNQAjowLJM2yY9ikYy2qNJazpeHo.4UzW-_pc32ZB01RhhqCtjeRfzy6vbluKquABtpYww-Q')
})

app.listen(port, function () {
    console.log('Example app listening port ' + port)
})
