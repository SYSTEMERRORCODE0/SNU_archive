import java.util.Scanner;

import structures.queue.LinkedQueue;
import structures.queue.Queue;
import structures.stack.LinkedStack;
import structures.stack.Stack;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.util.LinkedList;

public class Main {

        @SuppressWarnings("resource")
        public static void main(String[] args) {

            FileInputStream fis = null;
            BufferedReader reader = null;

            try {
                fis = new FileInputStream("sample_input.txt");
            } catch (FileNotFoundException e) {
                e.printStackTrace();
                return;
            }
            reader = new BufferedReader(new InputStreamReader(fis));

            String line;
            LinkedList<String> outputs = new LinkedList<String>();
            Stack<Integer> stack = new LinkedStack<Integer>();
            Queue<Integer> queue = new LinkedQueue<Integer>();
            Parentheses par = new Parentheses();

            try {
                for (line=reader.readLine(); line !=null; line=reader.readLine()) {
                    String[] line_split = line.split(",");
                    String cmd_type = line_split[0];

                    if (cmd_type.equals("stack")) {
                        String cmd = line_split[1];
                        if (cmd.equals("clear")) {
                            stack.clear();
                            outputs.add("clear success");
                        } else if (cmd.equals("push")) {
                            int value = Integer.valueOf(line_split[2]);
                            stack.push(value);
                            outputs.add("push "+ value);
                        } else if (cmd.equals("pop")) {
                            outputs.add("pop " + stack.pop());
                        } else if (cmd.equals("length")) {
                            outputs.add(String.valueOf(stack.length()));
                        }
                        else if (cmd.equals("isempty")) {
                            outputs.add(String.valueOf(stack.isEmpty()));
                        }
                    } else if (cmd_type.equals("queue")) {
                        String cmd = line_split[1];
                        if (cmd.equals("clear")) {
                            queue.clear();
                            outputs.add("clear success");
                        } else if (cmd.equals("enqueue")) {
                            int value = Integer.valueOf(line_split[2]);
                            queue.enqueue(value);
                            outputs.add("enqueue " + value);
                        } else if (cmd.equals("dequeue")) {
                            outputs.add("dequeue " + queue.dequeue());
                        }
                        else if (cmd.equals("length")) {
                            outputs.add(String.valueOf(queue.length()));
                        } else if (cmd.equals("isempty")) {
                            outputs.add(String.valueOf(queue.isEmpty()));
                        }
                    } else if (cmd_type.equals("isvalid")) {
                        String infix = line_split[1];
                        outputs.add(String.valueOf(par.isValid(infix)));
                    }

                }
            } catch (Exception e) {
                e.printStackTrace();
            }

            for (String output : outputs) {
                System.out.println(output);
            }
        }


}