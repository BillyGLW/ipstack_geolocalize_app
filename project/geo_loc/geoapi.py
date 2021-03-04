from ipstack import GeoLookup

class GeoApi(GeoLookup):
	to_alias = {
				'protocol': 'type',
				'zip_number': 'zip'
				}
	geo_loc_fields = ['ip', 'protocol']

	def __init__(self, access_key):
		self.access_key = access_key
		self.data = None
		super().__init__(self.access_key)

	def alliased(func, to_alias=to_alias):
		def wrapper(*args, **kwargs):
			_ret = func(*args, **kwargs)
			for index, value in to_alias.items():
				_ret[index] = _ret.pop(value)
			return _ret
		return wrapper

	def serializer(f):
		def wrapper(*args, **kwargs):
			_region_dict = dict()
			data = dict()
			_data = f(*args, **kwargs)
			for key, value in _data.items():
				if key not in ['ip', 'protocol']:
					_region_dict[key] = _data[key]
					continue
				data[key] = value
			data.update({'region': _region_dict})
			return data
		return wrapper

	@serializer
	@alliased
	def get_location(self, *ips):
		return super().get_location(*ips)