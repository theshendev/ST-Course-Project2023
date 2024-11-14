from hypothesis import given,settings
import hypothesis.strategies as st
import pytest
from io import StringIO
from contextlib import redirect_stdout
from SUT_golestan import Student, Professor, Class,main

# Alphabet for random texts to use
alphabet = st.characters(min_codepoint=65, max_codepoint=90) | st.characters(min_codepoint=97, max_codepoint=122)

# Random data to generate prerequisites for tests (Register student, make class and etc.)
student_strategy = st.fixed_dictionaries(
    {
        'name': st.text(min_size=1,alphabet=alphabet),
        'identical_num': st.integers(min_value=1000000000, max_value=9999999999),
        'entering_year': st.integers(min_value=2000, max_value=2023),
        'field': st.text(min_size=1,alphabet=alphabet),
    }
)

class_strategy = st.fixed_dictionaries(
    {
        'name': st.text(min_size=1,alphabet=alphabet),
        'class_id': st.integers(min_value=1000000000, max_value=9999999999),
        'field': st.text(min_size=1,alphabet=alphabet),
    }
)

professor_strategy = st.fixed_dictionaries(
    {
        'name': st.text(min_size=1,alphabet=alphabet),
        'identical_num': st.integers(min_value=1000000000, max_value=9999999999),
        'field': st.text(min_size=1,alphabet=alphabet),
    }
)
@settings(max_examples=100)
@given(
    student_data=student_strategy,
    class_data=class_strategy,
)
def test_add_student(student_data,class_data):
    # Test the add_student function
    students = []
    
    classes = []

    # Create a sample student object
    student = Student(**student_data)

    # Add the student to the list of students
    students.append(student)

    # Create a sample class object
    class_obj = Class(**class_data)

    # Add the class to the list of classes
    classes.append(class_obj)
    inst = f"add_student {student_data['identical_num']} {class_data['class_id']}"

    output = capture_output(main,inst,students,classes,[])

    if student.field != class_obj.field:
        # Student field does not match class field
        expected_output = "student field is not match\n"
        assert output == expected_output            
    else:
        # Student added successfully to the class
        expected_output = "student added successfully to the class\n"

        # Add the student to the class in order to check other tests based on this addition
        classes.remove(class_obj)
        class_obj.students.append([student,None])
        classes.append(class_obj)
        assert output == expected_output
    for prop in student.__dict__.keys():
        assert getattr(student, prop) is not None
    for prop in class_obj.__dict__.keys():
        if prop != 'professor':
            assert getattr(class_obj, prop) is not None

@settings(max_examples=10)
@given(
    student_data=student_strategy,
    class_data=class_strategy,
)
def test_add_already_registered_student(student_data,class_data):
    # Test the add_student function
    students = []
    
    classes = []

    # Create a sample student object
    student = Student(**student_data)
    student.field = class_data['field']
    # Add the student to the list of students
    students.append(student)

    # Create a sample class object
    class_obj = Class(**class_data)
    class_obj.students.append(student)
    # Add the class to the list of classes
    classes.append(class_obj)
    inst = f"add_student {student_data['identical_num']} {class_data['class_id']}"

    output = capture_output(main,inst,students,classes,[])

    expected_output = "student is already registered\n"
    assert output == expected_output
    
@settings(max_examples=10)
@given(
    student_data=student_strategy,
    class_data=class_strategy,
)
def test_add_invalid_student(student_data,class_data):
    students = []
    classes = []
    # Create a sample student object
    student = Student(**student_data)

    # Create a sample class object
    class_obj = Class(**class_data)

    # Add the class to the list of classes
    classes.append(class_obj)
    inst = f"add_student {student_data['identical_num']} {class_data['class_id']}"

    output = capture_output(main,inst,students,classes,[])
    expected_output = "invalid student\n"
    assert output == expected_output


@settings(max_examples=10)
@given(
    student_data=student_strategy,
    class_data=class_strategy,
)
def test_add_invalid_class(student_data,class_data):
    students = []
    classes = []
    # Create a sample student object
    student = Student(**student_data)
    students.append(student)

    # Create a sample class object
    class_obj = Class(**class_data)

    # Add the class to the list of classes
    inst = f"add_student {student_data['identical_num']} {class_data['class_id']}"

    output = capture_output(main,inst,students,classes,[])
    expected_output = "invalid class\n"
    assert output == expected_output

