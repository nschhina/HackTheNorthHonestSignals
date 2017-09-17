// If absolute URL from the remote server is provided, configure the CORS
// header on that server.
var url = './helloworld3.pdf';

var audioArray = [];
var recorder;
var context = new AudioContext();

window.URL = window.URL || window.webkitURL;
navigator.getUserMedia  = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

// The workerSrc property shall be specified.
PDFJS.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';

var pdfDoc = null,
    pageNum = 1,
    pageRendering = false,
    pageNumPending = null,
    scale = 0.8,
    canvas = document.getElementById('the-canvas'),
    ctx = canvas.getContext('2d');

/**
 * Get page info from document, resize canvas accordingly, and render page.
 * @param num Page number.
 */
function renderPage(num) {
  pageRendering = true;
  // Using promise to fetch the page
  pdfDoc.getPage(num).then(function(page) {
    var viewport = page.getViewport(scale);
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    // Render PDF page into canvas context
    var renderContext = {
      canvasContext: ctx,
      viewport: viewport
    };
    var renderTask = page.render(renderContext);

    // Wait for rendering to finish
    renderTask.promise.then(function() {
      pageRendering = false;
      if (pageNumPending !== null) {
        // New page rendering is pending
        renderPage(pageNumPending);
        pageNumPending = null;
      }
    });
  });

  // Update page counters
  document.getElementById('page_num').textContent = pageNum;
}

/**
 * If another page rendering in progress, waits until the rendering is
 * finised. Otherwise, executes rendering immediately.
 */
function queueRenderPage(num) {
  if (pageRendering) {
    pageNumPending = num;
  } else {
    renderPage(num);
  }
}

/**
 * Asynchronously downloads PDF.
 */
PDFJS.getDocument(url).then(function(pdfDoc_) {
  pdfDoc = pdfDoc_;
  document.getElementById('page_count').textContent = pdfDoc.numPages;

  // Initial/first page rendering
  renderPage(pageNum);
});

/**
 * Displays next page.
 */
function onNextPage() {
  stopSlideRecording();
  console.log(pageNum + " " + pdfDoc.numPages);
  if (pageNum >= pdfDoc.numPages) {
    document.getElementById('next').disabled = true;
    console.log("Sending to Python Backend");
    console.log(audioArray);
    var form = new FormData();
    form.append('file', audioArray[0], 'one.wav');
    var xmlhttp=new XMLHttpRequest();
    var url = "accessdata";
    xmlhttp.open("POST",url,true);
    xmlhttp.send(form);

    /*$.ajax({
      type: 'POST',
      url: 'ServerURL',
      data: form,
      cache: false,
      processData: false,
      contentType: false
    }).done(function(data){
      console.log("Sent");
      console.log(data);
    })*/
    //need to ajax to python from here...
    return;
  }
  else if(pageNum == pdfDoc.numPages-1) {
    document.getElementById('next').textContent = "Submit";
  }
  else {
    startSlideRecording();
  }
  pageNum++;
  queueRenderPage(pageNum);
}
document.getElementById('next').addEventListener('click', onNextPage);

var onSuccess = function(s) {
    var mediaStreamSource = context.createMediaStreamSource(s);
    console.log(mediaStreamSource);
    recorder = new Recorder(mediaStreamSource);
    recorder.record();
    // audio loopback
    // mediaStreamSource.connect(context.destination);
}

var onFail = function(e) {
  console.log('Rejected!', e);
};

function startSlideRecording() {
  if (navigator.getUserMedia) {
    navigator.getUserMedia({audio: true}, onSuccess, onFail);
  } else {
    console.log('navigator.getUserMedia not present');
  }
}

function stopSlideRecording() {
  recorder.stop();
  recorder.exportWAV(function(s) {
    console.log(s);
    audioArray.push(s);
    var wUrl = window.URL.createObjectURL(s);
    //audioArray.push(wUrl);
    console.log(audioArray);
    //audio.src = wUrl;
  });
}

// on load
startSlideRecording();
