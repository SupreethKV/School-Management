odoo.define('school.dashboard2', function (require) {
"use strict";

var ControlPanelMixin = require('web.ControlPanelMixin');
var Widget = require('web.Widget');
var core = require('web.core');


var SplitAction = Widget.extend(ControlPanelMixin, {
    title: core._t('Bank reconciliation'),
    template: 'dashboard2',


    start: function() {
        var self = this;
        self._rpc({
                route: '/dashboard2',
                params: {
                },
            })
    },
});

core.action_registry.add('dashboard2', SplitAction);

return {
    SplitAction: SplitAction,

};


});