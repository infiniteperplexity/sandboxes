const dispatcher = require('httpdispatcher');
const http = require('http');

const PORT=8080;

function handleRequest(request, response) {
  try {
    //log the request to the console
    console.log(request.url);
    //dispatch
    dispatcher.dispatch(request, response)
  } catch(err) {
    console.log(err);
  }
}
// For all your static resources, set the directory name (relative path)
dispatcher.setStatic('resources');

// A sample GET request
dispatcher.onGet("/page1", function(req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Page One');
});

// A sample POST request
dispatcher.onPost("/post1", function(req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Got Post Data')
});


const server = http.createServer(handleRequest);

server.listen(PORT, function () {
  console.log("Server listening on http://localhost:%s",PORT);
});
