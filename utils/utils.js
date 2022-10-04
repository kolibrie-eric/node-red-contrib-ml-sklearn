const status = require('./status.js');
const { spawn } = require('child_process');
const { notStrictEqual } = require('assert');
const { networkInterfaces } = require('os');

//use 'python3' on linux and 'python' on anything else
const pcmd = process.platform === 'linux' ? 'python3' : 'python';

//initialize child process
const create_python_process = (node) => {
	if (node.proc === undefined) {
		// node.file contains the python script to execute
		node.proc = spawn(pcmd, [node.file]);

		// Handle results
		node.proc.stdout.on('data', (data) => {
			let msg = {};
			try {
				// Try to parse the return string as a JSON string
				// If it is not a JSON string it will throw an exception
				data = JSON.parse(data);

				// Process the parameters passed back to this function
				Object.entries(data).forEach(item => {
					try {
						// Try a JSON parse
						msg[item[0]] = JSON.parse(item[1]);
					}
					catch (err) {
						// We'll end up here when the item value is not a JSON string
						msg[item[0]] = item[1].toString();
					}
				})
			}
			catch (err) {
				// JSON parse not succesfull. Just return the result string
				msg.payload = data.toString();
				msg.topic = "string received";
				msg.status = status.DONE;
			}
			node.status({ fill: "green", shape: "dot", text: msg.status });
			delete msg.status;

			if (msg.payload !== null)
				node.send(msg)
		})

		// Handle errors and debug messages
		node.proc.stderr.on('data', (data) => {
			let s = data.toString();

			// Is this a debug message from the python process?
			if (s.includes("#log#")) {
				// Remove the identification string that makes this a debug message
				s = s.replace(/#log#\s*/, "");

				// Remove the trailing /n if necessary
				s = s.replace(/[\n\r]+$/, "");

				// Add a end of line after the first semicolon (after filename and line number)
				s = s.replace(/=/, "=\n")

				// Notify nodered
				node.warn(s);
			}
			else {
				node.status(status.ERROR);
				node.error(data.toString());
			}
		})

		// Handle crashes
		node.proc.on('exit', () => {
			delete node.proc;
		})
	}
}

module.exports = {
	// Initialize node
	run: (RED, node, config) => {
		RED.nodes.createNode(node, config);
		node.status(status.NONE);

		// Use the user directory as the default path to store 
		node.config.path = RED.settings.userDir;

		// The id of the node is used to give the model file a unique name
		node.config.id = node.id;

		// Initalize child process
		create_python_process(node);

		// Send the configuration and parameters to child process 
		node.proc.stdin.write(JSON.stringify(node.config) + '\n');

		// Handle input
		node.on('input', (msg) => {
			node.status(status.PROCESSING);
			create_python_process(node);

			// Go through all the message properties and add everything but the 
			// standard properties to the kwargs argument passed to the python script
			let kwargs = {};
			for (const [key, value] of Object.entries(msg)) {
				if (key != 'payload' && key != 'topic' && key != '_msgid') {
					kwargs[key] = value;
				}
			}

			// Send the message to the python script
			const args = { payload: JSON.stringify(msg.payload), topic: msg.topic, kwargs: kwargs };

			// Send message to child process (containing the data)
			node.proc.stdin.write(JSON.stringify(args) + '\n');
		})

		// When node is closed, kill child process
		node.on('close', (done) => {
			node.status(status.NONE);
			if (node.proc != null) {
				node.proc.kill();
				node.proc = null;
			}
			done();
		})
	}
}
