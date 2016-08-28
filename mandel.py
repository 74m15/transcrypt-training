from math import cos, sqrt, pi

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
    self.mandel_left = -2.0
    self.mandel_top = 1.25
    self.mandel_right = 0.5
    self.mandel_bottom = -1.25
  
  
  def startup(self):
    print("let's go!")
    
    self.resizing = 0
    self.worker = __new__(Worker("../worker.js"))
    self.worker.onmessage = self.on_message

    self.reset()
    
    self.selector = document.getElementById("selector")
    self.canvas = document.getElementById("mandelbrot")
    self.ctx = self.canvas.getContext("2d")

    document.getElementById("container").onmousedown = self.on_mousedown
    document.getElementById("container").onmousemove = self.on_mousemove
    document.getElementById("container").onmouseup = self.on_mouseup
    
    document.getElementById("container").ontouchstart = self.on_touchstart
    document.getElementById("container").ontouchmove = self.on_touchmove
    document.getElementById("container").ontouchend = self.on_touchend
  
  
  def drawPixel(self, x, y, c):
    self.ctx.fillStyle = c
    self.ctx.fillRect(int(x * self.ratio), int(y * self.ratio), int(self.ratio), int(self.ratio))
  
  
#  def getColor(self, cr, ci):
#    zr, zi = cr, ci
#    
#    iter = 1
#    
#    while True:
#      zr, zi = zr * zr - zi * zi + cr, 2 * zr * zi + ci
#      
#      if (zr * zr + zi * zi > 4):
#        return iter
#      
#      if (iter > self.max_iter):
#        return 0
#      
#      iter += 1
#  
#  
#  def drawLine(self, y0):
#    f = (self.mandel_right - self.mandel_left) / self.width
#  
#    for y in range(y0, y0 + 10):
#      for x in range(self.width):
#        cr = self.mandel_left + x * f
#        ci = self.mandel_top - y * f
#        # c = complex(-2.0 + x * f, 1.25 - y * f)
#        c = self.getColor(cr, ci)
#        color = rgb(int(c) & 0xFF, int(4 * c) & 0xFF, int(16 * c) & 0xFF)
#
#        # print("\tm(x={},y={})={}, color={3}".format(x,y,c,rgb(c,c,c)))
#        
#        self.drawPixel(x, y, color)
#  
#  
#  def draw(self):
#    self.width = int(document.getElementById("txt_width").value)
#    self.ratio = min(self.canvas.width, self.canvas.height) / self.width
#    self.max_iter = int(document.getElementById("txt_max_iter").value)
#    
#    self.selector.style.visibility = "hidden"
#    
#    print(self.width, self.ratio, self.max_iter)
#    print(self.mandel_left, self.mandel_top, self.mandel_right, self.mandel_bottom)
#    
#    for y in range(int((self.width + 9) / 10)):
#      self.drawLine(y * 10)
  
  
  def getColor(self, c):
    if (c == 0):
      return (0,0,0)
    
    r = int(255 * (1 + cos(sqrt(c))) / 2)
    g = int(255 * (1 + cos(sqrt(2 * c))) / 2)
    b = int(255 * (1 + cos(sqrt(3 * c) + pi / 4)) / 2)
    
    return (r, g, b)
  
  
  def updateProgress(self):
      progress = int(100 * (self.rows_done + 1) / self.width)
      
      document.getElementById("progress-bar").style.width = "{}%".format(progress)
  
  
  def on_message(self, e):
    self.rows_done += 1
    
    self.updateProgress()
    
    for p in e.data:
      r, g, b = self.getColor(p.c)
      
      self.drawPixel(p.x, p.y, rgb(r, g, b))
  
  
  def draw(self):
    self.width = int(document.getElementById("txt_width").value)
    self.ratio = min(self.canvas.width, self.canvas.height) / self.width
    self.max_iter = int(document.getElementById("txt_max_iter").value)
    
    if (self.selector.style.visibility == "visible"):
      self.define_selection()
      self.selector.style.visibility = "hidden"
    
    print(self.width, self.ratio, self.max_iter)
    print(self.mandel_left, self.mandel_top, self.mandel_right, self.mandel_bottom)
    
    self.rows_done = 0
    
    self.updateProgress()
    
    self.worker.postMessage({
      "cmd":'start', 
      "width":self.width, 
      "max_iter":self.max_iter,
      "left":self.mandel_left,
      "top":self.mandel_top,
      "right":self.mandel_right,
      "bottom":self.mandel_bottom})
    
  
  def start_selection(self, x, y):
    self.resizing = 1
    self.baseX = x
    self.baseY = y
    
    self.selector.style.visibility = "visible"
    self.selector.style.left = "{}px".format(x)
    self.selector.style.top = "{}px".format(y)
    self.selector.style.width = "10px"
    self.selector.style.height = "10px"
  
  
  def adjustBox(self, bX, bY, eX, eY):
      deltaX = bX - eX + 1
      deltaY = bY - eY + 1
      delta = max(10, abs(deltaX), abs(deltaY))
      
      if (deltaX > 0):
        left = bX - delta
      else:
        left = bX
      
      if (deltaY > 0):
        top = bY - delta
      else:
        top = bY

      return (left, top, left + delta - 1, top + delta - 1)
  
  
  def modify_selection(self, x, y):
    self.l, self.t, self.r, self.b = self.adjustBox(self.baseX, self.baseY, x, y)
    
    self.selector.style.left = "{}px".format(self.l)
    self.selector.style.top = "{}px".format(self.t)
    self.selector.style.width = "{}px".format(self.r - self.l + 1)
    self.selector.style.height = "{}px".format(self.b - self.t + 1)
  
  
  def define_selection(self):
    self.mandel_left, self.mandel_top, self.mandel_right, self.mandel_bottom = \
      self.mandel_left + (self.mandel_right - self.mandel_left) * self.l / self.canvas.width, \
      self.mandel_top - (self.mandel_top - self.mandel_bottom) * self.t / self.canvas.height, \
      self.mandel_left + (self.mandel_right - self.mandel_left) * self.r / self.canvas.width, \
      self.mandel_top - (self.mandel_top - self.mandel_bottom) * self.b / self.canvas.height
      
    print(self.mandel_left, self.mandel_top, self.mandel_right, self.mandel_bottom)
  
  
  def on_mousedown(self, e):
    if (e.target.id == "mandelbrot"):
      self.start_selection(e.clientX, e.clientY)
      
      return False
  
  
  def on_touchstart(self, e):
    if (e.target.id == "mandelbrot"):
      self.start_selection(e.targetTouches[0].clientX, e.targetTouches[0].clientY)
      
      return False
  
  
  def on_mousemove(self, e):
    if (self.resizing == 1):
      self.modify_selection(e.clientX, e.clientY)
      
      return False
  
  
  def on_touchmove(self, e):
    if (self.resizing == 1):
      self.modify_selection(e.targetTouches[0].clientX, e.targetTouches[0].clientY)
      
      return False
  
  
  def on_mouseup(self, e):
    if (self.resizing == 1):
      self.resizing = 0
      
      return False
  
  
  def on_touchend(self, e):
    if (self.resizing == 1):
      self.resizing = 0
      
      return False


mandelbrot = Mandel()