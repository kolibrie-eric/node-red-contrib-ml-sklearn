module.exports = function (RED) {
    function dataframeNode(config) {
        const utils = require('../../utils/utils')

        const node = this;

        //set configurations
        node.file = __dirname + '/dataframe.py'
        node.topic = 'predicted'
        node.config = {
            name: config.name,
            rules: config.rules,
            orient: config.orient
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("dataframe", dataframeNode)
}
