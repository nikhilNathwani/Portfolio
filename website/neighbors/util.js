//move selected object to front of parent's layout
d3.selection.prototype.moveToFront = function() {
    return this.each(function(){
      this.parentNode.appendChild(this);
    });
  };

//returns max and min neighbor distance from central circle 
function getDistBounds(arr) {
    max= -Number.MAX_VALUE;
    min= Number.MAX_VALUE;
    for (i = 0; i < arr.length; i++) {
        if(arr[i].dist>max) {
            max= arr[i].dist;
        }
        if(arr[i].dist<min) {
            min= arr[i].dist;
        }
    }
    return [max,min];
}

//return text to display on circle when clicked
function teamText(d) {
    return [[d.name + " " + d.year,d.url], d.wins + " series won","Biggest Similarities:"].concat(d.attrs)
}