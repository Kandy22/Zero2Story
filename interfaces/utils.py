import copy
import json
import string
import random

from modules import palmchat
from pingpong.context import CtxLastWindowStrategy

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def parse_first_json_code_snippet(code_snippet):
	json_parsed_string = None
	
	try:
		json_parsed_string = json.loads(code_snippet, strict=False)
	except:
		json_start_index = code_snippet.find('```json')
		json_end_index = code_snippet.find('```', json_start_index + 6)

		if json_start_index < 0 or json_end_index < 0:
			raise ValueError('No JSON code snippet found in string.')

		json_code_snippet = code_snippet[json_start_index + 7:json_end_index]
		json_parsed_string = json.loads(json_code_snippet, strict=False)
	finally:
		return json_parsed_string

async def retry_until_valid_json(prompt, parameters=None):
	response_json = None
	while response_json is None:
		_, response_txt = await palmchat.gen_text(prompt, mode="text", parameters=parameters)
		print(response_txt)

		try:
			response_json = parse_first_json_code_snippet(response_txt)
		except:
			pass
			
	return response_json

def build_prompts(ppm, win_size=3):
	dummy_ppm = copy.deepcopy(ppm)
	lws = CtxLastWindowStrategy(win_size)
	return lws(dummy_ppm)

async def get_chat_response(prompt, ctx=None):
	parameters = {
		'model': 'models/chat-bison-001',
		'candidate_count': 1,
		'context': "" if ctx is None else ctx,
		'temperature': 1.0,
		'top_k': 50,
		'top_p': 0.9,
	}
	
	_, response_txt = await palmchat.gen_text(
		prompt, 
		parameters=parameters
	)

	return response_txt
