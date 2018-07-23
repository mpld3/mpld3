/**********************************************************************/
/* Button object: */
mpld3.Button = mpld3_Button;
mpld3_Button.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Button.prototype.constructor = mpld3_Button;

function mpld3_Button(toolbar, key) {
    mpld3_PlotElement.call(this, toolbar);
    this.toolbar = toolbar;
    this.fig = this.toolbar.fig;
    this.cssclass = "mpld3-" + key + "button";
    this.active = false;
    }

mpld3_Button.prototype.setState = function(state) {
    (state) ? this.activate() : this.deactivate();
}

mpld3_Button.prototype.click = function() {
    this.active ? this.deactivate() : this.activate();
};

mpld3_Button.prototype.activate = function() {
    // This will also deactivate itself. A bit silly, but should be ok, maybe.
    this.toolbar.deactivate_by_action(this.actions);
    this.onActivate();
    this.active = true;
    this.toolbar.toolbar
        .select('.' + this.cssclass)
        .classed('pressed', true);
    if (!this.sticky) {
        this.deactivate();
    }
};

mpld3_Button.prototype.deactivate = function() {
    this.onDeactivate();
    this.active = false;
    this.toolbar.toolbar
        .select('.' + this.cssclass)
        .classed('pressed', false);
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
    if (typeof members.buttonID !== "string"){
        throw "ButtonFactory: buttonID must be present and be a string";
    }
    function B(toolbar) {
        mpld3_Button.call(this, toolbar, this.buttonID);
    }
    B.prototype = Object.create(mpld3_Button.prototype);
    B.prototype.constructor = B;
    for (var key in members) {
        B.prototype[key] = members[key];
    }
    return B;
}
