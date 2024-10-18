package target;

import datastructure.Course;

import java.util.Comparator;

public class CompareByDept implements Comparator<Course> {
    @Override
    public int compare(Course a, Course b) {
        if(a.department.equals(b.department)) {
            return new CompareById().compare(a, b);
        }
        return a.department.compareTo(b.department);
    }
}
