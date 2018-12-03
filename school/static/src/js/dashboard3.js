odoo.define('school.dashboard3', function (require) {
"use strict";

var ControlPanelMixin = require('web.ControlPanelMixin');
var Widget = require('web.Widget');
var core = require('web.core');


var SplitAction = Widget.extend(ControlPanelMixin, {
    title: core._t('Bank reconciliation'),
    template: 'dashboard3',


    start: function() {
        var self = this;
        self._rpc({
                route: '/dashboard3',
                params: {
                },
            })
    },
});

core.action_registry.add('dashboard3', SplitAction);

return {
    SplitAction: SplitAction,

};


});