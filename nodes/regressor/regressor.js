module.exports = function (RED) {
    function regressorNode(config) {
        const utils = require('../../utils/utils')
        let node = this;

        //set configurations
        node.file = __dirname + '/regressor.py'
        node.config = {
            name: config.name,
            algorithm: config.algorithm,
            parameters: config.rules,
            debug: config.debug,
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("regressor", regressorNode);
}
