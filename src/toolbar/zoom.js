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