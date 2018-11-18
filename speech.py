import speech_recognition as sr 

class Speech():

	def __init__(self):
		pass

	def recognize_speech(self, recognizer, microphone):
		if not isinstance(recognizer, sr.Recognizer):
			raise TypeError('Recognizer must be a recognizer instance')
		if not isinstance(microphone, sr.Microphone):
			raise TypeError('Microphone must be a microphone instance')

		with microphone as source:
			recognizer.adjust_for_ambient_noise(source)
			audio = recognizer.listen(source)

		response = {
			'success': True,
			'error': None,
			'transcription': None
		}

		try:
			response['transcription'] = recognizer.recognize_google(audio, language='de-DE')
		except sr.RequestError:
			response['success'] = False
			response['error'] = 'API unavailable'
		except sr.UnknownValueError:
			response['error'] = 'Unable to recognize speech'

		return response
