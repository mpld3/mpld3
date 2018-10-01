/**********************************************************************/
/* Toolbar object: */
mpld3.Toolbar = mpld3_Toolbar;
mpld3_Toolbar.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Toolbar.prototype.constructor = mpld3_Toolbar;
mpld3_Toolbar.prototype.defaultProps = {
    buttons: ["reset", "move"]
};

function mpld3_Toolbar(fig, props) {
    mpld3_PlotElement.call(this, fig, props)
    this.buttons = [];
    this.props.buttons.forEach(this.addButton.bind(this));
}

mpld3_Toolbar.prototype.addButton = function(button) {
    this.buttons.push(new button(this));
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
            d3.select(this).classed('active', true);
        })
        .on("mouseleave", function() {
            d3.select(this).classed('active', false);
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
