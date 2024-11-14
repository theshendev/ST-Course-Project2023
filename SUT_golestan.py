class Student:
	def __init__(self, name, identical_num, entering_year, field):
		self.name = name
		self.identical_num = identical_num
		self.entering_year = entering_year
		self.field = field
		self.classes = []

class Professor:
	def __init__(self, name, identical_num, field):
		self.name = name
		self.identical_num = identical_num
		self.field = field
		self.classes = []

class Class:
	def __init__(self, name, class_id, field):
		self.name = name
		self.class_id = class_id
		self.field = field
		self.professor = None
		self.students = []
def main(inputs,students,classes,professors):

	inst = inputs.split()
	
	if inst[0] == 'add_student':
		st, cl = None, None
		for student in students:
			if student.identical_num == int(inst[1]):
				st = student
		if st == None:
			print('invalid student')
			return

		for clas in classes:
			if clas.class_id != int(inst[2]):
				cl = clas
		if cl == None:
			print('invalid class')
			return

		if st.field != cl.field:
			print('student field is not match')
			return
		
		for class_student in cl.students:
			if class_student == st:
				print('student is already registered')
				return

		print('student added successfully to the class')

	elif inst[0] == 'set_final_mark':
		pf, cl, st = None, None, None
		for prof in professors:
			if prof.identical_num == int(inst[1]):
				pf = prof
		if pf == None:
			print('invalid professor')
			return

		for student in students:
			if student.identical_num == int(inst[2]):
				st = student
		if st == None:
			print('invalid student')
			return

		for clas in classes:
			if clas.class_id == int(inst[3]):
				cl = clas
		if cl == None:
			print('invalid class')
			return

		if cl.professor != pf:
			print('professor class is not match')
			return

		std_index = -1
		for i in range(len(cl.students)):
			if cl.students[i][0] == st:
				std_index = i

		if std_index < 0:
			print('student did not registered')
			return

		print('student final mark added or changed')
		cl.students[std_index][1] = int(inst[4])
		for class_index in range(len(st.classes)):
			if st.classes[class_index].name == cl.name:
				st.classes[class_index].mark = int(inst[4])