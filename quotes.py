#!/usr/bin/env python

from SimpleCV import Camera, Display, Image, Color
from translator import Translator
from time import sleep


sentences = ["http://blogiceo.nq.pl/patrycjagata/files/2013/03/GkdFC.png",
			"http://shapeshed.com/images/articles/pizza_quote.png",
			"http://media-cache-is0.pinimg.com/192x/80/0b/f5/800bf536adfb16dcdf73e5043c22d825.jpg",
			"http://24.media.tumblr.com/bc45a06051f6cbfe8843e6a16e102436/tumblr_mgfrulxZfm1s2579io1_500.jpg"]

trans = Translator()
langpair = 'en|es'


def cleanText(text): return ' '.join([e.strip() for e in text.replace('\n', ' ').split(' ') if e])


def translateQuotes():
	[lan1, lan2] = langpair.split('|')
	for src in sentences:
		try:
			img = Image(src)
			text = img.binarize().readText()
		except Exception as e:
			print e
			print '###'
		else:
			cleantext = cleanText(text)
			translated = trans.translate(cleantext, langpair)
			img.drawText(translated, 0, 0, color=Color.BLACK, fontsize=28)
			img.show()
			print lan1 + ": " + cleantext
			print lan2 + ": " + translated.encode('utf-8')
			print '###'
			sleep(1)


def interactiveTranslation():
	cam = Camera()
	disp = Display()
	current = " "
	while disp.isNotDone():
		image = cam.getImage()
		if disp.mouseLeft: break
		if disp.mouseRight:
			text = image.readText()
			text = cleanText(text)
			translated = trans.translate(text, langpair)
			if translated: current = translated
		image.drawText(current, 0, 0, color=Color.BLACK, fontsize=40)
		image.save(disp)


if __name__ == '__main__':
	translateQuotes()
	# interactiveTranslation()
