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
  
  def startup(self):
    print("let's go!")
    

  def drawPixel(self, x, y, c):
    self.ctx.fillStyle = c
    self.ctx.fillRect(int(x * self.ratio), int(y * self.ratio), int(self.ratio), int(self.ratio))
  
  
  def getColor(self, cr, ci):
    zr, zi = cr, ci
    
    iter = 1
    
    while True:
      zr, zi = zr * zr - zi * zi + cr, 2 * zr * zi + ci
      
      if (zr * zr + zi * zi > 4):
        return max(0, 256 - iter)
      
      if (iter > self.max_iter):
        return 0
      
      iter += 1
  
  
  def draw(self):
    canvas = document.getElementById("mandelbrot")
    self.ctx = canvas.getContext("2d")
    
    self.width = int(document.getElementById("txt_width").value)
    self.ratio = min(canvas.width, canvas.height) / self.width
    self.max_iter = int(document.getElementById("txt_max_iter").value)
    
    print(self.width, self.ratio, self.max_iter)
    
    for y in range(int((self.width + 9) / 10)):
      print("y={}".format(y))
      
      self.drawLine(y * 10)
  
  
  def drawLine(self, y0):
    f = 2.5 / self.width
  
    for y in range(y0, y0 + 10):
      for x in range(self.width):
        cr = -2.0 + x * f
        ci = 1.25 - y * f
        # c = complex(-2.0 + x * f, 1.25 - y * f)
        c = self.getColor(cr, ci)
        color = rgb(c, 4 * c, 16 * c)

        # print("\tm(x={},y={})={}, color={3}".format(x,y,c,rgb(c,c,c)))
        
        self.drawPixel(x, y, color)


mandelbrot = Mandel()