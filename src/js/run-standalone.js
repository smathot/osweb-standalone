var context = {
	confirm: null,
	debug: false,
	fullScreen: {fullscreen},
	introClick: true,
	introScreen: true,
	mimetype: '',
	name: 'ovp',
	onLog: onLogHandler,
	prompt: null,
	scaleMode: 'exactFit',
	source: '{osexp}',
	subject: 0,
	target: null
};

var log_url = {log_url};

/**
 * Launches the experiment on page load.
 */
function run_experiment() {
	var runner = osweb.getRunner('osweb_div');
	runner.run(context);
}

/**
 * Callback function for processing log data
 * @param {Object} data - The result data.
 */
function onLogHandler(data) {
	if (data === null) {
		return;
	}
	if (log_url === null) {
		console.log(data);
	} else {
		console.log('Logging');
		document.getElementById('log_frame').src = log_url + escape(JSON.stringify(data)) + '\n';
	}
}
