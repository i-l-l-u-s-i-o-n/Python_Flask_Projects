from application.models import User, Course, Enrollment

def course_list(user_id):    
    classes = list(User.objects.aggregate(*[
        {
            '$lookup': {    # Performs left outer join
                'from': 'enrollment',
                'localField': 'user_id',
                'foreignField': 'user_id',
                'as': 'r1'
            }
        }, {
            '$unwind': {    # converts the array r1 to the object notation
                'path': '$r1',
                'includeArrayIndex': 'r1_id',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$lookup': {  # Again finding the course details returned from the join of user and enrollment
                'from': 'course',
                'localField': 'r1.courseID',
                'foreignField': 'courseID',
                'as': 'r2'
            }
        }, {
            '$unwind': {
                'path': '$r2',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$match': {
                'user_id': user_id  # Getting the courses to which the current user enrolled
            }
        }, {
            '$sort': {
                'courseID': 1  # +1 means ascending and -1 means descending
            }
        }
    ]))

    return classes