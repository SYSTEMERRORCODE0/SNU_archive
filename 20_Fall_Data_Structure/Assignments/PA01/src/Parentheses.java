import structures.stack.LinkedStack;
import structures.stack.Stack;

class Parentheses {
    public boolean isValid(String s) {
        //Fill your code here
        Stack<Character> stack = new LinkedStack<Character>();

        int length = s.length();
        for(int i = 0; i < length; i++) {
            Character c;
            switch (s.charAt(i)) {
                case '(' :
                case '{' :
                case '[' :
                    stack.push(s.charAt(i));
                    break;

                case ')' :
                    c = stack.pop();
                    if(c == null || c != '(') return false;
                    break;

                case '}' :
                    c = stack.pop();
                    if(c == null || c != '{') return false;
                    break;

                case ']' :
                    c = stack.pop();
                    if(c == null || c != '[') return false;
                    break;
            }
        }
        if(stack.isEmpty()) return true;
        return false;
    }
}