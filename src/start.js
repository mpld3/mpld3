/* mpld3.js: javascript backend for displaying interactive matplotlib plots */
/*   Author: Jake Vanderplas                                                */
/*   License: 3-clause BSD (see http://github.com/jakevdp/mpld3)            */
/*                                                                          */
/* Notes:                                                                   */
/* - the objects here use prototype-based definitions rather than           */
/*   closure-based definitions for the sake of memory efficiency.           */
/*                                                                          */
/* - this assumes that d3 is defined in the global namespace, and the       */
/*   result is that mpld3 is defined in the global namespace.               */
/*                                                                          */

!function(d3) {
    var mpld3 = {
        figures: [],
        plugin_map: {},
        register_plugin: function(name, obj) {
            mpld3.plugin_map[name] = obj;
        }
    };

