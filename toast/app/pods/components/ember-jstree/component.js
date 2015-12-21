import Ember from 'ember';
import EmberJstree from 'ember-cli-jstree/components/ember-jstree';

export default EmberJstree.extend({
    _setupJsTree() {
        var config = {};

        config.core = {
            'data': this.get('data'),
            'check_callback': this.get('checkCallback')
        };

        var themes = this.get('themes');
        if (themes && typeof themes === 'object') {
            configObject.core.themes = themes;
        }

        var pluginsArray = this.get('plugins');
        if(pluginsArray) {
            let self = this;
            pluginsArray = pluginsArray.replace(/ /g, '').split(',');
            config.plugins = pluginsArray;

            if (pluginsArray.indexOf('contextmenu') !== -1 ||
                pluginsArray.indexOf('dnd') !== -1 ||
                pluginsArray.indexOf('unique') !== -1) {
                // These plugins need core.check_callback
                config.core.check_callback = true;
            }

            pluginsArray.forEach(plugin => {
                if (self.get(`${plugin}Options`))
                    config[plugin] = self.get(`${plugin}Options`);
            });

            config.contextmenu = this._setupContextMenus(pluginsArray);
            config.search = {'search_callback' : this.searchCallback.bind(this)};
        }

        return this.$().jstree(config);
    }
});
