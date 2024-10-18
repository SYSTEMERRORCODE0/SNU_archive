package target;

import datastructure.Course;

import java.util.Comparator;

public class CompareByAy implements Comparator<Course> {
    @Override
    public int compare(Course a, Course b) {
        if(a.academicYear == b.academicYear) {
            return new CompareById().compare(a, b);
        }
        if(b.academicYear < a.academicYear) return 1;
        else if(b.academicYear == a.academicYear) return 0;
        else return -1;
    }
}
