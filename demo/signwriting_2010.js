function fromSymKey(key){
  code = 0x100000 - 0x10000 + ((parseInt(key.slice(1,4),16) - 256) * 96) + ((parseInt(key.slice(4,5),16))*16) + parseInt(key.slice(5,6),16) + 1
  return String.fromCharCode(0xD800 + (code >> 10), 0xDC00 + (code & 0x3FF));
}

function getSymSize(key) {
  var bound = 82;
  var plus = 3;
  var canvas = getSymSize.canvas || (getSymSize.canvas = document.createElement("canvas"));
  var context = canvas.getContext("2d");
  context.clearRect(0, 0, bound, bound);
  context.font = "30px 'SignWriting 2010'";
  context.fillText(fromSymKey(key),0,0);

  var detect = function(x,y,w,h){
    var line=false;
    imgData = context.getImageData(x,y,w,h)
    data = imgData.data
    for (var i=data.length; i--;) {
      if (data[i]){ line = true; break; }
    }
    return line;
  }

  var min,max,current,found,foundPlus,width,height;
  min=0;
  max=bound;
  while(min!=(max-1)){ 
    current=parseInt((max+min)/2)
    found = detect(current,0,1,bound);
    foundPlus = detect(current + plus,0,1,bound)
    if (found || foundPlus){ 
      min = current
    } else {
      max = current
    }
  }
  width = 500 + min;

  min=0;
  max=bound;
  while(min!=(max-1)){
    current=parseInt((max+min)/2)
    found = detect(0,current,width,1);
    foundPlus = detect(0,current + plus,width,1)
    if (found || foundPlus){
      min = current
    } else {
      max = parseInt((max+max+current)/3)
    }
  }
  height = 500 + max
  size= width + 'x' + height;
  if (size=='500x501') return
  return size;
}

function getSignCanvas(fsw){
  var canvas = document.createElement("canvas");
  var r, rsym, rcoord, sym, syms, coords;
  r = /(A(S[123][0-9a-f]{2}[0-5][0-9a-f])+)?[BLMR]([0-9]{3}x[0-9]{3})(S[123][0-9a-f]{2}[0-5][0-9a-f][0-9]{3}x[0-9]{3})*|S38[7-9ab][0-5][0-9a-f][0-9]{3}x[0-9]{3}/g;
  rsym = /S[123][0-9a-f]{2}[0-5][0-9a-f][0-9]{3}x[0-9]{3}/g;
  rcoord = /[0-9]{3}x[0-9]{3}/g;
  var x, x1 = 500,
    x2 = 500,
    y, y1 = 500,
    y2 = 500,
    k, w, h, l;

  k = fsw.charAt(0);
  coords = fsw.match(rcoord);
  for (var i=0; i < coords.length; i++) {
    x = parseInt(coords[i].slice(0, 3));
    y = parseInt(coords[i].slice(4, 7));
    x1 = Math.min(x1, x);
    x2 = Math.max(x2, x);
    y1 = Math.min(y1, y);
    y2 = Math.max(y2, y);
  }

  canvas.width = x2-x1;
  canvas.height = y2-y1;

  var context = canvas.getContext("2d");
  context.translate(0.5, 0.5);
  syms = fsw.match(rsym);
  for (var i=0; i < syms.length; i++) {
    sym = syms[i].slice(0,6)
    x = syms[i].slice(6, 9);
    y = syms[i].slice(10, 13);
    //line
    context.font = "30px 'SignWriting 2010 Filling'";
    context.fillStyle = "white";
    context.fillText(fromSymKey(sym),x-x1,y-y1);
    context.font = "30px 'SignWriting 2010'";
    context.fillStyle = "black";
    context.fillText(fromSymKey(sym),x-x1,y-y1);
  }
  return canvas;
}

function getSignSvg(fsw,laned){
  var r, rsym, rcoord, sym, syms, coords, o;
  r = /(A(S[123][0-9a-f]{2}[0-5][0-9a-f])+)?[BLMR]([0-9]{3}x[0-9]{3})(S[123][0-9a-f]{2}[0-5][0-9a-f][0-9]{3}x[0-9]{3})*|S38[7-9ab][0-5][0-9a-f][0-9]{3}x[0-9]{3}/g;
  rsym = /S[123][0-9a-f]{2}[0-5][0-9a-f][0-9]{3}x[0-9]{3}/g;
  rcoord = /[0-9]{3}x[0-9]{3}/g;
  o = {};
  o.L = -1;
  o.R = 1;
  var x, x1 = 500,
    x2 = 500,
    y, y1 = 500,
    y2 = 500,
    k, w, h, l;

  k = fsw.charAt(0);
  coords = fsw.match(rcoord);
  for (var i=0; i < coords.length; i++) {
    x = parseInt(coords[i].slice(0, 3));
    y = parseInt(coords[i].slice(4, 7));
    x1 = Math.min(x1, x);
    x2 = Math.max(x2, x);
    y1 = Math.min(y1, y);
    y2 = Math.max(y2, y);
  }
  syms = fsw.match(rsym);
  for (var i=0; i < syms.length; i++) {
    sym = syms[i].slice(0,6)
    x = syms[i].slice(6, 9);
    y = syms[i].slice(10, 13);
    syms[i] = '<g transform="translate(' + x + '.5,' + y + '.5)"><text class="sym-fill">' + sym + '</text><text class="sym-line">' + sym + '</text></g>';
  }
  if (k == 'S') {
    x2 = 1000 - x1;
    y2 = 1000 - y1;
  }
  w = x2 - x1;
  h = y2 - y1;
  l = o[k] || 0;
  l = l * 75 + x1 - 400;
  var svg = '<svg width="' + w + '" height="' + h + '" viewBox="' + x1 + ' ' + y1 + ' ' + w + ' ' + h + '">' + syms.join('') + "</svg>";
  if (laned){
    svg = '<div style="padding:10px;position:relative;width:' + w + 'px;height:' + h + 'px;left:' + l + 'px;">' + svg + '</div>';
  }
  return svg
}
