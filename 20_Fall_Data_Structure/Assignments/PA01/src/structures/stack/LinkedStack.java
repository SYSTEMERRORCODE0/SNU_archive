package structures.stack;

import java.util.LinkedList;

public class LinkedStack<E> implements Stack<E> {
	
	private LinkedList<E> list = new LinkedList<E>();
	private E top = null;
	private int length = 0;

	@Override
	public void clear() {
		//Fill your code here
		list.clear();
		top = null;
		length = 0;
	}

	@Override
	public void push(E item) {
		//Fill your code here
		list.add(item);
		top = item;
		length++;
	}

	@Override
	public E pop() {
		//Fill your code here
		if(length == 0) {
			return null;
		}
		E e = list.removeLast();
		if(length == 1) top = null;
		else top = list.getLast();
		length--;
		return e;
	}

	@Override
	public int length() {
		//Fill your code here
		return length;
	}

	@Override
	public boolean isEmpty() {
		//Fill your code here
		return list.isEmpty();
	}

}
