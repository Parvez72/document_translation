var express = require('express');
var router = express.Router();
var html2json = require('html2json').html2json;
var json2html = require('html2json').json2html;
var fs = require('fs');
var http = require('http')
var download = require('download-pdf')
var mammoth = require('mammoth')
var Client = require('node-rest-client').Client;
var pdf = require('html-pdf')
var request = require('request')





var client = new Client();

//https://cdn.yellowmessenger.com/GRi0FJ8Xt5fY1531562873479.docx

var options = {
    directory: "./",
    filename: "file.docx"
}

let log = (message, name)=>{
  console.log(name+": {\n"+message+"\n}");
}

let createPdf = (htmldata)=>{
    return new Promise(resolve => {
        pdf.create(htmldata, {format:'Letter'}).toFile('./businesscard.pdf', function(err, res) {
            if (err) return console.log(err);
            var formData = {

                file: fs.createReadStream('./businesscard.pdf'),

            };
            //console.log(formData,'pdf File name'); // { filename: '/app/businesscard.pdf' }
            request.post({url:'https://chat.botplatform.io/upload-file?json=true', formData: formData}, function optionalCallback(err, httpResponse, body) {
                if (err) {
                    return console.error('upload failed:', err);
                }
                else{
                    console.log(body,"body");
                    resolve(JSON.parse(body).url)
                }

            });

        })
    })
}

let convert = function(){
    return new Promise(resolve => {
        mammoth.convertToHtml({path: "./file.docx"})
            .then(function(result) {
                var html = result.value; // The generated HTML
                var messages = result.messages; // Any messages, such as warnings during conversion
                var jsonText = html2json(html)
                var args ={
                    data:jsonText,
                    headers: { "Content-Type": "application/json" }
                }
                client.post('http://127.0.0.1:5000/jsontoarray/',args,function (data, res) {
                    console.log(data,"converted data")
                    createPdf(json2html(data)).then((result)=>{
                        console.log(result)
                        resolve(result)
                    })
                },function (err) {
                    if(err) reject(err)
                })
            })
    }).catch(e=>{
        console.log(e)
    })
}

/* GET home page. */
router.get('/', function(req, res, next) {
    console.log(req.params)
  res.render('index', { title: 'Express' });
});

router.get('/getDoc',function (req, res, next) {
    mammoth.convert({path:'./file.docx'}).then(function (result) {
        pdf.create(result.value, {format:'Letter'}).toFile('./businesscard.pdf', function(err, res) {
            if (err) return console.log(err);
            console.log(res); // { filename: '/app/businesscard.pdf' }
        });
        res.send(result.value)
    })

})
router.post('/translateDoc/',function (req, res, next) {
    console.log(req.query,"incoming query")
    let url = req.query.url

    download(url, options, function(err){
            convert().then((result)=>{
                console.log(result,"result from convert")
                res.send(result)
            })
        })


})

module.exports = router;
