scales = {
			"major": {
						"Name": "Escala Maior",
						"Formula": "T T s T T T s",
						"Description": "Escala bastante usada na musica popular. Tem uma sonoridade vibrante, alegre, feliz."
					},
			"minor": {
						"Name": "Escala Menor",
						"Formula": "T s T T s T T",
						"Description": "Possui uma sonoridade triste e geralmente e utilizada em contextos melancolicos."
					 },
			"pentatonic": {
						"Name": "Escala Pentatonica",
						"Formula": "T T x T x",
						"Description": "Escala com sonoridade oriental muito utilizada em improvisos"
					 }
		}

def seed_scales_with_proper_number_progression():
	global scales
	for k, v in scales.items():
		np = []
		np.append(0)
		cont = 2
		scont = 0
		while cont < 61:
			if scont >= len(v["Formula"]):
				scont = 0
			if v["Formula"][scont] == "T":
				np.append(np[ len(np) - 1] + 2)
				cont += 2
			elif v["Formula"][scont] == "s":
				np.append(np[ len(np) - 1] + 1)
				cont += 1
			elif v["Formula"][scont] == "x":
				np.append(np[ len(np) - 1] + 3)
				cont += 3
			scont += 2
		
		v["progression"] = np

