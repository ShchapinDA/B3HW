class Tag:
	def __init__(self, tag, is_single=False, klass=None, **kwargs):
		self.tag = tag
		self.text = ""
		self.attributes = {}
		self.is_single = is_single
		self.children = []

		if klass is not None:
			self.attributes["class"]= " ".join(klass)

		for attr, value in kwargs.items():
			if "_" in attr:
				attr = attr.replace("_","-")
			self.attributes[attr] = value

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		return self

	def __str__(self):
		attrs = []
		for attribute, value in self.attributes.items():
			attrs.append(' %s="%s"' % (attribute, value))
		attrs = "".join(attrs)

		if self.children:
			opening = "\n<{tag}{attrs}>\n".format(tag=self.tag,attrs=attrs)
			if self.text:
				internal ="%s" % self.text
			else:
				internal =""
			for child in self.children:
				internal += str(child)
			ending = "\n</%s>" % self.tag
			return opening + internal + ending
		else:
			if self.is_single:
				return "\n<{tag}{attrs}/>".format(tag=self.tag, attrs=attrs)
			else:
				return "<{tag}{attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text)
	def __iadd__(self, other):
		self.children.append(other)
		return self

class TopLevelTag:
	def __init__(self, tag, **kwargs):
		self.tag = tag
		self.attributes = {}
		self.children = []

		for attr, value in kwargs.items():
			if "_" in attr:
				attr = attr.replace("_","-")
			self.attributes[attr] = value

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		return self

	def __str__(self):
		attrs = []
		for attribute, value in self.attributes.items():
			attrs.append(' %s="%s"' % (attribute, value))
		attrs = "".join(attrs)

		opening = "\n<{tag}{attrs}>\n".format(tag=self.tag,attrs=attrs)
		for child in self.children:
			opening += str(child)
		ending = "\n</%s>" % self.tag
		return opening + ending

	def __iadd__(self, other):
		self.children.append(other)
		return self

class HTML:
	def __init__(self, output=None):
		self.output = output
		self.children = []

	def __enter__(self):
		return self

	def __exit__(self, *args, **kwargs):
		if self.output is not None:
			with open(self.output, "w") as html_file:
				html_file.write(str(self))
		else:
			print(self)

	def __str__(self):
		opening = "<HTML>"
		for child in self.children:
			opening += str(child)
		ending = "\n</HTML>"
		return opening + ending

	def __iadd__(self, other):
		self.children.append(other)
		return self



