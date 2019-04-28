import json

def save_class (cls, file_path):
	with open(file_path, "w") as save_file:
		save_file.write(json.dumps(cls.__dict__))

def load_class (cls, file_path):
	with open(file_path, "r") as save_file:
		cls.__dict__ = json.load(save_file)

def scale_vector (vector, scalar):
	return [vector[0] * scalar, vector[1] * scalar]

def add_vectors (v1, v2):
	return [v1[0] + v2[0], v1[1] + v2[1]]