@settings(max_examples=100)
@given(
    student_data=student_strategy,
    class_data=class_strategy,
    professor_data=professor_strategy,
    mark=st.integers(min_value=0, max_value=20),
    assigned_professor = st.booleans(),
    registered_student = st.booleans()
)
def test_set_final_mark(student_data,class_data,professor_data,mark,assigned_professor,registered_student):
    # Test the set_final_mark function
    students = []
    professors = []
    classes = []

    # Create a sample professor object
    professor = Professor(**professor_data)
    for prop in professor.__dict__.keys():
        assert getattr(professor, prop) is not None
    # Create a sample student object
    student = Student(**student_data)

    # Create a sample class object
    class_obj = Class(**class_data)

    # Add the professor, student, and class to their respective lists
    professors.append(professor)
    students.append(student)
    if assigned_professor:
        class_obj.professor = professor
    if registered_student:
        class_obj.students.append([student,None])
        student.classes.append(class_obj)
    classes.append(class_obj)

    inst = f"set_final_mark {professor_data['identical_num']} {student_data['identical_num']} {class_data['class_id']} {mark}"


    output = capture_output(main, inst, students, classes, professors)


    # Find the class associated with the professor
    professor_class = None
    for cls in classes:
        if cls.professor == professor:
            professor_class = cls
            break

    # Check if the professor is assigned to the class
    if professor_class is None:
        expected_output = "professor class is not match\n"
        assert output == expected_output

    # Check if the student is registered in the class
    elif [student, None] not in professor_class.students and [student,mark] not in professor_class.students:
        expected_output = "student did not registered\n"
        assert output == expected_output

    # Update the student's final mark
    else:
        expected_output = "student final mark added or changed\n"
        assert output == expected_output

@settings(max_examples=10)
@given(
    student_data=student_strategy,
    class_data=class_strategy,
    professor_data=professor_strategy,
    mark=st.integers(min_value=0, max_value=20),
)
def test_set_final_mark_for_invalid_student(student_data,class_data,professor_data,mark):
    # Test the set_final_mark function
    students = []
    professors = []
    classes = []

    # Create a sample professor object
    professor = Professor(**professor_data)

    # Create a sample student object
    student = Student(**student_data)

    # Create a sample class object
    class_obj = Class(**class_data)

    # Add the professor, student, and class to their respective lists
    professors.append(professor)
    classes.append(class_obj)

    inst = f"set_final_mark {professor_data['identical_num']} {student_data['identical_num']} {class_data['class_id']} {mark}"

    output = capture_output(main, inst, students, classes, professors)
    expected_output = "invalid student\n"
    assert output == expected_output
@settings(max_examples=10)
@given(
    student_data=student_strategy,
    class_data=class_strategy,
    professor_data=professor_strategy,
    mark=st.integers(min_value=0, max_value=20),
)
def test_set_final_mark_for_invalid_professor(student_data,class_data,professor_data,mark):
    # Test the set_final_mark function
    students = []
    professors = []
    classes = []

    # Create a sample professor object
    professor = Professor(**professor_data)

    # Create a sample student object
    student = Student(**student_data)

    # Create a sample class object
    class_obj = Class(**class_data)

    # Add the professor, student, and class to their respective lists
    students.append(student)
    classes.append(class_obj)

    inst = f"set_final_mark {professor_data['identical_num']} {student_data['identical_num']} {class_data['class_id']} {mark}"

    output = capture_output(main, inst, students, classes, professors)
    expected_output = "invalid professor\n"
    assert output == expected_output

@settings(max_examples=10)
@given(
    student_data=student_strategy,
    class_data=class_strategy,
    professor_data=professor_strategy,
    mark=st.integers(min_value=0, max_value=20),
)
def test_set_final_mark_for_invalid_class(student_data,class_data,professor_data,mark):
    # Test the set_final_mark function
    students = []
    professors = []
    classes = []

    # Create a sample professor object
    professor = Professor(**professor_data)

    # Create a sample student object
    student = Student(**student_data)

    # Create a sample class object
    class_obj = Class(**class_data)

    # Add the professor, student, and class to their respective lists
    students.append(student)
    professors.append(professor)

    inst = f"set_final_mark {professor_data['identical_num']} {student_data['identical_num']} {class_data['class_id']} {mark}"

    output = capture_output(main, inst, students, classes, professors)
    expected_output = "invalid class\n"
    assert output == expected_output

def capture_output(func, *args):
    output = StringIO()
    with redirect_stdout(output):
        func(*args)
    return output.getvalue()

