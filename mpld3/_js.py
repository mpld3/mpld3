"""Some javascript snippets which are used in _objects.py"""


CONSTRUCT_SVG_PATH = """
    // This function constructs a mapped SVG path
    // from an input data array
    var construct_SVG_path = function(data, xmap, ymap){
       var result = "";
       for (var i=0;i<data.length;i++){
          result += data[i][0];
          if(data[i][0] == 'Z'){
            continue;
          }
          for (var j=0;j<data[i][1].length;j++){
            if(j % 2 == 0){
               result += " " + xmap(data[i][1][j]);
            }else{
               result += " " + ymap(data[i][1][j]);
            }
          }
          result += " ";
       }
       return result;
     };
"""
