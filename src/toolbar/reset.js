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