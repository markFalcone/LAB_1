

var server_port = 65432;
var server_addr = "192.168.1.89";   // the IP address of your Raspberry PI

function client(){
	const net = require('net');
	const server = net.createServer((c) => {
	  // 'connection' listener.
	  console.log('client connected');
	  c.on('end', () => {
	    console.log('client disconnected');
	  });
	  c.write('hello\r\n');
	  c.pipe(c);
	  //console.log(c);
	});
	server.on('error', (err) => {
	  throw err;
	});
	server.listen(8124, ()=> {
	  console.log('server bound' , server.address());
	});


}

function clientCarMovement(direction){
    
    const net = require('net');
    //var input = document.getElementById("myName").value;
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${direction}`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
       // document.getElementById("greet_from_server").innerHTML = data;
        console.log(data.toString());
        var datajson = JSON.parse(data.toString()); 
        
        document.getElementById("battery-status").innerHTML = 'Power Status : ' + datajson['battery'] + ' V';
        document.getElementById("car-status").innerHTML = 'Car Status : ' + datajson['Status'];
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

function carMovement(direction){
	clientCarMovement(direction);
}

function greeting(){

    // get the element from html
    console.log('here');
    var name = document.getElementById("myName").value;
    // update the content in html
    document.getElementById("greet").innerHTML = "Hello " + name + " !";
    // send the data to the server 
    //to_server(name);
    client();

}
