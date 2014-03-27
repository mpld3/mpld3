    // put mpld3 in the global namespace
    if (typeof define === "function" && define.amd) {
        define(mpld3);
    } else if (typeof module === "object" && module.exports) {
        module.exports = mpld3;
    } else {
        this.mpld3 = mpld3;
    }

    console.log("Loaded mpld3 version " + mpld3.version);
}(d3);
