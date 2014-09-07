function hideOrbit() {
	//Hide all neighbor circles
	orbGroups= svg.selectAll("g.orbit")
	orbGroups.select("circle")
			.attr("r",0)
			
	//Hide all neighbor text
	orbGroups.selectAll("text")
			.attr("font-size",0);
			
			
	//Hide sun
	sunGroup= svg.select("g.sun")
	sunGroup.select("circle")
			.attr("r",0);
    sunGroup.selectAll("text")
            .attr("font-size",0);
}

function hideHelp(){
    //hide help text on axes
    help.selectAll("text.helpPath")
        .attr("font-size", 0)
    
    //hide help sun
    help.select("circle.sun")
        .attr("fill","none")
    
	//unhide sun
	sunGroup= svg.select("g.sun")
	sunGroup.select("circle")
			.attr("r",mainR)
}

function showHelp() {
    //Hide orbit
    if(!onHelp) {
        hideOrbit();  
    }
    onHelp= true;
    
    //show help sun
    help.select("circle.sun")
        .attr("fill",colors["HELP"])
        
    //show help text on axes
    help.selectAll("text.helpPath")
        .attr("font-size", distScale/8);    
}

function setOrbit(dat) {
    //Hide help
    if(onHelp) {
        hideHelp();  
    }
    onHelp= false;

	var name= dat.team;
    var neighbors= dat.neighbors;
	
    x= getDistBounds(neighbors);
    max= x[0];
    min= x[1];

	//set sun format and text
    sun.select("circle")
        .attr("fill", colors[name]);
    labels= ["","Playoff series won: ", "Predicted series wins: ", "Weighted win score: ", "Conference rank: ", "League rank: "];
    sunTextSizes= [mainR/4,mainR/6,mainR/7,mainR/7,mainR/7,mainR/7];
    sunData= [name+" \'13-\'14",3,2,2.12,6,9];
	sun.selectAll("text")
        .data(sunData)
        .attr("x",orbitCenterX)
        .attr("y", function(d,i){
                s= 0;
				for(k=0;k<=i;k++) {
					s += sunTextSizes[k];
				}
                return orbitCenterY - mainR + s + 5*mainR/12 + (i-1)*mainR/12
            })
        .attr("font-size",function(d,i){
                return sunTextSizes[i];
            })
        .text(function(d,i) {
                if(i==0) {
					d3.select(this.parentNode).attr("xlink:href", "http://www.basketball-reference.com"+"/teams/"+name+"/2014.html");
					d3.select(this).style("text-decoration","underline")
                                    .attr("fill","white")
									.on("click", function() {
										return;
									});
				}
                return labels[i]+d;    
            })
	
    //set properties and event handlers of each circle in orbit
    orbit= svg.selectAll("g.orbit")
            .data(neighbors);  	
    orbit.select("circle")
        .attr("class","orbit")
        .attr("cx", function(d,i) {
                return orbitCenterX + (offset + mainR + ((d.dist-min)/(max-min))*distScale)*Math.cos(2*i*Math.PI/neighbors.length);
            })
        .attr("cy", function(d,i) {
                return orbitCenterY - (offset + mainR + ((d.dist-min)/(max-min))*distScale)*Math.sin(2*i*Math.PI/neighbors.length);
            })
        .attr("r", function(d) {
                return d.wins*winRadScale+minNeighRad;
            })
        .attr("fill", function(d,i) {
                return (d.name in colors) ? colors[d.name] : "#000000";
            })
	
	//set event handlers for neighbor orbit groups
    orbit.on("mouseover",function() {
                color= d3.select(this).select("circle.orbit").attr("fill");
                d3.select(this).select("circle.orbit").attr("stroke",d3.rgb(color).darker(1));
                d3.select(this).select("circle.orbit").attr("stroke-width","5")
            })
        .on("mouseout",function() {
                d3.select(this).select("circle.orbit").attr("stroke-width","0");
            })
        .on("click", function() {
                resize(d3.select(this));
            });
}

