var express = require('express')
var app = express()

var port = process.env.PORT || 8080;

app.get('/.well-known/acme-challenge/SImgd24WRS64hT8QsPGFVLay1nmGM_IO6WLrBGvr9QA', function(req, res) {
    res.send('SImgd24WRS64hT8QsPGFVLay1nmGM_IO6WLrBGvr9QA.4UzW-_pc32ZB01RhhqCtjeRfzy6vbluKquABtpYww-Q')
})

app.get('/.well-known', function(req, res) {
    res.send('SImgd24WRS64hT8QsPGFVLay1nmGM_IO6WLrBGvr9QA.4UzW-_pc32ZB01RhhqCtjeRfzy6vbluKquABtpYww-Q')
})

app.listen(port, function () {
    console.log('Example app listening port ' + port)
})
