odoo.define('school.dashboard1', function (require) {
"use strict";

var ControlPanelMixin = require('web.ControlPanelMixin');
var Widget = require('web.Widget');
var core = require('web.core');


var SplitAction = Widget.extend(ControlPanelMixin, {
    title: core._t('Bank reconciliation'),
    template: 'dashboard1',

//        events: {
//            "click": "CreStartRedirect",
//        },

    start: function() {
        var self = this;
        self._rpc({
                route: '/dashboard1',
                params: {
                },
            })
    },


//    CreStartRedirect: function (e) {
//        e.stopImmediatePropagation();
//        var start_current_id = e.currentTarget.childNodes[1].innerHTML;
//        var model_name = e.currentTarget.childNodes[2].innerHTML;
//        return ajax.jsonRpc('/start_button', 'call', {
//             'start_click_id': start_current_id,'model_name':model_name})
//        .then(function (data) {
//            //console.log('start',data['model']);
//            self.do_action({
//            type: 'ir.actions.client',
//            tag: 'dashboard1'
//            });
//        });
//    },


});

core.action_registry.add('dashboard1', SplitAction);

return {
    SplitAction: SplitAction,

};


});