from org.transcrypt.stubs.browser import __pragma__, __new__
from math import cos, log, sqrt, pi


__pragma__ ('skip')
document = window = Math = Date = Worker = 0 # Prevent complaints by optional static checker
__pragma__ ('noskip')

def rgb(r, g, b):
  
  def _hex(x):
    _SYM_ = "0123456789abcdef"
    
    res = [ "0", "0" ]
    

    for i in range(2):
      x, r = x // 16, x % 16
      
      res[1 - i] = _SYM_[r]
    
    return "".join(res)
  
  return "#{0}{1}{2}".format(_hex(r), _hex(g), _hex(b))
  
class Mandel:
  
  def __init__(self):
    pass
  
  
  def reset(self):
    if (self.canvas.width <= self.canvas.height):
      self.mandel_left = -2
      self.mandel_top = 2.5 * (self.canvas.height / self.canvas.width) / 2
      self.mandel_right = 0.5
      self.mandel_bottom = -self.mandel_top
    else:
      self.mandel_left =  -(2.5 * (self.canvas.width / self.canvas.height)) * (3/5)
      self.mandel_top = 1.25
      self.mandel_right = (2.5 * (self.canvas.width / self.canvas.height)) * (2/5)
      self.mandel_bottom = -1.25
  
  
  def startup(self):
    print("let's go!")
    
    self.resizing = 0
    self.action = None
    self.worker = __new__(Worker("__javascript__/sample_worker.js"))
    self.worker.onmessage = self.on_message

    self.selector = document.getElementById("selector")
    self.container = document.getElementById("container")
    self.canvas = document.getElementById("mandelbrot")
    self.canvas.width = self.container.offsetWidth
    self.canvas.height = self.container.offsetHeight
    self.canvas.style.width = "{}px".format(self.canvas.width)
    self.canvas.style.height = "{}px".format(self.canvas.height)
    self.ctx = self.canvas.getContext("2d")

    self.reset()
    
    document.getElementById("container").onmousedown = self.on_mousedown
    document.getElementById("container").onmousemove = self.on_mousemove
    document.getElementById("container").onmouseup = self.on_mouseup
    
    document.getElementById("container").ontouchstart = self.on_touchstart
    document.getElementById("container").ontouchmove = self.on_touchmove
    document.getElementById("container").ontouchend = self.on_touchend
  
  
  def drawPixel(self, x, y, c, size):
    self.ctx.fillStyle = c
    self.ctx.fillRect(int(x * self.ratio), int(y * self.ratio), int(size * self.ratio), int(size * self.ratio))
  
  
  def getColor(self, c):
    if (c == 0):
      return (0,0,0)
    
    r = int(255 * (1 + cos(sqrt(sqrt(c)))) / 2)
    g = int(255 * (1 + cos(sqrt(sqrt(2 * c)))) / 2)
    b = int(255 * (1 + cos(sqrt(sqrt(3 * c) + pi / 4))) / 2)
    
    return (r, g, b)
  
  
  def updateProgress(self):
      progress = int(100 * (8/15) * (self.rows_done + 1) / self.canvas.height * self.ratio)
      
      document.getElementById("progress-bar").style.width = "{}%".format(progress)
  
  
  def on_message(self, e):
    self.rows_done += 1
         
    self.updateProgress()
    
    for p in e.data:
      r, g, b = self.getColor(p.c)
      
      self.drawPixel(p.x, p.y, rgb(r, g, b), p.size)
  
  
  def draw(self):
    self.action = None
    
    self.ratio = int(document.getElementById("txt_width").value)
    self.max_iter = 1 << int(document.getElementById("txt_max_iter").value)
    
    if (self.selector.style.visibility == "visible"):
      self.define_selection()
      self.selector.style.visibility = "hidden"
    
    print(self.width, self.ratio, self.max_iter)
    print(self.mandel_left, self.mandel_top, self.mandel_right, self.mandel_bottom)
    
    self.rows_done = 0
    
    self.updateProgress()
    
    self.worker.postMessage({
      "cmd":'start', 
      "width":int(self.canvas.width / self.ratio), 
      "height":int(self.canvas.height / self.ratio),
      "max_iter":self.max_iter,
      "left":self.mandel_left,
      "top":self.mandel_top,
      "right":self.mandel_right,
      "bottom":self.mandel_bottom})
    
  def define_selection(self):
    deltaX = self.mandel_right - self.mandel_left
    deltaY = self.mandel_top - self.mandel_bottom
    
    deltaSelX = self.r - self.l
    deltaSelY = self.b - self.t
    
    if (self.canvas.width <= self.canvas.height):
      self.t -= (self.canvas.height / self.canvas.width - 1) * deltaSelY / 2
      self.b += (self.canvas.height / self.canvas.width - 1) * deltaSelY / 2
    else:
      self.l -= (self.canvas.width / self.canvas.height - 1) * deltaSelX / 2
      self.r += (self.canvas.width / self.canvas.height - 1) * deltaSelX / 2
    
    self.mandel_left, self.mandel_top, self.mandel_right, self.mandel_bottom = \
      self.mandel_left + deltaX * self.l / self.canvas.width, \
      self.mandel_top - deltaY * self.t / self.canvas.height, \
      self.mandel_left + deltaX * self.r / self.canvas.width, \
      self.mandel_top - deltaY * self.b / self.canvas.height
      
    print(self.mandel_left, self.mandel_top, self.mandel_right, self.mandel_bottom)
  
  
  def place_selector(self, x, y):
    self.action = "select"
    
    self.l, self.t = x - 30, y - 30
    self.r, self.b = x + 30, y + 30
    self.baseX = int(self.r + self.l) / 2
    self.baseY = int(self.b + self.t) / 2
    
    deltaX = max(0, -self.l) + min(0, self.canvas.width - self.r)
    deltaY = max(0, -self.t) + min(0, self.canvas.height - self.b)

    self.l += deltaX
    self.r += deltaY
    self.t += deltaY
    self.b += deltaY
    
    self.selector.style.visibility = "visible"
    self.selector.style.left = "{}px".format(self.l)
    self.selector.style.top = "{}px".format(self.t)
    self.selector.style.width = "{}px".format(self.r - self.l + 1)
    self.selector.style.height = "{}px".format(self.b - self.t + 1)
  
  
  def move_selector(self, x, y):
    deltaX = x - self.baseX
    deltaY = y - self.baseY
    
    if (self.l + deltaX < 0):
      deltaX = self.l
      
    if (self.r + deltaX >= self.canvas.width):
      deltaX = self.canvas.width - self.r
      
    if (self.t + deltaY < 0):
      deltaY = self.t
      
    if (self.b + deltaY >= self.canvas.height):
      deltaY = self.canvas.height - self.b
    
    self.l += deltaX
    self.r += deltaX
    self.baseX += deltaX
    self.t += deltaY
    self.b += deltaY
    self.baseY += deltaY

    self.selector.style.left = "{}px".format(self.l)
    self.selector.style.top = "{}px".format(self.t)
    self.selector.style.width = "{}px".format(self.r - self.l + 1)
    self.selector.style.height = "{}px".format(self.b - self.t + 1)
  
  
  def resize_selector(self, dir, x, y):
    def sign(x):
      return 1 if x >= 0 else -1
    
    
    def adjust(dx, dy, esx, esy):
      d, sx, sy = min(abs(dx), abs(dy)), sign(dx), sign(dy)
      
      if (sx * sy == esx * esy):
        return (d * sx, d * sy)
      else:
        return (0, 0)
    
    
    if (dir == "NW"):
      deltaX = x - self.l
      deltaY = y - self.t
      console.log("NW (0): deltaX={}, deltaY={}".format(deltaX, deltaY))

      if (self.l + deltaX < 0):
        deltaX = self.l
      
      if (self.l + deltaX >= self.r - 30):
        deltaX = self.r - self.l - 30
      
      if (self.t + deltaY < 0):
        deltaY = self.t
      
      if (self.t + deltaY >= self.b - 30):
        deltaY = self.b - self.t - 30

      console.log("NW (1): deltaX={}, deltaY={}".format(deltaX, deltaY))
      deltaX, deltaY = adjust(deltaX, deltaY, -1, -1)
      console.log("NW (2): deltaX={}, deltaY={}".format(deltaX, deltaY))
      self.l += deltaX
      self.t += deltaY
    elif (dir == "NE"):
      deltaX = x - self.r
      deltaY = y - self.t

      if (self.r + deltaX >= self.canvas.width):
        deltaX = self.canvas.width - self.r
      
      if (self.r + deltaX <= self.l + 30):
        deltaX = self.l + 30 - self.r
      
      if (self.t + deltaY < 0):
        deltaY = self.t
      
      if (self.t + deltaY >= self.b - 30):
        deltaY = self.b - 30 - self.t

      deltaX, deltaY = adjust(deltaX, deltaY, 1, -1)
      self.r += deltaX
      self.t += deltaY
    elif (dir == "SW"):
      deltaX = x - self.l
      deltaY = y - self.b

      if (self.l + deltaX < 0):
        deltaX = self.l
      
      if (self.l + deltaX >= self.r - 30):
        deltaX = self.r - self.l - 30
      
      if (self.b + deltaY <= self.t + 30):
        deltaY = self.t + 30 - self.b
      
      if (self.b + deltaY >= self.canvas.height):
        deltaY = self.canvas.height - self.b

      deltaX, deltaY = adjust(deltaX, deltaY, -1, 1)
      self.l += deltaX
      self.b += deltaY
    elif (dir == "SE"):
      deltaX = x - self.r
      deltaY = y - self.b

      if (self.r + deltaX >= self.canvas.width):
        deltaX = self.canvas.width - self.r
      
      if (self.r + deltaX <= self.l + 30):
        deltaX = self.l + 30 - self.r
      
      if (self.b + deltaY <= self.t + 30):
        deltaY = self.t + 30 - self.b
      
      if (self.b + deltaY >= self.canvas.height):
        deltaY = self.canvas.height - self.b

      deltaX, deltaY = adjust(deltaX, deltaY, 1, 1)
      self.r += deltaX
      self.b += deltaY
    
    
    self.baseX = int(self.r + self.l) / 2
    self.baseY = int(self.b + self.t) / 2
    
    self.selector.style.left = "{}px".format(self.l)
    self.selector.style.top = "{}px".format(self.t)
    self.selector.style.width = "{}px".format(self.r - self.l + 1)
    self.selector.style.height = "{}px".format(self.b - self.t + 1)
  
  
  def __selector_start_event(self, target, x, y):
    if (target == "mandelbrot"):
      if (self.action is None):
        self.place_selector(x, y)
    else:
      if (self.action == "select"):
        if (self.baseX - 10 <= x <= self.baseX + 10 and self.baseY - 10 <= y <= self.baseY + 10):
          self.action = "moving"
        elif (self.l <= x <= self.l + 20):
          if (self.t <= y <= self.t + 20):
            self.action = "resize-NW"
          elif (self.b - 20 <= y <= self.b):
            self.action = "resize-SW"
        elif (self.r - 20 <= x <= self.r):
          if (self.t <= y <= self.t + 20):
            self.action = "resize-NE"
          elif (self.b - 20 <= y <= self.b):
            self.action = "resize-SE"
  
  
  def __selector_move_event(self, x, y):
    if (self.action is not None):
      if (self.action == "moving"):
        self.move_selector(x, y)
        
        return False
      elif (self.action.startswith("resize-")):
        self.resize_selector(self.action[-2:], x, y)
        
        return False
  
  
  def __selector_end_event(self):
    if (self.action is not None and (self.action == "moving" or self.action.startsWith("resize-"))):
      self.action = "select"
      
      return False
  
  
  def on_mousedown(self, e):
    self.__selector_start_event(e.target.id, e.clientX, e.clientY)
  
  
  def on_touchstart(self, e):
    self.__selector_start_event(e.target.id, e.targetTouches[0].clientX, e.targetTouches[0].clientY)
  
  
  def on_mousemove(self, e):
    ret = self.__selector_move_event(e.clientX, e.clientY)
    
    if (ret is False):
      return False
  
  
  def on_touchmove(self, e):
    ret = self.__selector_move_event(e.targetTouches[0].clientX, e.targetTouches[0].clientY)
    
    if (ret is False):
      return False
  
  
  def on_mouseup(self, e):
    ret = self.__selector_end_event()
    
    if (ret is False):
      return False
  
  
  def on_touchend(self, e):
    self.on_mouseup(e)


mandelbrot = Mandel()