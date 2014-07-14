#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call, Popen, PIPE
from spotify import Link, Image
from jukebox import Jukebox, container_loaded
import os, sys
import threading
import time

playback = False

pipe = None
ripping = False
end_of_track = threading.Event()

def printstr(str):
	sys.stdout.write(str)
	sys.stdout.flush()

def shell(cmdline):
	call(cmdline, shell=True)

def rip_init(session, track):
	global pipe, ripping
	num_track = "%02d" % (track.index(),)
	mp3file = track.name() + ".mp3"
	directory = os.getcwd() + "/" + track.artists()[0].name() + "/" + track.album().name() + "/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	printstr("ripping " + mp3file + "...")
	p = Popen("lame --silent -V2 -h -r - \"" + directory + mp3file + "\"", stdin=PIPE, shell=True)
	pipe = p.stdin
	ripping = True

def rip_terminate(session, track):
	global ripping
	if pipe is not None:
		print(' done!')
		pipe.close()
	ripping = False

def rip(session, frames, frame_size, num_frames, sample_type, sample_rate, channels):
	if ripping:
		printstr('.')
		pipe.write(frames);

def rip_id3(session, track):
	num_track = "%02d" % (track.index(),)
	mp3file = track.name() + ".mp3"
	artist = track.artists()[0].name()
	album = track.album().name()
	title = track.name()
	year = track.album().year()
	directory = os.getcwd() + "/" + track.artists()[0].name() + "/" + track.album().name() + "/"

	image = session.image_create(track.album().cover())
	while not image.is_loaded():
		time.sleep(0.1)
	fh_cover = open('cover.jpg', 'wb')
	fh_cover.write(image.data())
	fh_cover.close()

	cmd = "eyeD3 -2" + \
		  " --add-image cover.jpg:FRONT_COVER" + \
		  " -t \"" + title + "\"" + \
		  " -a \"" + artist + "\"" + \
		  " -A \"" + album + "\"" + \
		  " -n " + str(num_track) + \
		  " -Y " + str(year) + \
		  " \"" + directory + mp3file + "\""
	shell(cmd)

	shell("rm -f cover.jpg")

class RipperThread(threading.Thread):
	def __init__(self, ripper):
		threading.Thread.__init__(self)
		self.ripper = ripper

	def run(self):
		container_loaded.wait()
		container_loaded.clear()

		link = Link.from_string(sys.argv[3])
		if link.type() == Link.LINK_TRACK:
			track = link.as_track()
			itrack = iter([track])
		elif link.type() == Link.LINK_PLAYLIST:
			playlist = link.as_playlist()
			print('loading playlist...')
			while not playlist.is_loaded():
				time.sleep(0.1)
			print('done')
			itrack = iter(playlist)

		session = self.ripper.session
		for track in itrack:

			self.ripper.load_track(track)

			rip_init(session, track)

			self.ripper.play()

			end_of_track.wait()
			end_of_track.clear()

			rip_terminate(session, track)
			rip_id3(session, track)

		self.ripper.disconnect()

class Ripper(Jukebox):
	def __init__(self, *a, **kw):
		Jukebox.__init__(self, *a, **kw)
		self.ui = RipperThread(self)
		self.session.set_preferred_bitrate(2)

	def music_delivery_safe(self, session, frames, frame_size, num_frames, sample_type, sample_rate, channels):
		rip(session, frames, frame_size, num_frames, sample_type, sample_rate, channels)
		if playback:
			return Jukebox.music_delivery_safe(self, session, frames, frame_size, num_frames, sample_type, sample_rate, channels)
		else:
			return num_frames

	def end_of_track(self, session):
		Jukebox.end_of_track(self, session)
		end_of_track.set()

if __name__ == '__main__':
	if len(sys.argv) >= 3:
		ripper = Ripper(sys.argv[1], sys.argv[2])
		ripper.connect()
	else:
		print "usage: \n"
		print "     ./sputrifis.py [username] [password] [spotify_url]"
		print "example: \n"
		print "     ./sputrifis.py javirevillas 123456 spotify:track:0q6LuUqGLUiCPP1cbdwFs3"
		print "     ./sputrifis.py javirevillas 123456 spotify:user:aguarate:playlist:77sxS8MfEXMvgD1t5JikQq"