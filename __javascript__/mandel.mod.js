	(function () {
		var __symbols__ = ['__esv5__'];
		var rgb = function (r, g, b) {
			var _hex = function (x) {
				var _SYM_ = '0123456789abcdef';
				var res = list (['0', '0']);
				for (var i = 0; i < 2; i++) {
					var __left0__ = tuple ([Math.floor (x / 16), x % 16]);
					var x = __left0__ [0];
					var r = __left0__ [1];
					res [1 - i] = _SYM_ [r];
				}
				return ''.join (res);
			};
			return '#{0}{1}{2}'.format (_hex (r), _hex (g), _hex (b));
		};
		var Mandel = __class__ ('Mandel', [object], {
			get __init__ () {return __get__ (this, function (self) {
				// pass;
			});},
			get startup () {return __get__ (this, function (self) {
				print ("let's go!");
			});},
			get drawPixel () {return __get__ (this, function (self, x, y, c) {
				self.ctx.fillStyle = c;
				self.ctx.fillRect (int (x * self.ratio), int (y * self.ratio), int (self.ratio), int (self.ratio));
			});},
			get getColor () {return __get__ (this, function (self, cr, ci) {
				var __left0__ = tuple ([cr, ci]);
				var zr = __left0__ [0];
				var zi = __left0__ [1];
				var py_iter = 1;
				while (true) {
					var __left0__ = tuple ([(zr * zr - zi * zi) + cr, (2 * zr) * zi + ci]);
					var zr = __left0__ [0];
					var zi = __left0__ [1];
					if (zr * zr + zi * zi > 4) {
						return max (0, 256 - py_iter);
					}
					if (py_iter > self.max_iter) {
						return 0;
					}
					py_iter++;
				}
			});},
			get draw () {return __get__ (this, function (self) {
				var canvas = document.getElementById ('mandelbrot');
				self.ctx = canvas.getContext ('2d');
				self.width = int (document.getElementById ('txt_width').value);
				self.ratio = min (canvas.width, canvas.height) / self.width;
				self.max_iter = int (document.getElementById ('txt_max_iter').value);
				print (self.width, self.ratio, self.max_iter);
				for (var y = 0; y < int ((self.width + 9) / 10); y++) {
					print ('y={}'.format (y));
					self.drawLine (y * 10);
				}
			});},
			get drawLine () {return __get__ (this, function (self, y0) {
				var f = 2.5 / self.width;
				for (var y = y0; y < y0 + 10; y++) {
					for (var x = 0; x < self.width; x++) {
						var cr = -(2.0) + x * f;
						var ci = 1.25 - y * f;
						var c = self.getColor (cr, ci);
						var color = rgb (c, 4 * c, 16 * c);
						self.drawPixel (x, y, color);
					}
				}
			});}
		});
		var mandelbrot = Mandel ();
		__pragma__ ('<all>')
			__all__.Mandel = Mandel;
			__all__.mandelbrot = mandelbrot;
			__all__.rgb = rgb;
		__pragma__ ('</all>')
	}) ();
