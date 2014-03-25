import "core";

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