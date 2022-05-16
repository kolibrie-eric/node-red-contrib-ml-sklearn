module.exports = function (RED) {
  function predictorNode(config) {
    const utils = require('../../utils/utils')

    const node = this;

    //set configurations
    node.file = __dirname + '/predictor.py'
    node.topic = 'predicted'
    node.config = {
      name: config.name,
      orient: config.orient,
      y_column: config.y_column
    }

    utils.run(RED, node, config)
  }
  RED.nodes.registerType("predictor", predictorNode)
}
