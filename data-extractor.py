import re

class MEDTEXRecord(object):
	def __init__(self, patient):
		self.patient = patient

	def to_csv(self):
		return "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % ( self.patient["keycode"],
			self.patient["last_name"],
			self.patient["first_name"],
			self.patient["sex"],
			self.patient["health_number"],
			self.patient["version"],
			#self.patient["rmb_ohip"],
			self.patient["address"],
			self.patient["city"],
			self.patient["province"],
			self.patient["post_code"],
			self.patient["birth_date"],
			self.patient["chart"],
			self.patient["class"],
			self.patient["referring_physician_initial"],
			self.patient["referring_physician_last_name"],
			self.patient["referring_physician_number"],
			self.patient["home_phone"],
			self.patient["bus_phone"],
			self.patient["adm_date"],
			self.patient["comments"],
			self.patient["billing"],
			self.patient["default_diag"],
			self.patient["suscribed_last_name"],
			self.patient["date_entered"],
			self.patient["last_updated"],
			self.patient["last_visit"])

class MEDTEXDataReader(object):
	def __init__(self, filename):
 		fi = open(filename)
 		self.data = fi.read()

class MEDTEXRecordParser(object):
	def patients(self, binary_data_dissasambler):
		return self._parse(binary_data_dissasambler.records())

	def _parse(self, records):
		patients = []
		for record in records:
			patients.append(self._build_patient(record))
		return patients

	def _build_patient(self, record):
		patient = {}
		patient["keycode"] = record[0:7].rstrip() #7
		patient["last_name"] = record[7:21].rstrip() #14
		patient["first_name"] = record[21:31].rstrip() # 10
		patient["sex"] = record[31:44].rstrip() #13
		patient["health_number"] = record[44:54].rstrip() #10
		patient["version"] = record[54:56].rstrip() #2
		#patient["rmb_ohip"] = record[44:55]
		patient["address"] = record[56:81].rstrip() #25
		patient["city"] = record[81:106].rstrip()#25
		patient["province"] = record[106:108].rstrip()#2
		patient["post_code"] = record[108:115].rstrip()#7
		patient["birth_date"] = record[115:123].rstrip()#8
		patient["chart"] = record[123:130].rstrip()#7
		patient["class"] = record[130:131].rstrip()#1
		patient["referring_physician_initial"] = record[131:132].rstrip()#1
		patient["referring_physician_last_name"] = record[132:140].rstrip()#?
		patient["referring_physician_number"] = record[140:144].rstrip() #? there are not patient data with these both fields
		patient["home_phone"] = record[150:162].rstrip()#12
		patient["bus_phone"] = record[162:174].rstrip()#12
		patient["adm_date"] = record[174:182].rstrip()#8
		patient["comments"] = record[182:202].rstrip()#20
		patient["billing"] = record[202:203].rstrip()#1
		patient["default_diag"] = record[203:206].rstrip()#3
		patient["suscribed_last_name"] = record[206:220].rstrip()#14
		patient["date_entered"] = record[220:228].rstrip()#8
		patient["last_updated"] = record[228:236].rstrip()#8
		patient["last_visit"] = record[236:244].rstrip()#8
		return MEDTEXRecord(patient)


class MEDTEXDissasambler(object):
	def __init__(self, data_reader):
		self.content = data_reader.data

	def records(self):
		records = []

		START = 4102 # RECORDS START AT THIS BYTE+1
		OFFSET = 244 # SIZE OF A RECORD
		BETWEEN_RECORDS = 20 # BETWEEN RECORDS
		BETWEEN_BLOCK_OF_THREE = 252

		exp = re.compile('^[A-Z]')
		count = 0
		b = START
		while b < len(self.content):
			try:
				data = self.content[b:b+OFFSET]
				if exp.match(data):
					#print data
					records.append(data)
			except:
				pass
			b += OFFSET
			count += 1
			if count == 3:
				count=0
				b += BETWEEN_BLOCK_OF_THREE
			else:
				b += BETWEEN_RECORDS
		return records	




if __name__ == "__main__":
	parser = MEDTEXRecordParser()	
	patients = parser.patients(MEDTEXDissasambler(MEDTEXDataReader("PATFLE.DAT")))
	print "keycode, last_name, first_name, sex, health_number, version, address, city, province, post_code, birth_date, chart, class, referring_physician_initial, referring_physician_last_name, referring_physician_number, home_phone, bus_phone, adm_date, comments, billing, default_diag, suscribed_last_name, date_entered, last_updated, last_visit"
	for patient in patients:
		print patient.to_csv()		