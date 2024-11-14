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
	while inst[0] != 'end':
		flag = True
		if inst[0] == 'register_student' or inst[0] == 'register_professor':
			for student in students:
				if student.identical_num == inst[2]:
					print('this identical number previously registered')
					flag = False
			if flag:
				for prof in professors:
					if prof.identical_num == inst[2]:
						print('this identical number previously registered')
						flag = False
			if flag:
				print('welcome to golestan')
				if inst[0] == 'register_student':
					students.append(Student(inst[1],inst[2],inst[3],inst[4]))
				else:
					professors.append(Professor(inst[1],inst[2],inst[3]))
			
		elif inst[0] == 'make_class':
			for clas in classes:
				if clas.class_id == inst[2]:
					print('this class id previously used')
					flag = False
			if flag:
				print('class added successfully')
				classes.append(Class(inst[1],inst[2],inst[3]))
		elif inst[0] == 'add_student':
			st, cl = None, None
			for student in students:
				if student.identical_num == inst[1]:
					st = student
			if st == None:
				print('invalid student')

			for clas in classes:
				if clas.class_id == inst[2]:
					cl = clas
			if cl == None:
				print('invalid class')
				

			if st.field != cl.field:
				print('student field is not match')
				
				
			
			for class_student in cl.students:
				if class_student[0] == st:
					print('student is already registered')
					flag = False
					

			if not(flag):
				
				

			print('student added successfully to the class')
			cl.students.append([st,None])
			st.classes.append([cl.name,None])


		elif inst[0] == 'add_professor':
			pf, cl = None, None
			for prof in professors:
				if prof.identical_num == inst[1]:
					pf = prof
					
			if pf == None:
				print('invalid professor')
				
				

			for clas in classes:
				if clas.class_id == inst[2]:
					cl = clas
					
			if cl == None:
				print('invalid class')
				
				

			if pf.field != cl.field:
				print('professor field is not match')
				
				

			if cl.professor != None:
				print('this class has a professor')
				
				

			print('professor added successfully to the class')
			cl.professor = pf
			pf.classes.append(cl.name)

		elif inst[0] == 'student_status':
			st = None
			for student in students:
				if student.identical_num == inst[1]:
					st = student
					
			if st == None:
				print('invalid student')
				
				
			
			print(st.name, st.entering_year, st.field, end = ' ')
			for clas in st.classes[:-1]:
				print(clas[0], end = ' ')
			if len(st.classes) > 0:
				print(st.classes[-1][0])
			else:
				print()

		elif inst[0] == 'professor_status':
			pf = None
			for prof in professors:
				if prof.identical_num == inst[1]:
					pf = prof
					
			if pf == None:
				print('invalid professor')
				
				
			
			print(pf.name, pf.field, end = ' ')
			for clas in pf.classes[:-1]:
				print(clas, end = ' ')
			if len(pf.classes) > 0:
				print(pf.classes[-1])
			else:
				print()

		elif inst[0] == 'class_status':
			cl = None
			for clas in classes:
				if clas.class_id == inst[1]:
					cl = clas
					
			if cl == None:
				print('invalid class')
				
				

			if cl.professor == None:
				print('None', end = ' ')
			else:
				print(cl.professor.name, end = ' ')
			
			for clas_student in cl.students[:-1]:
				print(clas_student[0].name, end = ' ')
			if len(cl.students) > 0:
				print(cl.students[-1][0].name)
			else:
				print()

		elif inst[0] == 'set_final_mark':
			pf, cl, st = None, None, None
			for prof in professors:
				if prof.identical_num == inst[1]:
					pf = prof
					
			if pf == None:
				print('invalid professor')
				
				

			for student in students:
				if student.identical_num == inst[2]:
					st = student
					
			if st == None:
				print('invalid student')
				
				

			for clas in classes:
				if clas.class_id == inst[3]:
					cl = clas
					
			if cl == None:
				print('invalid class')
				
				

			if cl.professor != pf:
				print('professor class is not match')

			std_index = -1
			for i in range(len(cl.students)):
				if cl.students[i][0] == st:
					std_index = i
			if std_index < 0:
				print('student did not registered')
			print('student final mark added or changed')
			cl.students[std_index][1] = int(inst[4])
			for class_index in range(len(st.classes)):
				if st.classes[class_index][0] == cl.name:
					st.classes[class_index][1] = int(inst[4])
		elif inst[0] == 'mark_student':
			cl, st = None, None
			for student in students:
				if student.identical_num == inst[1]:
					st = student
					
			if st == None:
				print('invalid student')
				
				

			for clas in classes:
				if clas.class_id == inst[2]:
					cl = clas
					
			if cl == None:
				print('invalid class')
				
				

			std_index = -1
			for i in range(len(cl.students)):
				if cl.students[i][0] == st:
					std_index = i
					grade = cl.students[i][1]
					

			if std_index < 0:
				print('student did not registered')
				
				

			print(grade)

		elif inst[0] == 'mark_list':
			cl = None
			for clas in classes:
				if clas.class_id == inst[1]:
					cl = clas
			if cl == None:
				print('invalid class')
			if cl.professor == None:
				print('no professor')
			if len(cl.students) == 0:
				print('no student')
			for class_std in cl.students[:-1]:
				print(class_std[1], end = ' ')
			if len(cl.students) > 0:
				print(cl.students[-1][1])

		elif inst[0] == 'average_mark_professor':
			pf = None
			for prof in professors:
				if prof.identical_num == inst[1]:
					pf = prof
					
			if pf == None:
				print('invalid professor')
			sum = 0
			count = 0
			for clas in classes:
				if clas.professor == pf:
					for class_std in clas.students:
						if class_std[1] != None:
							sum += class_std[1]
							count += 1
			if count == 0:
				print('None')
			else:
				print("%.2f"%(sum/count))

		elif inst[0] == 'average_mark_student':
			st = None
			for student in students:
				if student.identical_num == inst[1]:
					st = student
			if st == None:
				print('invalid student')
			sum = 0
			count = 0
			for std_class in st.classes:
				if std_class[1] != None:
					sum += std_class[1]
					count += 1
			if count == 0:
				print('None')
			else:
				print("%.2f"%(sum/count))
		elif inst[0] == 'top_student':
			max_mean = -1
			max_std = None
			for std in students:
				if std.field == inst[1] and std.entering_year == inst[2]:
					sum = 0
					count = 0
					for std_class in std.classes:
						if std_class[1] != None:
							sum += std_class[1]
							count += 1
					if count > 0 and sum/count > max_mean:
						max_mean = sum/count
						max_std = std.name
			print(max_std)
		elif inst[0] == 'top_mark':
			cl = None
			for clas in classes:
				if clas.class_id == inst[1]:
					cl = clas	
			if cl == None:
				print('invalid class')
			max_grade = -1
			for class_std in cl.students:
				if class_std[1] != None:
					max_grade = max(max_grade, class_std[1])
			if max_grade < 0:
				print('None')
			else:
				print(max_grade)

		print()