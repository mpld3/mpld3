import "core";
import "util";

/**********************************************************************/
/* Toolbar object: */
mpld3.Toolbar = mpld3_Toolbar;
mpld3_Toolbar.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Toolbar.prototype.constructor = mpld3_Toolbar;
mpld3_Toolbar.prototype.defaultProps = {
    buttons: ["reset", "move"]
};
mpld3_Toolbar.prototype.buttonDict = {}; // to be filled by ButtonFactory

function mpld3_Toolbar(fig, props) {
    mpld3_PlotElement.call(this, fig, props)
    this.buttons = [];
    this.props.buttons.forEach(this.addButton.bind(this));
}

mpld3_Toolbar.prototype.addButton = function(key) {
    var Button = this.buttonDict[key];
    if (typeof(Button) === "undefined") {
        console.warn("Skipping unrecognized Button type '" + key + "'.");
    } else {
        this.buttons.push(new Button(this, key));
    }
};

mpld3_Toolbar.prototype.draw = function() {
    mpld3.insert_css("div#" + this.fig.figid + " .mpld3-toolbar image", {
        cursor: "pointer",
        opacity: 0.2,
        display: "inline-block",
        margin: "0px"
    })
    mpld3.insert_css("div#" + this.fig.figid + " .mpld3-toolbar image.active", {
        opacity: 0.4
    })
    mpld3.insert_css("div#" + this.fig.figid + " .mpld3-toolbar image.pressed", {
        opacity: 0.6
    })

    function showButtons() {
        this.buttonsobj.transition(750).attr("y", 0);
    }

    function hideButtons() {
        this.buttonsobj.transition(750)
            .delay(250).attr("y", 16);
    }

    // buttons will be shown and hidden on mouse movements.
    // (the buttons will be also be shown on touch events.)
    this.fig.canvas
        .on("mouseenter", showButtons.bind(this))
        .on("mouseleave", hideButtons.bind(this))
        .on("touchenter", showButtons.bind(this))
        .on("touchstart", showButtons.bind(this));

    this.toolbar = this.fig.canvas.append("svg:svg")
        .attr("width", 16 * this.buttons.length)
        .attr("height", 16)
        .attr("x", 2)
        .attr("y", this.fig.height - 16 - 2)
        .attr("class", "mpld3-toolbar");

    this.buttonsobj = this.toolbar.append("svg:g").selectAll("buttons")
        .data(this.buttons)
        .enter().append("svg:image")
        .attr("class", function(d) {
            return d.cssclass;
        })
        .attr("xlink:href", function(d) {
            return d.icon();
        })
        .attr("width", 16)
        .attr("height", 16)
        .attr("x", function(d, i) {
            return i * 16;
        })
        .attr("y", 16)
        .on("click", function(d) {
            d.click();
        })
        .on("mouseenter", function() {
            d3.select(this).classed({
                active: 1
            })
        })
        .on("mouseleave", function() {
            d3.select(this).classed({
                active: 0
            })
        });

    for (var i = 0; i < this.buttons.length; i++)
        this.buttons[i].onDraw();
};

mpld3_Toolbar.prototype.deactivate_all = function() {
    this.buttons.forEach(function(b) {
        b.deactivate();
    });
};

mpld3_Toolbar.prototype.deactivate_by_action = function(actions) {
    function filt(e) {
        return actions.indexOf(e) !== -1;
    }
    if (actions.length > 0) {
        this.buttons.forEach(function(button) {
            if (button.actions.filter(filt).length > 0) button.deactivate();
        });
    }
};

/**********************************************************************/
/* Button object: */
mpld3.Button = mpld3_Button;
mpld3_Button.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Button.prototype.constructor = mpld3_Button;

function mpld3_Button(toolbar, key) {
    mpld3_PlotElement.call(this, toolbar);
    this.toolbar = toolbar;
    this.cssclass = "mpld3-" + key + "button";
    this.active = false;
}

mpld3_Button.prototype.click = function() {
    this.active ? this.deactivate() : this.activate();
};

mpld3_Button.prototype.activate = function() {
    this.toolbar.deactivate_by_action(this.actions);
    this.onActivate();
    this.active = true;
    this.toolbar.toolbar.select('.' + this.cssclass)
        .classed({
            pressed: true
        });
    if (!this.sticky)
        this.deactivate();
};

mpld3_Button.prototype.deactivate = function() {
    this.onDeactivate();
    this.active = false;
    this.toolbar.toolbar.select('.' + this.cssclass)
        .classed({
            pressed: false
        });
}
mpld3_Button.prototype.sticky = false;
mpld3_Button.prototype.actions = [];
mpld3_Button.prototype.icon = function() {
    return "";
}
mpld3_Button.prototype.onActivate = function() {};
mpld3_Button.prototype.onDeactivate = function() {};
mpld3_Button.prototype.onDraw = function() {};

/* Factory for button classes */
mpld3.ButtonFactory = function(members) {
    function B(toolbar, key) {
        mpld3_Button.call(this, toolbar, key);
    };
    B.prototype = Object.create(mpld3_Button.prototype);
    B.prototype.constructor = B;
    for (key in members) B.prototype[key] = members[key];
    mpld3.Toolbar.prototype.buttonDict[members.toolbarKey] = B;
    return B;
}

/* Reset Button */
mpld3.ResetButton = mpld3.ButtonFactory({
    toolbarKey: "reset",
    sticky: false,
    onActivate: function() {
        this.toolbar.fig.reset();
    },
    icon: function() {
        return mpld3.icons["reset"];
    }
});

/* Move Button */
mpld3.MoveButton = mpld3.ButtonFactory({
    toolbarKey: "move",
    sticky: true,
    actions: ["scroll", "drag"],
    onActivate: function() {
        this.toolbar.fig.enable_zoom();
    },
    onDeactivate: function() {
        this.toolbar.fig.disable_zoom();
    },
    onDraw: function() {
        this.toolbar.fig.disable_zoom();
    },
    icon: function() {
        return mpld3.icons["move"];
    }
});
