let context = {
	confirm: null,
	debug: false,
	fullScreen: {fullscreen},
	introClick: false,
	introScreen: false,
	mimetype: '',
	name: 'osweb',
	onLog: onLogHandler,
	onFinished: onFinishedHandler,
	prompt: null,
	scaleMode: 'exactFit',
	source: null,
	subject: 0,
	target: null
};

let taskData = ''

/**
 * Converts base-64-encoded data to a File object, which can be passed to
 * osweb as an experiment file
 **/
function URItoFile(uri) {
  let byteCharacters = atob(uri.split(',')[1])
  let byteArrays = []
  for (let offset = 0; offset < byteCharacters.length; offset += 512) {
    let slice = byteCharacters.slice(offset, offset + 512);
    let byteNumbers = new Array(slice.length)
    for (let i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i)
    }
    let byteArray = new Uint8Array(byteNumbers)
    byteArrays.push(byteArray)
  }
  let blob = new Blob(byteArrays)
  return new File([blob], "osexp_src")
}

/**
 * Is called on page load to launch the experiment
 */
function run_experiment() {
	context.source = URItoFile(document.getElementById('osexp_src').src)
	let runner = osweb.getRunner('osweb_div')
	runner.run(context)
}

/**
 * Callback function for processing log data
 * @param {Object} data - The result data.
 */
function onLogHandler(data) {
	if (data === null) {
		return
	}
	taskData = taskData + JSON.stringify(data) + '\n'
}

/** Callback function for processing after an experiment is finished.
 * @param {Object} data - The result data.
 * @param {Object} sessionData - The session data.
 */
function onFinishedHandler(data, sessionData) {
  Qualtrics.SurveyEngine.setEmbeddedData('taskdata', taskData)
  document.getElementById("osweb_div").style.display = "none"
  Qualtrics.SurveyEngine.Page.pageButtons.showNextButton()
}

Qualtrics.SurveyEngine.addOnload(run_experiment)
