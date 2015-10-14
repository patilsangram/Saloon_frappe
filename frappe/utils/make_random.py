import frappe, random

settings = frappe._dict(
	prob = {
		"default": { "make": 0.6, "qty": (1,5) },
	}
)

def add_random_children(doc, fieldname, rows, randomize, unique=None):
	nrows = rows
	if rows > 1:
		nrows = random.randrange(1, rows)

	for i in xrange(nrows):
		d = {}
		for key, val in randomize.items():
			if isinstance(val[0], basestring):
				d[key] = get_random(*val)
			else:
				d[key] = random.randrange(*val)

		if unique:
			if not doc.get(fieldname, {unique:d[unique]}):
				doc.append(fieldname, d)
		else:
			doc.append(fieldname, d)

def get_random(doctype, filters=None):
	condition = []
	if filters:
		for key, val in filters.items():
			condition.append("%s='%s'" % (key, str(val).replace("'", "\'")))
	if condition:
		condition = " where " + " and ".join(condition)
	else:
		condition = ""

	out = frappe.db.sql("""select name from `tab%s` %s
		order by RAND() limit 0,1""" % (doctype, condition))

	return out and out[0][0] or None

def can_make(doctype):
	return random.random() < settings.prob.get(doctype, settings.prob["default"])["make"]

def how_many(doctype):
	return random.randrange(*settings.prob.get(doctype, settings.prob["default"])["qty"])
