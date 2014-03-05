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

!(function(d3){
    var mpld3 = {
	version: "0.1",
	figures: [],
	plugin_map: {},
	register_plugin: function(name, obj){mpld3.plugin_map[name] = obj;}
    };
    
    /* Figure object: */
    mpld3.Figure = function(figid, prop){
	this.name = "mpld3.Figure";
	this.figid = figid;

	// Make a root div with relative positioning,
	// so we can position elements absolutely within it.
	this.root = d3.select('#' + figid)
	               .append("div").style("position","relative");
	
	var required = ["width", "height"];
	var defaults = {data:{},
			axes:[],
			plugins:[],
			toolbar:["reset", "move"],
			id: mpld3.generate_id(),
		       };
	this.prop = mpld3.process_props(this, prop, defaults, required);
	
	this.width = this.prop.width;
	this.height = this.prop.height;
	this.data = this.prop.data;
	
	this.axes = [];
	for(var i=0; i<prop.axes.length; i++){
	    this.axes.push(new mpld3.Axes(this, this.prop.axes[i]));
	}

	this.plugins = [];
	for(var i=0; i<prop.plugins.length; i++){
	    this.add_plugin(this.prop.plugins[i]["type"],
			    this.prop.plugins[i]);
	}

	this.toolbar = new mpld3.Toolbar(this, this.prop.toolbar);
    };
    
    mpld3.Figure.prototype.add_plugin = function(plug, props){
	if(plug in mpld3.plugin_map)
          plug = mpld3.plugin_map[plug];
	if(typeof(plug) === "string"){
          console.warn("Skipping unrecognized plugin: " + plug);
          return;
        }

	if(props.clear_toolbar){
	    this.prop.toolbar = [];
	}
	if("buttons" in props){
	    if(typeof(props.buttons) === "string"){
		this.prop.toolbar.push(props.buttons);
	    }else{
		for(var i=0; i<props.buttons.length; i++){
		    this.prop.toolbar.push(props.buttons[i]);
		}
	    }
	}
	this.plugins.push(new plug(this, props));
    };
    
    mpld3.Figure.prototype.draw = function(){
	this.canvas = this.root.append('svg:svg')
            .attr('class', 'mpld3-figure')
            .attr('width', this.width)
            .attr('height', this.height);
	
	for (var i=0; i<this.axes.length; i++){
	    this.axes[i].draw();
	}
	
	// enable zoom by default; plugins or toolbar items might change this.
	this.enable_zoom();
	
	for (var i=0; i<this.plugins.length; i++){
	    this.plugins[i].draw();
	}
	
	this.toolbar.draw();
    };
    
    mpld3.Figure.prototype.reset = function(duration){
	duration = (typeof duration !== 'undefined') ? duration : 750;
	for (var i=0; i<this.axes.length; i++){
	    this.axes[i].prep_reset();
	}
	
	var transition = function(t){
	    for (var i=0; i<this.axes.length; i++){
		this.axes[i].xdom(this.axes[i].xdom.domain(this.axes[i].ix(t)));
		this.axes[i].ydom(this.axes[i].ydom.domain(this.axes[i].iy(t)));
		
		// don't propagate: this will be done as part of the loop.
		this.axes[i].zoomed(false);
	    }
	}.bind(this)
	
	d3.transition().duration(duration)
            .tween("zoom", function(){return transition;});
	
	for (var i=0; i<this.axes.length; i++){
	    this.axes[i].finalize_reset();
	}
    };
    
    mpld3.Figure.prototype.enable_zoom = function(){
	for(var i=0; i<this.axes.length; i++){
	    this.axes[i].enable_zoom();
	}
	this.zoom_on = true;
    };
    
    mpld3.Figure.prototype.disable_zoom = function(){
	for(var i=0; i<this.axes.length; i++){
	    this.axes[i].disable_zoom();
	}
	this.zoom_on = false;
    };
    
    mpld3.Figure.prototype.toggle_zoom = function(){
	if(this.zoom_on){
	    this.disable_zoom();
	}else{
	    this.enable_zoom();
	}
    };
    
    mpld3.Figure.prototype.get_data = function(data){
	if(data === null || typeof(data) === "undefined"){
	    return null;
	}else if(typeof(data) === "string"){
	    return this.data[data];
	}else{
	    return data;
	}
    }
    
    
    /* Toolbar Object: */
    mpld3.Toolbar = function(fig, prop){
	this.name = "mpld3.Toolbar";
	this.fig = fig;
	this.prop = prop;
	this.buttons = [];
	for(var i=0; i<this.prop.length; i++){
	    var Button = this.buttonDict[this.prop[i]];
	    if(typeof(Button) === "undefined"){
		console.warn("Button type " + this.prop[i] + " not recognized");
	    }else{
		this.buttons.push(new Button(this,
					     "mpld3-"+this.prop[i]+"button",
					     this.prop[i]));
	    }
	}
    };
    
    mpld3.Toolbar.prototype.draw = function(){
	this.toolbar = this.fig.root.append("div")
	    .attr("class", "mpld3-toolbar")
            .style("position", "absolute") // relative to parent div
            .style("bottom", "0px")
            .style("left", "0px");

	mpld3.insert_css("div#"+this.fig.figid + " .mpld3-toolbar img",
			 {width: "16px", height: "16px",
			  cursor: "pointer", opacity: 0.2,
			  display: "inline-block",
			  margin: "0px"})
	mpld3.insert_css("div#"+this.fig.figid + " .mpld3-toolbar img.active",
			 {opacity: 0.4})
	mpld3.insert_css("div#"+this.fig.figid + " .mpld3-toolbar img.pressed",
			 {opacity: 0.6})

	for(var i=0; i<this.buttons.length; i++){
	    this.buttons[i].draw();
	}
	this.toolbar.selectAll("img")
           .on("mouseenter", function(){d3.select(this).classed({active:1})})
           .on("mouseleave", function(){d3.select(this).classed({active:0})})
           .on("mousedown", function(){d3.select(this).classed({pressed:1})})
           .on("mouseup", function(){d3.select(this).classed({pressed:0})});
    };

    mpld3.Toolbar.prototype.deactivate_all = function(){
	for(var i=0; i<this.buttons.length; i++){
	    this.buttons[i].deactivate();
	}
    };


    /* Toolbar Button Object: */
    mpld3.BaseButton = function(toolbar, cssclass, icon){
	this.toolbar = toolbar;
	this.cssclass = cssclass;
    };
    mpld3.BaseButton.prototype.draw = function(){
	return this.toolbar.toolbar.append("img")
	    .attr("class", this.cssclass)
	    .attr("src", this.icon)
	    .on("click", this.onClick.bind(this));
    };
    mpld3.BaseButton.prototype.deactivate = function(){};
    mpld3.BaseButton.prototype.onClick = function(){};
    mpld3.BaseButton.prototype.icon = "";

    /* Factory for button classes */
    mpld3.ButtonFactory = function(members){
	var F = function(){mpld3.BaseButton.apply(this, arguments);};
	F.prototype = new mpld3.BaseButton();
	F.prototype.constructor = F;
	for(key in members)
	    F.prototype[key] = members[key];
	return F;
    }

    /* Reset Button */
    mpld3.ResetButton = mpld3.ButtonFactory({
	onClick: function(){this.toolbar.fig.reset();},
	icon: function(){return mpld3.icons["reset"];}
    });

    /* Move Button */
    mpld3.MoveButton = mpld3.ButtonFactory({
	onClick: function(){
	    this.toolbar.fig.toggle_zoom();
	    this.toolbar.toolbar.selectAll(".mpld3-movebutton")
		.classed({pressed: this.toolbar.fig.zoom_on,
			  active: !this.toolbar.fig.zoom_on});},
	draw: function(){
	    mpld3.BaseButton.prototype.draw.apply(this);
	    this.toolbar.fig.disable_zoom();},
	deactivate: function(){
	    this.toolbar.fig.disable_zoom();
	    this.toolbar.toolbar.selectAll(".mpld3-movebutton")
		.classed({pressed: this.toolbar.fig.zoom_on,
			  active: false});},
	icon: function(){return mpld3.icons["move"];}
    });
    
    /* Set up the mapping of button types and icons */
    /* Icons come from the mpld3/icons/ directory   */
    mpld3.Toolbar.prototype.buttonDict = {move: mpld3.MoveButton,
					  reset: mpld3.ResetButton};


    /* Coordinates Object: */
    /* Converts from the given units to axes (pixel) units */
    mpld3.Coordinates = function(trans, ax){
	if(typeof(ax) === "undefined"){
	    this.ax = null;
	    this.fig = null;
	    if(this.trans !== "display"){
		throw "ax must be defined if transform != 'display'";
	    }
	}else{
	    this.ax = ax;
	    this.fig = ax.fig;
	}
	this.x = this["x_" + trans];
	this.y = this["y_" + trans];
	if(typeof(this.x) === "undefined" || typeof(this.y) === "undefined"){
	    throw "unrecognized coordinate code: " + trans;
	}
	this.zoomable = (trans === "data");
    }

    mpld3.Coordinates.prototype.x_data = function(x){return this.ax.x(x);}
    mpld3.Coordinates.prototype.y_data = function(y){return this.ax.y(y);}
    mpld3.Coordinates.prototype.x_display = function(x){return x;}
    mpld3.Coordinates.prototype.y_display = function(y){return y;}
    mpld3.Coordinates.prototype.x_axes = function(x){return x * this.ax.width;}
    mpld3.Coordinates.prototype.y_axes = function(y){
	return this.ax.height * (1 - y);}
    mpld3.Coordinates.prototype.x_figure = function(x){
	return x * this.fig.width - this.ax.position[0];}
    mpld3.Coordinates.prototype.y_figure = function(y){
	return (1 - y) * this.fig.height - this.ax.position[1];}

    
    /* Axes Object: */
    mpld3.Axes = function(fig, prop){
	this.name = "mpld3.Axes";
	this.fig = fig;
	this.axnum = fig.axes.length;
	this.axid = fig.figid + '_ax' + (this.axnum + 1)
	this.clipid = this.axid + '_clip'
	
	var required = ["xlim", "ylim"];
	var defaults = {"bbox": [0.1, 0.1, 0.8, 0.8],
			"axesbg": "#FFFFFF",
			"id": mpld3.generate_id(),
			"axesbgalpha": 1.0,
			"gridOn": false,
			"xdomain": null,
			"ydomain": null,
			"xscale": "linear",
			"yscale": "linear",
			"zoomable": true,
			"axes": [{position:"left"},
				 {position:"bottom"}],
			grids: [],
			"xgridprops": {},
			"ygridprops": {},
			"lines": [],
			"paths": [],
			"markers": [],
			"texts": [],
			"collections": [],
			"sharex": [],
			"sharey": [],
			"images": []};
	
	this.prop = mpld3.process_props(this, prop, defaults, required)
	this.prop.xdomain = this.prop.xdomain || this.prop.xlim;
	this.prop.ydomain = this.prop.ydomain || this.prop.ylim;
	
	this.fig = fig;
	
	this.sharex = [];
	this.sharey = [];
	
	this.elements = [];
	
	var bbox = this.prop.bbox;
	this.position = [bbox[0] * this.fig.width,
			 (1 - bbox[1] - bbox[3]) * this.fig.height];
	this.width = bbox[2] * this.fig.width;
	this.height = bbox[3] * this.fig.height;
	
	function buildDate(d){return new Date(d[0],d[1],d[2],d[3],d[4],d[5]);}
	
	if(this.prop.xscale === 'log'){
	    this.xdom = d3.scale.log();
	}else if(this.prop.xscale === 'date'){
	    this.prop.xdomain = [buildDate(this.prop.xdomain[0]),
				 buildDate(this.prop.xdomain[1])];
	    this.xdom = d3.time.scale();
	}else{
	    this.xdom = d3.scale.linear();
	}
	
	if(this.prop.yscale === 'log'){
	    this.ydom = d3.scale.log();
	}else if(this.prop.yscale === 'date'){
	    this.prop.ydomain = [buildDate(this.prop.ydomain[0]),
				 buildDate(this.prop.ydomain[1])];
	    this.ydom = d3.time.scale();
	}else{
	    this.ydom = d3.scale.linear();
	}
	
	this.xdom.domain(this.prop.xdomain)
            .range([0, this.width]);
	
	this.ydom.domain(this.prop.ydomain)
            .range([this.height, 0]);
	
	if(this.prop.xscale === 'date'){
	    this.xmap = d3.time.scale()
		.domain(this.prop.xdomain)
		.range(this.prop.xlim);
	    this.x = function(x){return this.xdom(this.xmap.invert(x));}
	}else if(this.prop.xscale === 'log'){
	    this.xmap = this.xdom;
	    this.x = this.xdom;
	}else{
	    this.xmap = this.xdom;
	    this.x = this.xdom;
	}
	
	if(this.prop.yscale === 'date'){
	    this.ymap = d3.time.scale()
		.domain(this.ydomain)
		.range(this.prop.ylim);
	    this.y = function(y){return this.ydom(this.ymap.invert(y));}
	}else if(this.prop.yscale === 'log'){
	    this.ymap = this.ydom;
	    this.y = this.ydom;
	}else{
	    this.ymap = this.ydom;
	    this.y = this.ydom;
	}
	
	// Add axes and grids
	var axes = this.prop.axes;
	for(var i=0; i<axes.length; i++){
	    var axis = new mpld3.Axis(this, axes[i])
	    this.elements.push(axis);
	    if(this.prop.gridOn || axis.prop.grid.gridOn){
		this.elements.push(axis.getGrid());
	    }
	}

	var grids = this.prop.grids;
	for(var i=0; i<grids.length; i++){
	    this.elements.push(new Grid(this, grids[i])); 
	}
	
	// Add paths
	var paths = this.prop.paths;
	for(var i=0; i<paths.length;i++){
	    this.elements.push(new mpld3.Path(this, paths[i]));
	}
	
	// Add lines
	var lines = this.prop.lines;
	for(var i=0; i<lines.length;i++){
	    this.elements.push(new mpld3.Line(this, lines[i]));
	}
	
	// Add markers
	var markers = this.prop.markers;
	for(var i=0; i<markers.length;i++){
	    this.elements.push(new mpld3.Markers(this, markers[i]));
	}
	
	// Add texts
	var texts = this.prop.texts;
	for(var i=0; i<texts.length; i++){
	    this.elements.push(new mpld3.Text(this, texts[i]));
	}
	
	// Add collections
	var collections = this.prop.collections;
	for(var i=0; i<collections.length; i++){
	    this.elements.push(new mpld3.PathCollection(this, collections[i]));
	}
	
	// Add images
	var images = this.prop.images;
	for(var i=0; i<images.length; i++){
	    this.elements.push(new mpld3.Image(this, images[i]));
	}
	
	// Sort all elements by zorder
	this.elements.sort(function(a,b){return a.prop.zorder-b.prop.zorder});
    }
    
    mpld3.Axes.prototype.draw = function(){
	for(var i=0; i<this.prop.sharex.length; i++){
	    this.sharex.push(mpld3.get_element(this.prop.sharex[i]));
	}
	
	for(var i=0; i<this.prop.sharey.length; i++){
	    this.sharey.push(mpld3.get_element(this.prop.sharey[i]));
	}
	
	this.zoom = d3.behavior.zoom();
	
	this.zoom.last_t = this.zoom.translate()
	this.zoom.last_s = this.zoom.scale()
	
	this.zoom_x = d3.behavior.zoom().x(this.xdom);
	this.zoom_y = d3.behavior.zoom().y(this.ydom);
	
	this.baseaxes = this.fig.canvas.append("g")
            .attr('transform', 'translate('
		  + this.position[0] + ','
		  + this.position[1] + ')')
            .attr('width', this.width)
            .attr('height', this.height)
            .attr('class', "mpld3-baseaxes");
	
	this.clip = this.baseaxes.append("svg:clipPath")
            .attr("id", this.clipid)
            .append("svg:rect")
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", this.width)
            .attr("height", this.height)
	
	this.axes = this.baseaxes.append("g")
            .attr("class", "mpld3-axes")
            .attr("clip-path", "url(#" + this.clipid + ")");
	
	this.axesbg = this.axes.append("svg:rect")
            .attr("width", this.width)
            .attr("height", this.height)
            .attr("class", "mpld3-axesbg")
	    .style("fill", this.prop.axesbg)
            .style("fill-opacity", this.prop.axesbgalpha);
	
	for(var i=0; i<this.elements.length; i++){
	    this.elements[i].draw();
	}
    };
    
    mpld3.Axes.prototype.enable_zoom = function(){
	if(this.prop.zoomable){
	    this.zoom.on("zoom", this.zoomed.bind(this));
	    this.axes.call(this.zoom);
	    this.axes.style("cursor", 'move');
	}
    };
    
    mpld3.Axes.prototype.disable_zoom = function(){
	if(this.prop.zoomable){
	    this.zoom.on("zoom", null);
	    this.axes.on('.zoom', null)
	    this.axes.style('cursor', null);
	}
    };
    
    mpld3.Axes.prototype.zoomed = function(propagate){
	// propagate is a boolean specifying whether to propagate movements
	// to shared axes, specified by sharex and sharey.  Default is true.
	propagate = (typeof propagate == 'undefined') ? true : propagate;
	
	if(propagate){
            // update scale and translation of zoom_x and zoom_y,
            // based on change in this.zoom scale and translation values
            var dt0 = this.zoom.translate()[0] - this.zoom.last_t[0];
            var dt1 = this.zoom.translate()[1] - this.zoom.last_t[1];
            var ds = this.zoom.scale() / this.zoom.last_s;
	    
            this.zoom_x.translate([this.zoom_x.translate()[0]+dt0, 0]);
            this.zoom_x.scale(this.zoom_x.scale() * ds)
	    
            this.zoom_y.translate([0, this.zoom_y.translate()[1]+dt1]);
            this.zoom_y.scale(this.zoom_y.scale() * ds)
	    
            // update last translate and scale values for future use
            this.zoom.last_t = this.zoom.translate();
            this.zoom.last_s = this.zoom.scale();
	    
            // update shared axeses
            for(var i=0; i<this.sharex.length; i++){
		this.sharex[i].zoom_x.translate(this.zoom_x.translate());
		this.sharex[i].zoom_x.scale(this.zoom_x.scale());
            }
            for(var i=0; i<this.sharey.length; i++){
		this.sharey[i].zoom_y.translate(this.zoom_y.translate());
		this.sharey[i].zoom_y.scale(this.zoom_y.scale());
            }
	    
            // render updates
            for(var i=0; i<this.sharex.length; i++){
		this.sharex[i].zoomed(false);
            }
            for(var i=0; i<this.sharey.length; i++){
		this.sharey[i].zoomed(false);
            }
	}
	
	for(var i=0; i<this.elements.length; i++){
            this.elements[i].zoomed();
	}
    };
    
    mpld3.Axes.prototype.prep_reset = function(){
	// interpolate() does not work on dates, so we map dates to numbers,
	// interpolate the numbers, and then invert the map.
	// we use the same strategy for log for smooth interpolation
	// There probably is a cleaner approach...
	
	if (this.prop.xscale === 'date'){
	    var start = this.xdom.domain();
	    var end = this.prop.xdomain;
	    var interp = d3.interpolate(
		[this.xmap(start[0]), this.xmap(start[1])],
		[this.xmap(end[0]), this.xmap(end[1])]);
	    this.ix = function(t){
		return [this.xmap.invert(interp(t)[0]),
			this.xmap.invert(interp(t)[1])];
	    }
	}else{
	    this.ix = d3.interpolate(this.xdom.domain(), this.prop.xlim);
	}
	
	if (this.prop.yscale === 'date'){
	    var start = this.ydom.domain();
	    var end = this.ydomain;
	    var interp = d3.interpolate(
		[this.ymap(start[0]), this.ymap(start[1])],
		[this.ymap(end[0]), this.ymap(end[1])]);
	    this.iy = function(t){
		return [this.ymap.invert(interp(t)[0]),
			this.ymap.invert(interp(t)[1])];
	    }
	}else{
	    this.iy = d3.interpolate(this.ydom.domain(), this.prop.ylim);
	}
    }
    
    mpld3.Axes.prototype.finalize_reset = function(){
	this.zoom.scale(1).translate([0, 0]);
	this.zoom.last_t = this.zoom.translate();
	this.zoom.last_s = this.zoom.scale();
	this.zoom_x.scale(1).translate([0, 0]);
	this.zoom_y.scale(1).translate([0, 0]);
    }
    
    mpld3.Axes.prototype.reset = function(){
	this.prep_reset();
	d3.transition().duration(750).tween("zoom", function() {
	    return function(t) {
		this.zoom_x.x(this.xdom.domain(this.ix(t)));
		this.zoom_y.y(this.ydom.domain(this.iy(t)));
		this.zoomed();
	    };
	});
	this.finalize_reset();
    };
    
    
    /* Axis object */
    mpld3.Axis = function(axes, prop){
	this.name = mpld3.Axis;
	this.axes = axes;
	
	var required = ["position"]
	var defaults = {nticks : 10,
			tickvalues : null,
			tickformat : null,
			fontsize : "11px",
			fontcolor : "black",
			axiscolor : "black",
			grid : {},
			zorder: 0,
			id: mpld3.generate_id()}
	this.prop = mpld3.process_props(this, prop, defaults, required);

	var trans = {bottom: [0, this.axes.height], top: [0, 0],
		     left: [0, 0], right: [this.axes.width, 0]};
	var xy = {bottom: 'x', top: 'x', left: 'y', right: 'y'}

	this.transform = "translate(" + trans[this.prop.position] + ")";
	this.prop.xy = xy[this.prop.position];
	this.cssclass = "mpld3-" + this.prop.xy + "axis";
	this.scale = this.axes[this.prop.xy + "dom"];
    };

    mpld3.Axis.prototype.getGrid = function(){
	var gridprop = {nticks: this.prop.nticks, zorder: this.prop.zorder,
			tickvalues: this.prop.tickvalues, xy: this.prop.xy}
	if(this.prop.grid){
	    for(var key in this.prop.grid){
		gridprop[key] = this.prop.grid[key];
	    }
	}
	return new mpld3.Grid(this.axes, gridprop);
    };
    
    mpld3.Axis.prototype.draw = function(){
	this.axis = d3.svg.axis()
            .scale(this.scale)
            .orient(this.prop.position)
            .ticks(this.prop.nticks)
            .tickValues(this.prop.tickvalues)
            .tickFormat(this.prop.tickformat);
	
	this.elem = this.axes.baseaxes.append('g')
            .attr("transform", this.transform)
            .attr("class", this.cssclass)
            .call(this.axis);
	
	// We create header-level CSS to style these elements, because
	// zooming/panning creates new elements with these classes.
	mpld3.insert_css("div#" + this.axes.fig.figid
			 + " ." + this.cssclass + " line, "
			 + " ." + this.cssclass + " path",
			 {"shape-rendering":"crispEdges",
			  "stroke":this.prop.axiscolor,
			  "fill":"none"});
	mpld3.insert_css("div#" + this.axes.fig.figid
			 + " ." + this.cssclass + " text",
			 {"font-family": "sans-serif",
			  "font-size": this.prop.fontsize,
			  "fill": this.prop.fontcolor,
			  "stroke": "none"});
    };
    
    mpld3.Axis.prototype.zoomed = function(){
	this.elem.call(this.axis);
    };
    
    
    /* Grid Object */
    mpld3.Grid = function(axes, prop){
	this.name = "mpld3.Grid";
	this.axes = axes;
	
	var required = ["xy"];
	var defaults = {color : "gray",
			dasharray : "2,2",
			alpha : "0.5",
			nticks : 10,
			tickvalues : null,
			zorder: 0,
			id: mpld3.generate_id()};
	this.prop = mpld3.process_props(this, prop, defaults, required);
	this.cssclass = "mpld3-" + this.prop.xy + "grid";
	
	if(this.prop.xy == "x"){
	    this.transform = "translate(0," + this.axes.height + ")";
	    this.position = "bottom";
	    this.scale = this.axes.xdom;
	    this.tickSize = -this.axes.height;
	}else if(this.prop.xy == "y"){
	    this.transform = "translate(0,0)";
	    this.position = "left";
	    this.scale = this.axes.ydom;
	    this.tickSize = -this.axes.width;
	}else{
	    throw "unrecognized grid xy specifier: should be 'x' or 'y'";
	}
    }
    
    mpld3.Grid.prototype.draw = function(){
	this.grid = d3.svg.axis()
            .scale(this.scale)
            .orient(this.position)
            .ticks(this.prop.nticks)
            .tickValues(this.prop.tickvalues)
            .tickSize(this.tickSize, 0, 0)
            .tickFormat("");
	this.elem = this.axes.axes.append("g")
            .attr("class", this.cssclass)
            .attr("transform", this.transform)
            .call(this.grid);
	
	// We create header-level CSS to style these elements, because
	// zooming/panning creates new elements with these classes.
	mpld3.insert_css("div#" + this.axes.fig.figid +
			 " ." + this.cssclass + " .tick",
			 {"stroke": this.prop.color,
			  "stroke-dasharray": this.prop.dasharray,
			  "stroke-opacity": this.prop.alpha});
	mpld3.insert_css("div#" + this.axes.fig.figid +
			 " ." + this.cssclass + " path",
			 {"stroke-width": 0});
    };
    
    mpld3.Grid.prototype.zoomed = function(){
	this.elem.call(this.grid);
    };
    
    
    /* Line Element */
    // TODO: should this be removed?
    //       Everything Line can do, Path can do (better)
    mpld3.Line = function(ax, prop){
	this.name = "mpld3.Line";
	this.ax = ax;
	
	var required = ["data"]
	var defaults = {xindex: 0,
			yindex: 1,
			coordinates: "data",
			color: "salmon",
			linewidth: 2,
			dasharray: "10,0",
			alpha: 1.0,
			zorder: 2,
			id: mpld3.generate_id()};
	
	this.prop = mpld3.process_props(this, prop, defaults, required);
	this.data = ax.fig.get_data(this.prop.data);
	this.coords = new mpld3.Coordinates(this.prop.coordinates, this.ax);
    };
    
    mpld3.Line.prototype.filter = function(d){
	return (!isNaN(d[this.prop.xindex])
		&& !isNaN(d[this.prop.yindex]));
    };
    
    mpld3.Line.prototype.draw = function(){
	this.datafunc = d3.svg.line()
            .interpolate("linear")
            .defined(this.filter.bind(this))
	    .x(function(d){return this.coords.x(d[this.prop.xindex]);})
	    .y(function(d){return this.coords.y(d[this.prop.yindex]);});
	
	this.line = this.ax.axes.append("svg:path")
	    .data(this.data)
            .attr('class', 'mpld3-line')
	    .style("stroke", this.prop.color)
	    .style("stroke-width", this.prop.linewidth)
	    .style("stroke-dasharray", this.prop.dasharray)
	    .style("stroke-opacity", this.prop.alpha)
	    .style("fill", "none");

	this.line.attr("d", this.datafunc(this.data));
    }
    
    mpld3.Line.prototype.elements = function(d){
	return this.line;
    };
    
    mpld3.Line.prototype.zoomed = function(){
	if(this.coords.zoomable){
	    this.line.attr("d", this.datafunc(this.data));
	}
    }
    
    
    /* Path Element */
    mpld3.Path = function(ax, prop){
	this.name = "mpld3.Path";
	this.ax = ax;
	
	var required = ["data"]
	var defaults = {xindex: 0,
			yindex: 1,
			coordinates: "data",
			facecolor: "green",
			edgecolor: "black",
			edgewidth: 1,
			dasharray: "10,0",
			pathcodes: null,
			offset: null,
			offsetcoordinates: "data",
			alpha: 1.0,
			zorder: 1,
			id: mpld3.generate_id()};
	
	this.prop = mpld3.process_props(this, prop, defaults, required);
	this.data = ax.fig.get_data(this.prop.data);
	this.pathcodes = this.prop.pathcodes;
	
	this.pathcoords = new mpld3.Coordinates(this.prop.coordinates,
						this.ax);
	this.offsetcoords = new mpld3.Coordinates(this.prop.offsetcoordinates,
						  this.ax);
    };
    
    mpld3.Path.prototype.draw = function(){
	this.datafunc = mpld3.path()
	    .x(function(d){return this.pathcoords.x(d[this.prop.xindex]);})
	    .y(function(d){return this.pathcoords.y(d[this.prop.yindex]);});

	this.path = this.ax.axes.append("svg:path")
            .attr("d", this.datafunc(this.data, this.pathcodes))
            .attr('class', "mpld3-path")
	    .style("stroke", this.prop.edgecolor)
	    .style("stroke-width", this.prop.edgewidth)
	    .style("stroke-dasharray", this.prop.dasharray)
	    .style("stroke-opacity", this.prop.alpha)
	    .style("fill", this.prop.facecolor)
	    .style("fill-opacity", this.prop.alpha)
            .attr("vector-effect", "non-scaling-stroke");
	
	if(this.prop.offset !== null){
	    var offset = [this.offsetcoords.x(this.prop.offset[0]),
			  this.offsetcoords.y(this.prop.offset[1])];    
	    this.path.attr("transform", "translate(" + offset + ")");
	}
    };
    
    mpld3.Path.prototype.elements = function(d){
	return this.path;
    };
    
    mpld3.Path.prototype.zoomed = function(){
	if(this.prop.coordinates === "data"){
	    this.path.attr("d", this.datafunc(this.data, this.pathcodes));
	}
	if(this.prop.offset !== null && this.prop.offsetcoordinates === "data"){
	    var offset = [this.ax.x(this.prop.offset[0]),
			  this.ax.y(this.prop.offset[1])];
	    this.path.attr("transform", "translate(" + offset + ")");
	}
    };
    
    
    /* Markers Element */
    mpld3.Markers = function(ax, prop){
	this.name = "mpld3.Markers";
	this.ax = ax;
	
	var required = ["data"];
	var defaults = {xindex: 0,
			yindex: 1,
			coordinates: "data",
			facecolor: "salmon",
			edgecolor: "black",
			edgewidth: 1,
			alpha: 1.0,
			markersize: 6,
			markername: "circle",
			markerpath: null,
			zorder: 3,
			id: mpld3.generate_id()};
	this.prop = mpld3.process_props(this, prop, defaults, required);
	this.data = ax.fig.get_data(this.prop.data);
	
	if(this.prop.markerpath !== null){
	    if(this.prop.markerpath[0].length > 0){
		this.marker = mpld3.path().call(this.prop.markerpath[0],
						this.prop.markerpath[1]);
	    }else{
		this.marker = null;
	    }
	}else{
	    if(this.prop.markername !== null){
		this.marker = d3.svg.symbol(this.prop.markername)
	            .size(Math.pow(this.prop.markersize, 2));
	    }else{
		this.marker = null;
	    }
	}
	this.coords = new mpld3.Coordinates(this.prop.coordinates, this.ax);
    };
    
    mpld3.Markers.prototype.translate = function(d){
	return "translate("
	    + this.coords.x(d[this.prop.xindex]) + ","
	    + this.coords.y(d[this.prop.yindex]) + ")";
    };
    
    mpld3.Markers.prototype.filter = function(d){
	return (!isNaN(d[this.prop.xindex])
		&& !isNaN(d[this.prop.yindex]));
    };
    
    mpld3.Markers.prototype.draw = function(){
	this.group = this.ax.axes.append("svg:g")
	this.pointsobj = this.group.selectAll("paths")
            .data(this.data.filter(this.filter.bind(this)))
            .enter().append("svg:path")
            .attr('class', 'mpld3-marker')
            .attr("d", this.marker)
            .attr("transform", this.translate.bind(this))
            .style("stroke-width", this.prop.edgewidth)
            .style("stroke", this.prop.edgecolor)
            .style("fill", this.prop.facecolor)
            .style("fill-opacity", this.prop.alpha)
            .style("stroke-opacity", this.prop.alpha)
            .attr("vector-effect", "non-scaling-stroke");
    };
    
    mpld3.Markers.prototype.elements = function(d){
	return this.group.selectAll("path");
    };
    
    mpld3.Markers.prototype.zoomed = function(){
	if(this.coords.zoomable){
	    this.pointsobj.attr("transform", this.translate.bind(this));
	}
    };
    
    /* Path Collection Element */
    mpld3.PathCollection = function(ax, prop){
	window.prop = prop;
	this.ax = ax;
	var required = ["paths", "offsets"]
	var defaults = {xindex: 0,
			yindex: 1,
			pathtransforms: [],
			pathcoordinates: "points",
			offsetcoordinates: "data",
			offsetorder: "before",
			edgecolors: ["#000000"],
			edgewidths: [1.0],
			facecolors: ["#0000FF"],
			alphas: [1.0],
			zorder: 2,
			id: mpld3.generate_id()};
	this.prop = mpld3.process_props(this, prop, defaults, required);
	this.paths = prop.paths;
	this.get = function(L, i, dflt){
	    return L.length ? L[i % L.length] : dflt;
	}
	
	if(this.prop.facecolors === null || this.prop.facecolors.length === 0){
	    this.prop.facecolors = ["none"];
	}
	if(this.prop.edgecolors === null || this.prop.edgecolors.length === 0){
	    this.prop.edgecolors = ["none"];
	}
	
	var offsets = this.ax.fig.get_data(this.prop.offsets);
	if(offsets === null || offsets.length === 0){
	    offsets = [null];
	}
	
	// For use in the draw() command, expand offsets to size N
	var N = Math.max(this.prop.paths.length, offsets.length);
	
	if(offsets.length === N){
            this.offsets = offsets;
        }else{
            this.offsets = [];
	    for(var i=0; i<N; i++){
		this.offsets.push(offsets[i % offsets.length]);
	    }
	}

	this.pathcoords = new mpld3.Coordinates(this.prop.pathcoordinates,
						this.ax);
	this.offsetcoords = new mpld3.Coordinates(this.prop.offsetcoordinates,
						  this.ax);
    };
    
    mpld3.PathCollection.prototype.transform_func = function(d, i){
	// here we apply the offset and the individual path transform
	var transform;
	var t = this.prop.pathtransforms;
	if(t.length > 0){
	    t = t[i % t.length];
	    transform = d3.transform("matrix(" + t + ")").toString();
	}else{
	    transform = "";
	}
	
	var offset;
	if(d === null || typeof(d) === "undefined"){
	    offset = "translate(0, 0)";
	}else{
	    offset = ("translate(" + [this.offsetcoords.x(d[this.prop.xindex]),
				      this.offsetcoords.y(d[this.prop.yindex])]
                      +")");
	}
	
	if(this.prop.offsetorder === "after"){
	    return transform + offset;
	}else{
	    return offset + transform;
	}
    };
    
    mpld3.PathCollection.prototype.path_func = function(d, i){
	var path = this.paths[i % this.paths.length]
	var ret = mpld3.path()
            .x(function(d){return this.pathcoords.x(d[0]);}.bind(this))
            .y(function(d){return this.pathcoords.y(d[1]);}.bind(this))
            .call(path[0], path[1]);
	return ret;
    };
    
    mpld3.PathCollection.prototype.style_func = function(d, i){
	var prop = this.prop;
	var styles = {"stroke": prop.edgecolors[i % prop.edgecolors.length],
		      "fill": prop.facecolors[i % prop.facecolors.length],
		      "stroke-width": prop.edgewidths[i%prop.edgewidths.length],
		      "stroke-opacity": prop.alphas[i % prop.alphas.length],
		      "fill-opacity": prop.alphas[i % prop.alphas.length]};
	var ret = ""
	for(key in styles){
	    ret += key + ":" + styles[key] + ";"
	}
	return ret
    };
    
    mpld3.PathCollection.prototype.draw = function(){
	this.group = this.ax.axes.append("svg:g");
	this.pathsobj = this.group.selectAll("paths")
            .data(this.offsets)
            .enter().append("svg:path")
            .attr("vector-effect", "non-scaling-stroke")
            .attr("class", "mpld3-path")
            .attr("d", this.path_func.bind(this))
            .attr("style", this.style_func.bind(this))
            .attr("transform", this.transform_func.bind(this));
    };
    
    mpld3.PathCollection.prototype.elements = function(d){
	return this.group.selectAll("path");
    };
    
    mpld3.PathCollection.prototype.zoomed = function(){
	if(this.prop.pathcoordinates === "data"){
	    this.pathsobj.attr("d", this.path_func.bind(this));
	}
	if(this.prop.offsetcoordinates === "data"){
	    this.pathsobj.attr("transform", this.transform_func.bind(this));
	}
    };
    
    /* Text Element */
    mpld3.Text = function(ax, prop){
	this.ax = ax;
	this.prop = mpld3.process_props(this, prop,
					{coordinates: "data",
					 h_anchor: "start",
					 v_baseline: "auto",
					 rotation: 0,
					 fontsize: 11,
					 color: "black",
					 alpha: 1.0,
					 zorder: 3,
					 id: mpld3.generate_id()},
					["text", "position"]);
	this.text = this.prop.text;
	this.position = this.prop.position;
	this.coords = new mpld3.Coordinates(this.prop.coordinates,
						 this.ax);
    };
    
    mpld3.Text.prototype.draw = function(){
	if(this.prop.coordinates == "data"){
	    this.obj = this.ax.axes.append("text");
	}else{
	    this.obj = this.ax.baseaxes.append("text");
	}
	
	this.obj.attr("class", "mpld3-text")
            .text(this.text)
            .style("text-anchor", this.prop.h_anchor)
	    .style("dominant-baseline", this.prop.v_baseline)
	    .style("font-size", this.prop.fontsize)
	    .style("fill", this.prop.color)
	    .style("opacity", this.prop.alpha);
	
	var pos_x = this.coords.x(this.position[0]);
	var pos_y = this.coords.y(this.position[1]);

	this.obj
	    .attr("x", pos_x)
	    .attr("y", pos_y);
	
	if(this.prop.rotation){
	    this.obj.attr("transform", "rotate("
			  + this.prop.rotation + ","
			  + pos_x + "," + pos_y + ")");
	}
    };
    
    mpld3.Text.prototype.elements = function(d){
	return d3.select(this.obj);
    };
    
    mpld3.Text.prototype.zoomed = function(){
	if(this.coords.zoomable){
	    pos_x = this.coords.x(this.position[0]);
	    pos_y = this.coords.y(this.position[1]);
	    
	    this.obj
		.attr("x", pos_x)
		.attr("y", pos_y);
	    
	    if(this.prop.rotation){
		this.obj.attr("transform", "rotate("
			      + this.prop.rotation + ","
			      + pos_x + "," + pos_y + ")");
	    }
	}
    };
    
    /* Image Object */
    mpld3.Image = function(ax, prop){
	this.ax = ax;
	var required = ["data", "extent"];
	var defaults = {alpha: 1.0,
	 		coordinates: "data",
	 		zorder: 1,
			id: mpld3.generate_id()};
	this.prop = mpld3.process_props(this, prop, defaults, required);
	this.coords = new mpld3.Coordinates(this.prop.coordinates, this.ax);
    };
    
    mpld3.Image.prototype.draw = function(){
	this.image = this.ax.axes.append("svg:image")
	    .attr('class', 'mpld3-image')
            .attr('xlink:href', "data:image/png;base64," + this.prop.data)
	    .style({'opacity': this.prop.alpha})
            .attr("preserveAspectRatio", "none");
	this.zoomed();
    };
    
    mpld3.Image.prototype.elements = function(d){
	return d3.select(this.image);
    };
    
    mpld3.Image.prototype.zoomed = function(){
	var extent = this.prop.extent;
	this.image
	    .attr("x", this.coords.x(extent[0]))
            .attr("y", this.coords.y(extent[3]))
            .attr("width", this.coords.x(extent[1])-this.coords.x(extent[0]))
            .attr("height", this.coords.y(extent[2])-this.coords.y(extent[3]));
    };
    
    
    /* Plugins */
    mpld3.TooltipPlugin = function(fig, prop){
	this.fig = fig;
	var required = ["id"];
	var defaults = {labels:null, hoffset:0, voffset:10, location:'mouse'};
	this.prop = mpld3.process_props(this, prop, defaults, required);
    }
    
    mpld3.TooltipPlugin.prototype.draw = function(){
	var obj = mpld3.get_element(this.prop.id, this.fig);
	var labels = this.prop.labels;
	var loc = this.prop.location;
	
	this.tooltip = this.fig.canvas.append("text")
            .attr("class", "mpld3-tooltip-text")
	    .attr("x", 0)
	    .attr("y", 0)
	    .text("")
	    .style("visibility", "hidden");
	
	if(loc == "bottom left" || loc == "top left"){
	    this.x = obj.ax.position[0] + 5 + this.prop.hoffset;
	    this.tooltip.style("text-anchor", "beginning")
	}else if(loc == "bottom right" || loc == "top right"){
	    this.x = obj.ax.position[0] + obj.ax.width - 5 + this.prop.hoffset;
	    this.tooltip.style("text-anchor", "end");
	}else{
            this.tooltip.style("text-anchor", "middle");
	}
	
	if(loc == "bottom left" || loc == "bottom right"){
	    this.y = obj.ax.position[1] + obj.ax.height - 5 + this.prop.voffset;
	}else if(loc == "top left" || loc == "top right"){
	    this.y = obj.ax.position[1] + 5 + this.prop.voffset;
	}
	
	function mouseover(d, i){
	    this.tooltip
		.style("visibility", "visible")
		.text((labels === null) ? "(" + d[0] + ", " + d[1] + ")"
		      : labels[i % labels.length]);
	}
	
	function mousemove(d, i){
	    if(loc === "mouse"){
		var pos = d3.mouse(this.fig.canvas.node())
		this.x = pos[0] + this.prop.hoffset;
		this.y = pos[1] - this.prop.voffset;
	    }
	    
            this.tooltip
		.attr('x', this.x)
		.attr('y', this.y);
	}
	
	function mouseout(d, i){
	    this.tooltip.style("visibility", "hidden");
	}
	
	obj.elements()
	    .on("mouseover", mouseover.bind(this))
            .on("mousemove", mousemove.bind(this))
            .on("mouseout", mouseout.bind(this));
    }
    
    mpld3.register_plugin("tooltip", mpld3.TooltipPlugin);
    
    /**********************************************************************/
    /* Data Parsing Functions */
    mpld3.draw_figure = function(figid, spec){
	var element = document.getElementById(figid);
	if(element === null){
	    throw (figid + " is not a valid id");
	    return null;
	}
	var fig = new mpld3.Figure(figid, spec);
	mpld3.figures.push(fig);
	fig.draw();
	return fig;
    };
    
    
    /**********************************************************************/
    /* Convenience Functions                                              */

    mpld3.merge_objects = function(_){
	var output = {};
	var obj;
	for(var i=0; i<arguments.length; i++){
	    obj = arguments[i];
	    for (var attr in obj){
		output[attr] = obj[attr];
	    }
	}
	return output;
    }
    
    mpld3.generate_id = function(N, chars){
	if(typeof(N) === "undefined"){N=10;}
	if(typeof(chars) === "undefined"){
	    chars = ("abcdefghijklmnopqrstuvwxyz" +
		     "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
		     "0123456789");}
	var id = "";
	for(var i=0; i<N; i++)
            id += chars.charAt(Math.round(Math.random() * (chars.length - 1)));
	return id;
    }
    
    // TODO: should elements be stored in a map/hash table instead?
    // It would make this more efficient.
    mpld3.get_element = function(id, fig){
	var figs_to_search, ax, el;
	if(typeof(fig) === "undefined"){
	    figs_to_search = mpld3.figures;
	}else if(typeof(fig.length) === "undefined"){
	    figs_to_search = [fig];
	}else{
	    figs_to_search = fig;
	}
	for(var i=0; i<figs_to_search.length; i++){
	    fig = figs_to_search[i];
	    if(fig.prop.id === id){
		return fig;
	    }
	    for(var j=0; j<fig.axes.length; j++){
		ax = fig.axes[j];
		if(ax.prop.id === id){
		    return ax;
		}
		for(var k=0; k<ax.elements.length; k++){
		    el = ax.elements[k];
		    if(el.prop.id === id){
			return el;
		    }
		}
	    }
	}
	return null;
    }
    
    mpld3.process_props = function(obj, properties, defaults, required){
	if(typeof(defaults) === "undefined"){defaults = {};}
	if(typeof(required) === "undefined"){required = [];}
	
	for(i=0; i<required.length; i++){
	    if(!(required[i] in properties)){
		throw ("property '" + required[i] + "' " +
		       "must be specified for " + obj.name);
	    }
	}
	for(var property in defaults){
	    if(!(property in properties)){
		properties[property] = defaults[property];
	    }
	}
	return properties;
    }
    
    // Function to insert some CSS into the header
    mpld3.insert_css = function(selector, attributes){
	var head = document.head || document.getElementsByTagName('head')[0];
	var style = document.createElement('style');
	
	var css = selector + " {"
	for(var prop in attributes){
	    css += prop + ":" + attributes[prop] + "; "
	}
	css += "}"
	
	style.type = 'text/css';
	if (style.styleSheet){
	    style.styleSheet.cssText = css;
	} else {
	    style.appendChild(document.createTextNode(css));
	}
	head.appendChild(style);
    };
    
    
    function mpld3_functor(v) {
	return typeof v === "function" ? v : function() {
	    return v;
	};
    }
    
    function mpld3_path(_){
	var x = function(d){return d[0];}
	var y = function(d){return d[1];}
	
	// number of vertices for each SVG code
	var n_vertices = {M:1, m:1, L:1, l:1, Q:2, q:2, T:2, t:2,
			  S:3, s:3, C:3, c:3, Z:0, z:0};
	
	function path(vertices, pathcodes){
	    // If pathcodes is not defined, we assume straight line segments
	    var fx = mpld3_functor(x), fy = mpld3_functor(y);
	    if((pathcodes === null) || (typeof(pathcodes) === "undefined")){
		pathcodes = ["M"];
		for(var i=0; i<vertices.length - 1; i++){
		    pathcodes.push("L");
		}
	    }
	    
	    var data = "";
	    var j = 0;  // counter for vertices
	    for (var i=0;i<pathcodes.length;i++){
		data += pathcodes[i]
		for(var jj=j; jj<j+n_vertices[pathcodes[i]]; jj++){
		    data += fx.call(this, vertices[jj]) + " ";
		    data += fy.call(this, vertices[jj]) + " ";
		}
		j += n_vertices[pathcodes[i]];
	    }
	    if(j != vertices.length){
		console.warn("Warning: not all vertices used in Path");
	    }
	    return data;
	}
	
	path.x = function(_) {
	    if (!arguments.length) return x;
	    x = _;
	    return path;
	};
	
	path.y = function(_) {
	    if (!arguments.length) return y;
	    y = _;
	    return path;
	};
	
	path.call = path;
	
	return path;
    }
    
    mpld3.path = function(){
	return mpld3_path();
    }

    mpld3.icons = {reset: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBI\nWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gIcACMoD/OzIwAAAJhJREFUOMtjYKAx4KDUgNsMDAx7\nyNV8i4GB4T8U76VEM8mGYNNMtCH4NBM0hBjNMIwSsMzQ0MamcDkDA8NmQi6xggpUoikwQbIkHk2u\nE0rLI7vCBknBSyxeRDZAE6qHgQkq+ZeBgYERSfFPAoHNDNUDN4BswIRmKgxwEasP2dlsDAwMYlA/\n/mVgYHiBpkkGKscIDaPfVMmuAGnOTaGsXF0MAAAAAElFTkSuQmCC\n",
		   move: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBI\nWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gIcACQMfLHBNQAAANZJREFUOMud07FKA0EQBuAviaKB\nlFr7COJrpAyYRlKn8hECEkFEn8ROCCm0sBMRYgh5EgVFtEhsRjiO27vkBoZd/vn5d3b+XcrjFI9q\nxgXWkc8pUjOB93GMd3zgB9d1unjDSxmhWSHQqOJki+MtOuv/b3ZifUqctIrMxwhHuG1gim4Ma5kR\nWuEkXFgU4B0MW1Ho4TeyjX3s4TDq3zn8ALvZ7q5wX9DqLOHCDA95cFBAnOO1AL/ZdNopgY3fQcqF\nyriMe37hM9w521ZkkvlMo7o/8g7nZYQ/QDctp1nTCf0AAAAASUVORK5CYII=\n"};
    
    // put mpld3 in the global namespace
    this.mpld3 = mpld3;
    console.log("Loaded mpld3 version " + mpld3.version);
})(d3);
