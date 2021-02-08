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

if (!d3) {
    var d3 = require('d3');
}

    var mpld3 = {
        _mpld3IsLoaded: true,  // used when loading lib in case global variable mpld3 is set to something else
        figures: [],
        plugin_map: {},
    };

