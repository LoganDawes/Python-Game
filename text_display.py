import sys
import time

def text_display(text):
	for char in text:
		sys.stdout.write(char)
		sys.stdout.flush()
		time.sleep(0.02)
	if text[-1] != "\n":
		print()