//Unselect all toggles (and help button) except that at index "except" (help is index 16)
function unSelectToggles(except) {
	var circs= svg.select("svg.toggle")
                .selectAll("g.toggleButton");
    circs.select("circle")
		.attr("stroke-width",function(d,i){
			toggleClicked[i]= 0;
            return except==i ? 5 : 0;
        })
}

//zoom or un-zoom informational circle
function resize(group) {
    //grab group's circle and text
    circ= group.select("circle.orbit");
    txt= group.select("svg.text")
        
    //clicked to zoom circle
    if (circ.attr("r") != zoomRad) {
        gs= svg.selectAll("g.orbit")
        
        //zoom out all zoomed circles 
        gs.selectAll("circle.orbit")
            .transition().delay(0).duration(500).attr("r", function(d) {
                    return d.wins*winRadScale + minNeighRad;
                });
            
        //hide all visible circle text
        gs.selectAll("svg.text").selectAll("text")
            .transition().delay(200).duration(500).attr("visibility","hidden");
        
        //move this group's circle and text to front
        group.moveToFront()
        
        //zoom in circle (i.e. increaase radius) and make its text visible
        circ.transition().delay(0).duration(500).attr("r", zoomRad);
        txt.selectAll("text").transition().delay(200).duration(500).attr("visibility","visible");
        txt.moveToFront()
    }
    
    //clicked to un-zoom circle
    else {
        //un-zoom circle (i.e. set radius to original length) and re-hide circle's text
        circ.transition().delay(0).duration(500).attr("r", function(d) {
            return d.wins*winRadScale+minNeighRad;
        });
        txt.selectAll("text").transition().delay(200).duration(500).attr("visibility","hidden");
    }
}

//format the axes
function formatAxes() {
	//set radii of axes
	//x= [0.5*(1-(offset)/distScale),1]
	x=[1];
    
	//draw ellipses
    axes.selectAll("ellipse")
		.data(x)
        .attr("rx", function(d) {
                    return offset + mainR + d*distScale;
                })
        .attr("ry", function(d) {
                    return offset + mainR + d*distScale;
                })
        .attr("fill-opacity",0.0)
        .attr("stroke","#999999");
}

function setZoomText(dat) {
    var name= dat.team;
    var neighbors= dat.neighbors;

    //add text to each group, set properties and event handler
    texts= orbit.select("svg")
			.attr("class","text")
			.attr("x", function(d,i) {
					return orbitCenterX + (offset + mainR + ((d.dist-min)/(max-min))*distScale)*Math.cos(2*i*Math.PI/neighbors.length) - zoomRad*(Math.sqrt(2)/2);
				})
			.attr("y", function(d,i) {
					return orbitCenterY - (offset + mainR + ((d.dist-min)/(max-min))*distScale)*Math.sin(2*i*Math.PI/neighbors.length) - zoomRad*(Math.sqrt(2)/2);
				})
			.attr("width", function(d) {
					return 2*zoomRad;
				})
			.attr("height", function(d) {
					return 2*zoomRad;
				});
			 
	sizes= [zoomRad/6,zoomRad/8,zoomRad/8,zoomRad/12,zoomRad/12,zoomRad/12,zoomRad/12,zoomRad/12]           
    texts.selectAll("text")
        .data(function(d){
                return teamText(d);
            })
        .attr("x", zoomRad*Math.sqrt(2)/2)
        .attr("y", function(d,i){
				s= 0;
				for(k=0;k<=i;k++) {
					s += sizes[k];
				}
                return s+(i-1)*zoomRad/12;
            })
		.attr("id","text")
		.attr("font-size",function(d,i){return sizes[i];})
		.attr("dominant-baseline","hanging")
        .attr("fill", "white")
        .attr("visibility","hidden")
        .moveToFront()
        .text(function(d,i){
				if(i==0) {
					d3.select(this.parentNode).attr("xlink:href", "http://www.basketball-reference.com"+d[1]);
					d3.select(this).style("text-decoration","underline")
									.on("click", function() {
										return;
									});
					return d[0];
				}
				else {
					return d;
				}
			})
}