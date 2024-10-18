package target;

import datastructure.Course;

import java.util.Comparator;

public class CompareById implements Comparator<Course> {

    @Override
    public int compare(Course a, Course b) {
        if(b.courseId < a.courseId) return 1;
        else if(b.courseId == a.courseId) return 0;
        else return -1;
    }
}
