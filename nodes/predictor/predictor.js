module.exports = function (RED) {
  function predictorNode(config) {
    const utils = require('../../utils/utils')

    const node = this;

    //set configurations
    node.file = __dirname + '/predictor.py'
    node.topic = 'predicted'
    node.config = {
      name: config.name,
    }

    utils.run(RED, node, config)
  }
  RED.nodes.registerType("predictor", predictorNode)
}
