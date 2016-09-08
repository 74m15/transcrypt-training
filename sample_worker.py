from org.transcrypt.stubs.browser import __pragma__

__pragma__ ('skip')
this = console = postMessage = addEventListener = 0 # Prevent complaints by optional static checker
__pragma__ ('noskip')

grid = [[ [1,0,0,0,0,0,0,0],  # 0
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0]],
        [ [0,0,0,0,1,0,0,0],  # 1
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,0,0,1,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0]],
        [ [0,0,1,0,0,0,1,0],  # 2
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,0,0,0,0,0,0,0],
          [0,0,1,0,0,0,1,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,0,0,0,0,0,0,0]],
        [ [0,1,0,1,0,1,0,1],  # 3
          [1,1,1,1,1,1,1,1],
          [0,1,0,1,0,1,0,1],
          [1,1,1,1,1,1,1,1],
          [0,1,0,0,0,1,0,1],
          [1,1,1,1,1,1,1,1],
          [0,1,0,1,0,1,0,1],
          [1,1,1,1,1,1,1,1]]]

def mandel(width, max_iter, left, top, right, bottom):

  f = (right - left) / width;

  for g in range(4):
    for y in range(0, width, (1 << (3 - g))):
      buffer = []
  
      for x in range(width):
        if (not (grid[g][y % 8][x % 8] == 1)):
          continue

        cr = left + x * f
        ci = top - y * f
  
        zr = cr
        zi = ci
        color = 0
  
        for i in range(1, max_iter):
          tmp = zr
          zr = zr*zr - zi*zi + cr
          zi = 2 * tmp * zi + ci
          
          if (zr * zr + zi * zi > 4):
            color = i
  
            break
        
        buffer.append({ 'x':x, 'y':y, 'c':color, 'size': (1 << (3 - g)) })
  
      postMessage(buffer)


def on_message(e):

  debugger
  data = e.data
  
  if (data.cmd == "start"):
    console.log("Worker started!")
    console.log("width={}".format(data.width))
    console.log("max_iter={}".format(data.max_iter))

    mandel(data.width, data.max_iter, data.left, data.top, data.right, data.bottom)

    console.log("Worker finished!")
  else:
    console.log("Unknown command!")


addEventListener("message", on_message)