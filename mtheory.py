import pygame, sys
import pygame.midi
from pygame.locals import *

pygame.init()
pygame.midi.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post

pygame.midi.init()

i = pygame.midi.Input( 3 ) # using 1 for programming purposes, default input is '3'

GAME_WIDTH = 800
GAME_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('CURSO PAJD - MTHEORY')
SCALE = 3
PIANO_X = 35
PIANO_Y = 240
wkeypat = [1, 2, 3, 1, 2, 2, 3]
bkey_skip_pat = [2, 3]
wkey_offset = 21
bkey_offset = 22
octaves = 5
oc = 1

white_keys = [0, 2, 4, 5, 7, 9, 11]
black_keys = [1, 3, 6, 8, 10]
piano_map = [False] * 60 # initializes all keys as 'False' which means they are not being pressed

fpsClock = pygame.time.Clock()
FPS = 30
dt = 0

# DONE!!: Implement method to return scaled image 
# DONE!!: Define screen size and piano octave lenght
# DONE!!: Implement for structure to draw whole piano
# DONE!!: Implement MIDI Input feature to light specific piano key when pressed
# TODO: Implement scales, chords and commands to change piano key highlight

def octs_pkey(keytype, num):
	cont = 0
	if keytype == 'white':
		while num >= 7:
			num -= 7
			cont += 1
	
		if num < 0:
			num = 0
		return num, cont

	elif keytype == 'black':
		
		while num >= 5:
			num -= 5
			cont += 1		

		if num < 0:
			num = 0
		return num, cont

def check_pressed(keytype, key):

	if keytype == 'white':
		if key < 7:
			return piano_map[ white_keys[key] ]
		elif key >= 7:
			return piano_map[ white_keys[ octs_pkey(keytype, key)[0] ] + octs_pkey(keytype, key)[1] * 12 ]
	elif keytype == 'black':
		if key < 5:
			return piano_map[ black_keys[key] ]
		elif key >= 5:
			return piano_map[ black_keys[ octs_pkey(keytype, key)[0] ] + octs_pkey(keytype, key)[1] * 12 ]
	else:
		return False

def load_assets():
	assets = {}
	temp = None
	cont = 0
	assetname = ['wpat', 'wpat', 'wpat', 'bpat1']
	assetcont = 1
	while cont <= 8:
		if cont % 2 == 0:
			temp = pygame.image.load('img/' + assetname[assetcont - 1] + ('', str(assetcont))[ assetcont != 4 ] + '.png')
			temp = pygame.transform.scale(temp, (temp.get_width() * SCALE, temp.get_height() * SCALE))
			assets[assetname[assetcont - 1].upper() + ('', str(assetcont))[ assetcont != 4 ]] = temp
			if cont != 0:
				assetcont += 1						
		else:
			temp = pygame.image.load('img/' + assetname[assetcont - 1] + ('', str(assetcont))[assetcont != 4] + '_pressed.png')		
			temp = pygame.transform.scale(temp, (temp.get_width() * SCALE, temp.get_height() * SCALE))
			assets[assetname[assetcont - 1].upper() + ('', str(assetcont))[ assetcont != 4 ] +  '_PRESSED'] = temp
		
		cont += 1
	return assets

piano = load_assets()

while True:
	
	events = event_get()
	for e in events:
		if e.type == KEYDOWN and e.key == K_ESCAPE:
			pygame.midi.quit()
			pygame.quit()
			sys.exit()
			del i			
		if e.type in [pygame.midi.MIDIIN]:
			print(e)
			if e.status == 144 or e.status == 128 and e.data1 <= 95 and e.data1 >= 36:
				if  e.data2 >= 1 and e.status == 144:
					piano_map[ e.data1 - 36 ] = True
				elif  e.data2 == 0 or e.status == 128:
					piano_map[ e.data1 - 36 ] = False
	
	if i.poll():
		midi_events = i.read(10)
		# convert them into pygame events
		midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

		for m_e in midi_evs:
			event_post( m_e )	

	# draws background	
	pygame.draw.rect(DISPLAYSURF, ( 12, 12, 12), (0, 0, GAME_WIDTH, GAME_HEIGHT))
	
	# draws white keys
	wcont = 0
	while wcont < 35:
		if check_pressed('white', wcont):
			pressed = '_PRESSED'
		else:
			pressed = ''
		DISPLAYSURF.blit(piano['WPAT' + str(wkeypat[wcont % 7]) + pressed], (PIANO_X + wkey_offset * wcont, PIANO_Y))		
		wcont += 1	
	
	# draws black keys
	bcont = 0
	skip_cont = 0
	skip_current = 0
	bskip_offset = 0
	balancer = 0
	while bcont < 25:		
		
		if check_pressed('black', bcont):
			bpressed = '_PRESSED'
		else:
			bpressed = ''

		if skip_cont == bkey_skip_pat[skip_current]:
			bskip_offset += 19.5
			skip_current += 1
			balancer += 1
			skip_cont = 0
			if skip_current >= len(bkey_skip_pat):
				skip_current = 0
		DISPLAYSURF.blit(piano['BPAT1' + bpressed ], (PIANO_X + 12 + (bkey_offset * bcont - balancer) + bskip_offset, PIANO_Y))
		bcont += 1
		skip_cont += 1	

	pygame.display.update()
	dt = 1 / fpsClock.tick(FPS)	
