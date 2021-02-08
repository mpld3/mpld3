    // put mpld3 in the global namespace
    if (typeof module === "object" && module.exports) {
        module.exports = mpld3;
    } else {
        this.mpld3 = mpld3;
    }

    console.log("Loaded mpld3 version " + mpld3.version);
