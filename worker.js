function mandel(width, max_iter, left, top, right, bottom) {

  f = (right - left) / width;

  for (y = 0; y < width; y++) {
    buffer = [];

    for(x = 0; x < width; x++) {
      cr = left + x * f;
      ci = top - y * f;

      zr = cr;
      zi = ci;
      color = 0;

      for (i = 1; i < max_iter; i++) {
        tmp = zr;
        zr = zr*zr - zi*zi + cr;
        zi = 2 * tmp * zi + ci;
        
        if (zr * zr + zi * zi > 4) {
          color = i;

          break;
        }
      }
      
      buffer.push({ 'x':x, 'y':y, 'c':color });
    }

    postMessage(buffer);
  }
}

addEventListener('message', function(e) {
  var data = e.data;
  
  switch (data.cmd) {
    case 'start':
      console.log("Worker started!"); 
      console.log("width=" + data.width);
      console.log("max_iter=" + data.max_iter);

      mandel(data.width, data.max_iter, data.left, data.top, data.right, data.bottom);

      console.log("Worker finished!"); 
      break;
  }
}, false);
