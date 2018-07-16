var request = require('request')
var fs = require('fs')


var formData = {

    file: fs.createReadStream(__dirname + '/businesscard.pdf'),

};

request.post({url:'https://chat.botplatform.io/upload-file', formData: formData}, function optionalCallback(err, httpResponse, body) {
    if (err) {
        return console.error('upload failed:', err);
    }
    console.log(body.split('"')[5]);
});
