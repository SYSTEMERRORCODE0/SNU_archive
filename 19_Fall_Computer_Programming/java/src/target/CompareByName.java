package target;

import datastructure.Course;

import java.util.Comparator;

public class CompareByName implements Comparator<Course> {
    @Override
    public int compare(Course a, Course b) {
        if(a.courseName.equals(b.courseName)) {
            return new CompareById().compare(a, b);
        }
        return a.courseName.compareTo(b.courseName);
    }
}
