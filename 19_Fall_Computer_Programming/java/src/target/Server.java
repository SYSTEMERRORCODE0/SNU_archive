package target;

import datastructure.*;

import java.io.*;
import java.util.*;
import java.util.zip.CheckedOutputStream;

import static datastructure.Config.MAX_MILEAGE_PER_COURSE;

public class Server {

    public List<Course> search(Map<String,Object> searchConditions, String sortCriteria){
        // TODO Problem 2.1.
        ///////////file loading////////////////////////////////////
        File file = new File("data/Courses/2020_Spring");
        File[] deptFolders = file.listFiles();
        List<Course> courseList = new LinkedList<>();
        for(File deptFolder : deptFolders) {
            File[] textFiles = deptFolder.listFiles();
            for(File textFile : textFiles) {
                try {
                    Scanner scanner = new Scanner(textFile);
                    String s = scanner.nextLine();
                    Course course = new Course(Integer.parseInt(textFile.getName().split("\\.")[0]),
                            deptFolder.getName(), s.split("\\|")[0], s.split("\\|")[1],
                            Integer.parseInt(s.split("\\|")[2]), s.split("\\|")[3],
                            Integer.parseInt(s.split("\\|")[4]), s.split("\\|")[5], s.split("\\|")[6],
                            Integer.parseInt(s.split("\\|")[7]));
                    courseList.add(course);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
            }
        }
        ////////////////////////////////////////////////////////////
        ////////////collect courses/////////////////////////////////
        if(searchConditions == null || searchConditions.isEmpty()) {
            //empty
        } else {
            if(searchConditions.containsKey("dept")) {
                for(int i = 0; i < courseList.size(); i++) {
                    Course course = courseList.get(i);
                    if(!course.department.equals(searchConditions.get("dept"))) {
                        courseList.remove(course);
                        i--;    //because courseList.size decreasses
                    }
                }
            }
            if(searchConditions.containsKey("ay")) {
                for(int i = 0; i < courseList.size(); i++) {
                    Course course = courseList.get(i);
                    if(course.academicYear != (int)searchConditions.get("ay")) {
                        courseList.remove(course);
                        i--;    //because courseList.size decreasses
                    }
                }
            }
            if(searchConditions.containsKey("name")) {
                for(int i = 0; i < courseList.size(); i++) {
                    Course course = courseList.get(i);
                    String[] words = ((String)searchConditions.get("name")).split(" ");
                    for(String word : words) {
                        if (!course.courseName.contains(word)) {
                            courseList.remove(course);
                            i--;    //because courseList.size decreasses
                            break;
                        }
                    }
                }
            }
        }
        ////////////////////////////////////////////////////////////
        ////////////sort courses////////////////////////////////////
        if(sortCriteria == null || sortCriteria.isEmpty() || sortCriteria == "id") {
            courseList.sort(new CompareById());
        } else if(sortCriteria == "name") {
            courseList.sort(new CompareByName());
        } else if(sortCriteria == "dept") {
            courseList.sort(new CompareByDept());
        } else {
            courseList.sort(new CompareByAy());
        }
        return courseList;
    }

    public int bid(int courseid, int mileage, String userid){
        // TODO Problem 2.2.
        File usersFolder = new File("data/Users");
        File user = new File("data/Users");
        boolean errorCatch = true;
        for(File userFolder : usersFolder.listFiles()) {
            if (userFolder.getName().equals(userid)) {
                user = userFolder;
                errorCatch = false;
            }
        }
        if(errorCatch) return ErrorCode.USERID_NOT_FOUND;

        errorCatch = true;
        for(Course course : search(null, null)) {
            if(course.courseId == courseid) {
                errorCatch = false;
            }
        }
        if(errorCatch) {
            return ErrorCode.NO_COURSE_ID;
        }

        if(mileage < 0) return ErrorCode.NEGATIVE_MILEAGE;

        Config config = new Config();
        if(mileage > config.MAX_MILEAGE_PER_COURSE) return ErrorCode.OVER_MAX_COURSE_MILEAGE;

        Pair<Integer, List<Bidding>> prevBids = retrieveBids(userid);
        int tempSum = 0;
        boolean hasAlready = false;
        for(Bidding bid : prevBids.value) {
            if(courseid != bid.courseId) {
                tempSum += bid.mileage;
            } else {
                if(mileage == 0) {
                    prevBids.value.remove(bid);
                } else {
                    bid.mileage = mileage;
                }
                hasAlready = true;
            }
        }
        if(!hasAlready) {
            prevBids.value.add(new Bidding(courseid, mileage));
        }
        if(tempSum + mileage > config.MAX_MILEAGE) return ErrorCode.OVER_MAX_MILEAGE;

        File textFile = user.listFiles()[0];
        try {
            FileWriter fileWriter = new FileWriter(textFile);
            for(Bidding bid : prevBids.value) {
                String format = String.format("%d|%d\n", bid.courseId, bid.mileage);
                fileWriter.append(format);
                fileWriter.flush();
            }
            fileWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return ErrorCode.SUCCESS;
    }

    public Pair<Integer,List<Bidding>> retrieveBids(String userid){
        // TODO Problem 2.2.
        File usersFolder = new File("data/Users");
        List<Bidding> bids = new LinkedList<>();
        for(File userFolder : usersFolder.listFiles()) {
            if(userFolder.getName().equals(userid)) {
                File textFile = userFolder.listFiles()[0];
                try {
                    Scanner scanner = new Scanner(textFile);
                    String s;
                    while(scanner.hasNext()) {
                        s = scanner.nextLine();
                        int courseId = Integer.parseInt(s.split("\\|")[0]);
                        int mileage = Integer.parseInt(s.split("\\|")[1]);
                        if(mileage == 0) continue;
                        Bidding bidding = new Bidding(courseId, mileage);
                        bids.add(bidding);
                    }
                    scanner.close();
                    return new Pair<>(ErrorCode.SUCCESS,bids);
                } catch (FileNotFoundException e) {
                    return new Pair<>(ErrorCode.IO_ERROR,new ArrayList<>());
                }
            }
        }
        return new Pair<>(ErrorCode.USERID_NOT_FOUND,new ArrayList<>());
    }

    public boolean clearBids(){
        // TODO Problem 2.3.
        List<Course> courses = search(null, null);
        File usersFolder = new File("data/Users");
        List<Pair<File, List<Bidding>>> collectedusers = new LinkedList<>();
        for(File userFolder : usersFolder.listFiles()) {
            collectedusers.add(new Pair<>(userFolder, retrieveBids(userFolder.getName()).value));
        }
        for(Course course : courses) {
            int courseQuota = course.quota;
            List<Pair<String, Pair<Integer, Integer>>> bidded = new LinkedList<>();    //userid, (mileage, totalBids)
            for(Pair<File, List<Bidding>> user : collectedusers) {
                for(Bidding bidding : user.value) {
                    if(bidding.courseId == course.courseId) {
                        bidded.add(new Pair<>(user.key.getName(), new Pair(bidding.mileage, user.value.size())));
                    }
                }
            }
            Collections.sort(bidded, new ComPair());
            for(Pair<String, Pair<Integer, Integer>> user_bid : bidded) {
                if(courseQuota <= 0) {

                    for(Pair<File, List<Bidding>> user : collectedusers) {
                        if(user.key.getName().equals(user_bid.key)) {

                            for(int i = 0; i < user.value.size(); i++) {
                                if(user.value.get(i).courseId == course.courseId) {
                                    user.value.remove(user.value.get(i));
                                }
                            }
                        }
                    }
                }
                courseQuota--;
            }
        }

        for(Pair<File, List<Bidding>> user : collectedusers) {
            try {
                FileWriter fileWriter = new FileWriter(user.key.toString() + "/confirmed.txt");
                for(Bidding bidding : user.value) {
                    fileWriter.append(Integer.toString(bidding.courseId) + "\n");
                }
                fileWriter.flush();
                fileWriter.close();
            } catch (IOException e) {
                return false;
            }
        }

        return true;
    }

    public Pair<Integer,List<Course>> retrieveRegisteredCourse(String userid){
        // TODO Problem 2.3.
        File usersFolder = new File("data/Users");
        boolean Error = true;
        for(File folder : usersFolder.listFiles()) {
            if(folder.getName().equals(userid)) {
                Error = false;
            }
        }
        if(Error) return new Pair<>(ErrorCode.USERID_NOT_FOUND,new ArrayList<>());

        String string = usersFolder + "/" + userid + "/confirmed.txt";
        File file = new File(string);
        List<Course> courses = new ArrayList<>();
        try {
            Scanner scanner = new Scanner(file);
            while(scanner.hasNext()) {
                int courseId = Integer.parseInt(scanner.nextLine());
                List<Course> temp = search(null, null);
                for(Course course : temp) {
                    if(courseId == course.courseId) {
                        courses.add(course);
                    }
                }
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            return new Pair<>(ErrorCode.IO_ERROR,new ArrayList<>());
        }
        string = usersFolder + "/" + userid + "/bid.txt";
        file = new File(string);
        try {
            FileWriter fileWriter = new FileWriter(file);
            fileWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
            return new Pair<>(ErrorCode.IO_ERROR,new ArrayList<>());
        }
        return new Pair<>(ErrorCode.SUCCESS, courses);
    }
}