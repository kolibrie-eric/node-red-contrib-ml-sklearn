module.exports = function (RED) {
    function regressorNode(config) {
        const utils = require('../../utils/utils')
        let node = this;

        //set configurations
        node.file = __dirname + '/trainer.py'
        node.config = {
            name: config.name,
            algorithm: config.algorithm
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("regressor", regressorNode);
}
