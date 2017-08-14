var smash = require("smash"),
    jsdom = require("jsdom");

global.document = jsdom.jsdom("<html><head></head><body></body></html>");

var d3 = require("d3");

module.exports = function() {
  var files = [].slice.call(arguments).map(function(d) { return "src/" + d; }),
      expression = "mpld3",
      sandbox = {console: console, d3: d3}; 

  files.unshift("src/start");
  files.push("src/version");
  files.push("src/end");

  function topic() {
    var callback = this.callback;
    smash.load(files, expression, sandbox, function(error, result) {
      if (error) console.trace(error.stack);
      callback(error, result);
    });
  }

  topic.expression = function(_) {
    expression = _;
    return topic;
  };

  topic.sandbox = function(_) {
    sandbox = _;
    return topic;
  };

  topic.document = function(_) {

    sandbox = {
      d3 : d3, 
      console: console,
      document: document,
      window: document.defaultView
    };

    return topic;
  };

  return topic;
};

process.on("uncaughtException", function(e) {
  console.trace(e.stack);
});
