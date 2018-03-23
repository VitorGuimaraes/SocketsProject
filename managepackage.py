import json

def jsonDefault(object):
	return object.__dict__

class ManagePackage():
	
	def pack_json(self, data):
		return json.dumps(data, default = jsonDefault)

	def unpack_json(self, package):
		return json.loads(package)