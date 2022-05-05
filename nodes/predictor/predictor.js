module.exports = function (RED) {
  function predictorNode(config) {
    const path = require('path')
    const utils = require('../../utils/utils')

    const node = this;

    //set configurations
    node.file = __dirname + '/predictor.py'
    node.topic = 'predicted'
    node.config = {
      name: config.name,
      file: config.modelfile
    }

    utils.run(RED, node, config)
  }
  RED.nodes.registerType("predictor", predictorNode)
}
